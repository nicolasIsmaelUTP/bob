import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain.tools import tool

# Ruta absoluta al archivo CSV
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRODUCT_FILE = BASE_DIR / 'data' / 'hackathon_data.csv'

product_df = pd.read_csv(PRODUCT_FILE, encoding='latin-1')

vectorizer = TfidfVectorizer()
product_df['text'] = (
    product_df['title'].astype(str) + ' ' +
    product_df['marca'].astype(str) + ' ' +
    product_df['categoria'].astype(str)
)
product_matrix = vectorizer.fit_transform(product_df['text'])

@tool
def search_product(query: str, top_n: int = 3) -> str:
    """
    Busca productos similares basándose en una consulta de texto.

    Args:
        query (str): Texto de búsqueda para encontrar productos similares.
        top_n (int, optional): Número de resultados a retornar. Por defecto 3.

    Returns:
        str: Texto formateado con los productos más similares.
    """
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, product_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    results = product_df.iloc[top_indices]
    
    # Formatear resultados como texto
    output = []
    for idx, row in results.iterrows():
        product_info = f"Producto: {row['title']}\n"
        if pd.notna(row.get('marca')):
            product_info += f"Marca: {row['marca']}\n"
        if pd.notna(row.get('precio')):
            product_info += f"Precio: ${row['precio']}\n"
        if pd.notna(row.get('categoria')):
            product_info += f"Categoría: {row['categoria']}\n"
        output.append(product_info.strip())
    
    return "\n\n".join(output) if output else "No se encontraron productos relacionados."

