import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Config
from .routers.whatsapp_webhook import router as whatsapp_router
from .routers.conversations import router as conversation_router
from .routers.frontend_data import router as frontend_router  # 👈 NUEVO

app = FastAPI()

# 👇 CORS: permite llamadas desde tu frontend en Render y desde localhost
origins = [
    "https://bob-subastas-team-huachili-frontend.onrender.com",
    "http://localhost:5173",   # opcional: para desarrollo local de React
    "http://127.0.0.1:5173",   # opcional
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # antes tenías ["*"], ahora más seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Servidor de WhatsApp funcionando correctamente."}

# Rutas existentes (no se tocan)
app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(conversation_router, prefix="/conversations")

# 👇 NUEVO: endpoints para que el frontend consuma la data de Supabase
app.include_router(frontend_router, prefix="/frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
