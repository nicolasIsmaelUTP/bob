# Bob - WhatsApp Assistant Bot

Bot asistente inteligente para WhatsApp que utiliza IA para responder preguntas y gestionar conversaciones.

## 🚀 Inicio Rápido

### Opción 1: Ejecutable automático (Windows)

Simplemente haz doble clic en el archivo `start.bat` o ejecuta en PowerShell:

```powershell
.\setup.ps1
```

Este script automáticamente:
- ✅ Crea el entorno virtual
- ✅ Activa el entorno virtual
- ✅ Verifica el archivo .env
- ✅ Instala las dependencias
- ✅ Levanta el servidor FastAPI

### Opción 2: Configuración manual

#### 1. Crear entorno virtual

```powershell
python -m venv venv
```

#### 2. Activar entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

#### 3. Configurar variables de entorno

Copia el archivo `.env.example` a `app\.env` y completa las variables:

```powershell
Copy-Item .env.example app\.env
```

Edita `app\.env` con tus credenciales:
- `VERSION`: Versión de la aplicación
- `PHONE_NUMBER_ID`: ID del número de teléfono de WhatsApp Business
- `RECIPIENT_PHONE_NUMBER`: Número de destinatario
- `ACCESS_TOKEN`: Token de acceso de WhatsApp Business API
- `OPENAI_API_KEY`: Clave API de OpenAI
- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_SERVICE_ROLE`: Clave de servicio de Supabase

#### 4. Instalar dependencias

```powershell
pip install -r app/requirements.txt
```

#### 5. Levantar el servicio

```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en: `http://localhost:8000`

#### 6. Exponer con ngrok (para webhooks de WhatsApp)

En una terminal separada, ejecuta:

```powershell
ngrok http 8000
```

Copia la URL HTTPS que ngrok genera (ej: `https://xxxx-xx-xxx-xxx-xx.ngrok-free.app`) y úsala para configurar el webhook en WhatsApp Business API.

## 📁 Estructura del Proyecto

```
bob/
├── app/
│   ├── agents/              # Agentes de IA
│   │   └── assistant_agent.py
│   ├── prompts/             # Prompts del sistema
│   ├── routers/             # Endpoints de la API
│   │   ├── conversations.py
│   │   └── whatsapp_webhook.py
│   ├── services/            # Servicios del negocio
│   │   ├── conversation_service.py
│   │   ├── message_handler.py
│   │   └── whatsapp_service.py
│   ├── tools/               # Herramientas del agente
│   │   ├── faq_tool.py
│   │   └── product_tool.py
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión a BD
│   ├── main.py              # Aplicación principal
│   └── requirements.txt     # Dependencias
├── data/                    # Datos del proyecto
├── notebooks/               # Jupyter notebooks
└── .env.example             # Ejemplo de variables de entorno
```

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **OpenAI**: Inteligencia artificial para el asistente
- **LangChain**: Framework para aplicaciones con LLM
- **Supabase**: Base de datos y autenticación
- **WhatsApp Business API**: Integración con WhatsApp
- **Uvicorn**: Servidor ASGI de alto rendimiento

## 📝 Endpoints Disponibles

- `GET /`: Verificación del servidor
- `GET /webhook`: Verificación del webhook de WhatsApp
- `POST /webhook`: Recepción de mensajes de WhatsApp
- `GET /conversations`: Obtener conversaciones

## 🔧 Requisitos

- Python 3.8 o superior
- Cuenta de WhatsApp Business API
- Cuenta de OpenAI con API key
- Proyecto de Supabase
- ngrok (para desarrollo local)

## 📞 Soporte

Para más información sobre la configuración de WhatsApp Business API, consulta la [documentación oficial](https://developers.facebook.com/docs/whatsapp).

## 📄 Licencia

Ver archivo `LICENSE` para más detalles.