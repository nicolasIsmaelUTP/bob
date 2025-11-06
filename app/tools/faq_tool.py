import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from langchain.tools import tool
from openai import OpenAI
from ..config import Config
import pickle

# Ruta absoluta al archivo CSV
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FAQ_FILE = BASE_DIR / 'data' / 'faqs.csv'
EMB_FILE = BASE_DIR / 'data' / 'faq_embeddings.pkl'

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class FAQStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FAQStore, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance
    
    def _load_data(self):
        self.faq_df = pd.read_csv(FAQ_FILE)
        if EMB_FILE.exists():
            with open(EMB_FILE, 'rb') as f:
                self.faq_embeddings = pickle.load(f)
        else:
            self.faq_embeddings = self._generate_embeddings()
            with open(EMB_FILE, 'wb') as f:
                pickle.dump(self.faq_embeddings, f)

    def _generate_embeddings(self):
        texts = (
            self.faq_df['Categoría'].astype(str) + ' ' +
            self.faq_df['Empresa'].astype(str) + ' ' +
            self.faq_df['Pregunta'].astype(str) + ' ' +
            self.faq_df['Respuesta'].astype(str)
        ).tolist()
        embeddings = []
        for chunk in range(0, len(texts), 100):
            response = client.embeddings.create(
                input=texts[chunk:chunk+100],
                model="text-embedding-3-small"
            )
            embeddings.extend([e.embedding for e in response.data])
        return embeddings

faq_store = FAQStore()

@tool
def search_faq(query: str, top_n: int = 3) -> str:
    """
    Busca en las preguntas frecuentes de Bob Subastas usando similitud semántica basada en embeddings.
    Esta función usa embeddings de OpenAI para encontrar las FAQs más similares
    basándose en la consulta del usuario. Devuelve información detallada sobre las preguntas y respuestas más coincidentes.
    
    Args:
        query (str): La consulta de búsqueda del usuario.
        top_n (int, opcional): Número de FAQs similares a devolver. Por defecto es 3.

    Returns:
        str: Una cadena formateada que contiene las preguntas y respuestas más coincidentes,
             incluyendo categoría y empresa. Devuelve un mensaje si no se encuentran FAQs.
    
    Examples:
        - Usa esta herramienta cuando el usuario pregunte sobre Bob Subastas, sus políticas o procedimientos
        - Usa esta herramienta cuando el usuario necesite información general sobre la empresa
        - Usa esta herramienta para resolver dudas frecuentes sobre Bob Subastas
    """
    q_emb = client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    ).data[0].embedding

    sims = cosine_similarity(
        [q_emb],
        faq_store.faq_embeddings
    ).flatten()
    top_indices = sims.argsort()[-top_n:][::-1]

    results = faq_store.faq_df.iloc[top_indices]
    
    # Formatear resultados como texto
    output = []
    for _, row in results.iterrows():
        output.append(
            f"Categoría: {row['Categoría']}\n"
            f"Empresa: {row['Empresa']}\n"
            f"Pregunta: {row['Pregunta']}\n"
            f"Respuesta: {row['Respuesta']}"
        )
    
    return "\n\n".join(output) if output else "No se encontraron FAQs relacionadas."