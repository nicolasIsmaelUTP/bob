from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from ..tools.faq_tool import search_faq
from ..tools.product_tool import search_product
from ..config import Config

model = ChatOpenAI(model="gpt-5-mini-2025-08-07", api_key=Config.OPENAI_API_KEY)

agent = create_agent(
    model=model,
    tools=[search_faq, search_product],
    system_prompt="Eres un asistente útil que responde en oraciones cortas y claras.",
)
