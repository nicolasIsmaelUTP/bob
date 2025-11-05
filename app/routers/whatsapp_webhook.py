import json

from fastapi import APIRouter, Request

from ..config import Config
from ..services.gpt_agent import GPTAgent
from ..services.whatsapp_service import WhatsAppService

router = APIRouter()

@router.get("/")
async def verify_token(request: Request):
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == Config.VERIFY_TOKEN:
        return int(params["hub.challenge"])
    return "Error de verificación", 403

@router.post("/")
async def receive_message(request: Request):
    data = await request.json()
    # print(json.dumps(data, indent=2, ensure_ascii=False))
    change = data["entry"][0]["changes"][0]["value"]

    gpt_agent = GPTAgent()
    whatsapp_service = WhatsAppService()
    
    if "messages" in change:
        if "contacts" in change and "messages" in change:
            # Mensaje recibido del usuario
            sender = change["contacts"][0]["wa_id"]
            name = change["contacts"][0]["profile"]["name"]
            text = change["messages"][0]["text"]["body"]
            print(f"Mensaje recibido de {name} ({sender}): {text}")

            response_text = await gpt_agent.generate_response(text)
            await whatsapp_service.send_message(f"+{sender}", response_text)
    else:
        print("Evento no manejado:", data)

    return {"status": "ok"}