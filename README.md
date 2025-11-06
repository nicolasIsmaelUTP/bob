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

## � Ejemplos de Conversaciones

A continuación se presentan 3 casos de uso reales para probar la funcionalidad del bot:

### Caso 1: Cliente empresario buscando vehículo comercial

**Historia:** *Carlos es dueño de una pequeña empresa de reparto en Lima y necesita un vehículo comercial económico para expandir su negocio.*

```
👤 Usuario: Hola, necesito un vehículo comercial para mi negocio de reparto

🤖 BOB: ¡Hola! Encantado de ayudarte. Tenemos varias opciones de vehículos 
comerciales en subasta. ¿Qué tipo de vehículo buscas específicamente? 
(furgón, camioneta, minivan)

👤 Usuario: Un furgón pequeño, algo económico

🤖 BOB: Perfecto, tengo estas opciones:
- CHEVROLET N400 (P4D443): USD 6,720 - Piura, 183,585 km, 2023
- DFSK K07S (BZD672): USD 3,900 - Lima, 102,110 km, 2021
- SUZUKI APV FURGON (BUA710): USD 7,200 - Ica, 16,366 km, 2022

👤 Usuario: Me interesa el DFSK. ¿Cómo funciona el proceso?

🤖 BOB: ¡Excelente elección! El proceso es simple:
1. Regístrate en https://www.somosbob.com/registro
2. No necesitas pagar para participar
3. Si ganas, pagas 8% de garantía y luego el 92% restante
4. Entrega en 5-10 días
¿Tienes alguna pregunta sobre el proceso?

👤 Usuario: ¿Puedo verlo antes de ofertar?

🤖 BOB: Sí, puedes coordinar una visita previa. Te contactaremos con un 
asesor para agendar la inspección. Deberás cumplir con requisitos de 
seguridad (SCTR y EPPS).
```

### Caso 2: Comprador frecuente consultando sobre Pacífico Seguros

**Historia:** *María es una revendedora con experiencia que ya ha participado en subastas de BOB, pero es su primera vez con Pacífico Seguros.*

```
👤 Usuario: Hola, vi una moto Honda en Pacífico Seguros. ¿Es igual que las 
otras subastas?

🤖 BOB: Hola María, las subastas de Pacífico Seguros tienen algunas 
diferencias importantes:
- Requieren oblaje de USD 300 como derecho de participación
- Debes llenar un formulario adicional
- Puedes visitar los vehículos de miércoles a viernes de 9am a 1pm

👤 Usuario: ¿Y si no gano, pierdo los USD 300?

🤖 BOB: No, si no ganas puedes solicitar la devolución íntegra del oblaje. 
Si ganas, ese monto se descuenta de la garantía del 8%.

👤 Usuario: Perfecto. ¿Cuál es la Honda disponible?

🤖 BOB: Tenemos:
- HONDA GLH150 (7895RC): USD 1,086.96 - Cajamarquilla, 2024, con garantía

👤 Usuario: ¿Cómo coordino la visita?

🤖 BOB: Te conectaré con un asesor para que agendes tu visita entre 
miércoles y viernes de 9am a 1pm. ¿Qué día prefieres?
```

### Caso 3: Primer usuario explorando opciones y pagos

**Historia:** *José es mecánico y quiere comprar su primer vehículo en subasta para repararlo y revenderlo, pero tiene dudas sobre transparencia y pagos.*

```
👤 Usuario: ¿Qué es BOB?

🤖 BOB: BOB Subastas es una plataforma online que ayuda a las empresas a 
vender sus activos en desuso mediante subastas transparentes y seguras. 
Hemos realizado más de 748 subastas exitosas y fuimos reconocidos por 
Forbes como una de las 100 mejores startups del Perú.

👤 Usuario: ¿Cómo sé que no están arregladas las subastas?

🤖 BOB: Excelente pregunta. Garantizamos transparencia así:
- Todas las ofertas están encriptadas con fecha/hora
- Los nombres de los postores están ocultos
- El sistema determina al ganador automáticamente
- Gana siempre la oferta válida más alta
- Si detectamos intentos de arreglo, bloqueamos al participante

👤 Usuario: Ok, me interesa. Tengo USD 5,000. ¿Qué puedo comprar?

🤖 BOB: Con ese presupuesto tienes varias opciones:
- CHEVROLET ONIX (Z7C108): USD 4,200 - Lima, 2022
- CHANGAN CS15 (P4D508): USD 5,100 - Piura, 63,235 km, 2023
- KIA SOLUTO (T5W378): USD 5,400 - Trujillo, 68,072 km, 2021

👤 Usuario: ¿Cuánto tengo que pagar si gano?

🤖 BOB: Si ganas:
1. Depositas 8% como garantía (ej: USD 336 para el Chevrolet)
2. Pagas el 92% restante al vendedor (ej: USD 3,864)
3. La garantía se convierte en comisión de BOB
Todo por transferencia bancaria, sin pagos adicionales.

👤 Usuario: ¿Y si compro, puedo revenderlo?

🤖 BOB: ¡Claro! Muchos de nuestros participantes compran para revender y 
generar ingresos. Es una práctica totalmente permitida.
```

## �📞 Soporte

Para más información sobre la configuración de WhatsApp Business API, consulta la [documentación oficial](https://developers.facebook.com/docs/whatsapp).

## 📄 Licencia

Ver archivo `LICENSE` para más detalles.