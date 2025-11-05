from openai import OpenAI
from ..config import Config

class GPTAgent:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-5-mini-2025-08-07",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
