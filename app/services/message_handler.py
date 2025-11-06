from typing import Dict, Any
from .gpt_agent import GPTAgent
from .whatsapp_service import WhatsAppService
from .conversation_service import ConversationService

class MessageHandler:
    def __init__(self):
        self.gpt_agent = GPTAgent()
        self.whatsapp_service = WhatsAppService()
        self.conversation_service = ConversationService()

    async def process_webhook_event(self, data: Dict[str, Any]) -> None:
        try:
            change = data["entry"][0]["changes"][0]["value"]
            
            if "messages" in change and "contacts" in change:
                self.conversation_service.save_message(
                    change["contacts"][0]["wa_id"],
                    "user",
                    change["messages"][0]["text"]["body"]
                )
                await self._handle_incoming_message(change)
            else:
                print("Evento no manejado")
                
        except (KeyError, IndexError) as e:
            print(f"Error al procesar el webhook: {e}")
            print(f"Datos recibidos: {data}")

    async def _handle_incoming_message(self, change: Dict[str, Any]) -> None:
        try:
            sender = change["contacts"][0]["wa_id"]
            name = change["contacts"][0]["profile"]["name"]
            text = change["messages"][0]["text"]["body"]
            
            print(f"Mensaje recibido de {name} ({sender}): {text}")

            # Generar respuesta con GPT
            context_history = self.conversation_service.get_conversation_history(sender)
            history_texts = "\n".join(f"{msg['sender_type']}: {msg['content']}" for msg in reversed(context_history))
            prompt = f"Contexto de la conversación:\n{history_texts}\nassistant:"
            print(f"Generando respuesta con el siguiente prompt:\n{prompt}")

            response_text = await self.gpt_agent.generate_response(prompt)

            self.conversation_service.save_message(
                sender,
                "assistant",
                response_text
            )

            # Enviar respuesta por WhatsApp
            await self.whatsapp_service.send_message(f"+{sender}", response_text)

            print(f"Mensaje enviado a {name} ({sender}): {response_text}")
            
        except (KeyError, IndexError) as e:
            print(f"Error al procesar mensaje: {e}")
        except Exception as e:
            print(f"Error inesperado al manejar mensaje: {e}")
