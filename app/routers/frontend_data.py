from fastapi import APIRouter
from app.services.data_al_frontend import (
    obtener_leads_frontend,
    obtener_conversaciones_por_numero,
    obtener_historial_por_numero,
)

router = APIRouter(tags=["Frontend"])

@router.get("/leads")
def listar_leads(limit: int = 100):
    return obtener_leads_frontend(limit)

@router.get("/conversaciones")
def listar_conversaciones(limit: int = 50):
    return obtener_conversaciones_por_numero(limit)

@router.get("/conversaciones/{wa_id}/mensajes")
def historial_conversacion(wa_id: str, limit: int = 200):
    return obtener_historial_por_numero(wa_id, limit)
