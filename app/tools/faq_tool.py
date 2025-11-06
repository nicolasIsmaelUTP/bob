import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain.tools import tool

# Ruta absoluta al archivo CSV
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FAQ_FILE = BASE_DIR / 'data' / 'faqs.csv'

faq_df = pd.read_csv(FAQ_FILE)

vectorizer = TfidfVectorizer()
faq_matrix = vectorizer.fit_transform(faq_df['Pregunta'])

@tool
def search_faq(query: str, top_n: int = 3) -> str:
    """
    Busca en las preguntas frecuentes usando similitud de coseno.

    Args:
        query (str): Consulta del usuario.
        top_n (int, optional): Número de resultados a retornar. Por defecto 3.

    Returns:
        str: Texto formateado con las preguntas y respuestas más relevantes.
    """
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, faq_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    results = faq_df.iloc[top_indices]
    
    # Formatear resultados como texto
    output = []
    for idx, row in results.iterrows():
        output.append(f"Pregunta: {row['Pregunta']}\nRespuesta: {row['Respuesta']}")
    
    return "\n\n".join(output) if output else "No se encontraron FAQs relacionadas."