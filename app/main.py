import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Config
from .routers.whatsapp_webhook import router as whatsapp_router
from .routers.conversations import router as conversation_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Servidor de WhatsApp funcionando correctamente."}

app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(conversation_router, prefix="/conversations")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)