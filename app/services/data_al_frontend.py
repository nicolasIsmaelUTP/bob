from datetime import datetime, timezone
from typing import Any, Dict, List

from .conversation_service import ConversationService
from ..database import get_supabase_client  # o como lo tengas

supabase = get_supabase_client()


# Helpers de tiempo ---------------------------------------

def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def _texto_hace(dt: datetime | None) -> str:
    if dt is None:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = _ahora_utc() - dt
    mins = int(diff.total_seconds() // 60)
    horas = mins // 60
    dias = diff.days
    if mins < 1:
        return "hace unos segundos"
    if mins < 60:
        return f"hace {mins} m"
    if horas < 24:
        return f"hace {horas} h"
    return f"hace {dias} d"


# -------- LEADS (para la vista Leads + Dashboard) -----------------

def obtener_leads_frontend(limit: int = 100) -> List[Dict[str, Any]]:
    res = (
        supabase.table("clientes_potenciales")
        .select(
            "id, nombre_completo, telefono, correo, canal_origen, "
            "nivel_interes, puntaje_interes, "
            "fecha_creacion, fecha_ultimo_mensaje, resumen_ultimo_mensaje"
        )
        .order("fecha_ultimo_mensaje", desc=True)
        .limit(limit)
        .execute()
    )

    leads: List[Dict[str, Any]] = []

    for row in res.data or []:
        fecha_ultimo = (
            datetime.fromisoformat(row["fecha_ultimo_mensaje"])
            if row.get("fecha_ultimo_mensaje")
            else None
        )

        leads.append(
            {
                "id": row["id"],
                "name": row["nombre_completo"],
                "lastMessageTime": _texto_hace(fecha_ultimo),
                "interest": row.get("nivel_interes") or "Medio",
                "phone": row.get("telefono") or "",
                "message": row.get("resumen_ultimo_mensaje") or "",
                "tag": "Sin etiqueta",
                "channel": row.get("canal_origen") or "WhatsApp",
                "lastSeen": _texto_hace(fecha_ultimo),
                "daysAgo": 0,  # si quieres, calcula días como antes
            }
        )

    return leads


# -------- CONVERSACIONES (lista izquierda) -----------------------

def obtener_conversaciones_por_numero(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Lista de conversaciones agrupadas por número de WhatsApp,
    usando directamente la tabla mensajes (más simple para ahora).
    """
    res = (
        supabase.table("mensajes")
        .select("numero_whatsapp, contenido, fecha_creacion")
        .order("fecha_creacion", desc=True)
        .limit(limit)
        .execute()
    )

    conversaciones: Dict[str, Dict[str, Any]] = {}

    for row in res.data or []:
        wa_id = row["numero_whatsapp"]
        fecha = (
            datetime.fromisoformat(row["fecha_creacion"])
            if row.get("fecha_creacion")
            else None
        )
        if wa_id not in conversaciones:
            conversaciones[wa_id] = {
                "id": wa_id,  # usamos el número como id de conversación
                "leadId": wa_id,
                "leadName": wa_id,  # luego puedes cruzar con clientes_potenciales
                "phone": wa_id,
                "interest": "Medio",
                "lastMessageTime": _texto_hace(fecha),
                "lastMessagePreview": row.get("contenido", ""),
                "status": "Abierta",
                "unread": 0,
                "channel": "WhatsApp",
            }

    # devolver como lista
    return list(conversaciones.values())


# -------- HISTORIAL DE UNA CONVERSACIÓN -------------------------

def obtener_historial_por_numero(wa_id: str, limit: int = 200) -> List[Dict[str, Any]]:
    """
    Reusa tu ConversationService para obtener el historial y
    lo formatea para el frontend.
    """
    service = ConversationService()
    rows = service.get_conversation_history(wa_id=wa_id, limit=limit)

    mensajes: List[Dict[str, Any]] = []
    for m in rows:
        fecha = (
            datetime.fromisoformat(m["fecha_creacion"])
            if m.get("fecha_creacion")
            else None
        )
        mensajes.append(
            {
                "id": m["id"],
                "from": m.get("tipo_emisor", "cliente"),  # cliente | bot | agente
                "time": fecha.strftime("%H:%M") if fecha else "",
                "text": m.get("contenido", ""),
            }
        )

    return mensajes
