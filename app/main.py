import uvicorn

from fastapi import FastAPI

from .config import Config
from .routers.whatsapp_webhook import router as whatsapp_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Servidor de WhatsApp funcionando correctamente."}


app.include_router(whatsapp_router, prefix="/webhook")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)