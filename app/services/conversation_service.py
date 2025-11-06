from supabase import create_client, Client
from ..config import Config

class ConversationService:
    supabase: Client = create_client(
        Config.SUPABASE_URL,
        Config.SUPABASE_SERVICE_ROLE
    )

    def __init__(self):
        pass

    def save_message(self, wa_id: str, role: str, content: str):
        data = {
            "wa_id": wa_id,
            "sender_type": role,
            "content": content
        }
        response = self.supabase.table("messages").insert(data).execute()
        return response
    
    def get_conversation_history(self, wa_id: str, limit: int = 10):
        response = (
            self.supabase
            .table("messages")
            .select("*")
            .eq("wa_id", wa_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data

