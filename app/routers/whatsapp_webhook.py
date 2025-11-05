import json

from fastapi import APIRouter, Request

from ..config import Config

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
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "ok"}