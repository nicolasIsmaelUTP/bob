from fastapi import APIRouter
from ..services.conversation_service import ConversationService

router = APIRouter()

@router.get("/{wa_id}")
async def get_conversation_history(wa_id: str, limit: int = 10):
    history = ConversationService().get_conversation_history(wa_id, limit)
    return {"history": history}

@router.post("/{wa_id}")
async def send_message(wa_id: str, message: str):
    ConversationService().save_message(wa_id, "assistant", message)
    return {"status": "message saved"}
