from ..database import get_supabase_client

class ConversationService:
    def __init__(self):
        self.supabase = get_supabase_client()

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

