import uvicorn
from fastapi import FastAPI, Request
from config import Config
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Servidor de WhatsApp funcionando correctamente."}

@app.get("/webhook")
async def verify_token(request: Request):
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == Config.VERIFY_TOKEN:
        return int(params["hub.challenge"])
    return "Error de verificación", 403

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)