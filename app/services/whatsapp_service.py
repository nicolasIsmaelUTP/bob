import requests

from ..config import Config

class WhatsAppService:
    async def send_message(self, to, message):
        url = f"https://graph.facebook.com/{Config.VERSION}/{Config.PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {Config.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        response = requests.post(url, headers=headers, json=data)
        return response