from ..database import get_supabase_client

class ConversationService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def save_message(self, wa_id: str, role: str, content: str):
        data = {
            "numero_whatsapp": wa_id,
            "tipo_emisor": role,
            "contenido": content
        }
        response = self.supabase.table("mensajes").insert(data).execute()
        return response
    
    def get_conversation_history(self, wa_id: str, limit: int = 10):
        response = (
            self.supabase
            .table("mensajes")
            .select("*")
            .eq("numero_whatsapp", wa_id)
            .order("fecha_creacion", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data

