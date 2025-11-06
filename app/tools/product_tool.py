import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain.tools import tool
from openai import OpenAI
from ..config import Config
import pickle

# Ruta absoluta al archivo CSV
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRODUCT_FILE = BASE_DIR / 'data' / 'hackathon_data.csv'
EMB_FILE = BASE_DIR / 'data' / 'product_embeddings.pkl'

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class ProductStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductStore, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance
    
    def _load_data(self):
        self.product_df = pd.read_csv(PRODUCT_FILE, encoding='latin-1')
        if EMB_FILE.exists():
            with open(EMB_FILE, 'rb') as f:
                self.product_embeddings = pickle.load(f)
        else:
            self.product_embeddings = self._generate_embeddings()
            with open(EMB_FILE, 'wb') as f:
                pickle.dump(self.product_embeddings, f)

    def _generate_embeddings(self):
        texts = (
            self.product_df['title'].astype(str) + ' ' +
            self.product_df['marca'].astype(str) + ' ' +
            self.product_df['modelo'].astype(str) + ' ' +
            self.product_df['categoria'].astype(str) + ' ' +
            self.product_df['ubicacion'].astype(str)
        ).tolist()
        embeddings = []
        for chunk in range(0, len(texts), 100):
            response = client.embeddings.create(
                input=texts[chunk:chunk+100],
                model="text-embedding-3-small"
            )
            embeddings.extend([e.embedding for e in response.data])
        return embeddings

product_store = ProductStore()

@tool
def search_product(query: str, top_n: int = 3) -> str:
    """
    Busca productos usando similitud semántica basada en una cadena de consulta.
    Esta función usa embeddings para encontrar los productos más similares en la tienda
    basándose en la consulta del usuario. Devuelve información detallada sobre los productos más coincidentes.
    Args:
        query (str): La consulta de búsqueda que describe el/los producto(s) que el usuario está buscando.
        top_n (int, opcional): Número de productos similares a devolver. Por defecto es 3.
    Returns:
        str: Una cadena formateada que contiene detalles de los productos más coincidentes incluyendo
            ID, título, precio, ubicación, marca, modelo, placa, kilometraje, año, origen,
            estado de garantía, categoría, tipo de subasta y proveedor. Devuelve un mensaje
            si no se encuentran productos.
    Examples:
        - Usa esta herramienta cuando el usuario quiera buscar vehículos o productos
        - Usa esta herramienta cuando el usuario pregunte sobre disponibilidad de artículos específicos
        - Usa esta herramienta cuando el usuario quiera comparar productos similares
    """
    q_emb = client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    ).data[0].embedding

    sims = cosine_similarity(
        [q_emb],
        product_store.product_embeddings
    ).flatten()
    top_indices = sims.argsort()[-top_n:][::-1]

    results = product_store.product_df.iloc[top_indices]
    output = []
    for _, row in results.iterrows():
        output.append(
            f"Title: {row['title']}\n"
            f"Price: {row['precio_base']} {row['tipo_moneda']}\n"
            f"Location: {row['ubicacion']}\n"
            f"Brand: {row['marca']}\n"
            f"Model: {row['modelo']}\n"
            f"Plate: {row['placa']}\n"
            f"Mileage: {row['kilometraje']} km\n"
            f"Year: {row['anio']}\n"
            f"Origin: {row['procedencia']}\n"
            f"Warranty: {row['con_garantia']}\n"
            f"Category: {row['categoria']}\n"
            f"Auction Type: {row['tipo_subasta']}\n"
            f"Provider: {row['empresa_proveedora']}"
        )

    return "\n\n".join(output) if output else "No se encontraron productos relacionados."
