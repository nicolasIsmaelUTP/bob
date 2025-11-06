import json
import pandas as pd
import joblib
import os
import sys

def calcular_sentimiento(texto):
    texto_clean = texto.lower()
    
    palabras_positivas = ["confirmar", "confirmen", "listo", "completado", "realizado", "realicé", 
                         "deseo", "quiero", "interesado", "participar", "ofertar", "he completado",
                         "he realizado", "ya pagué", "ya hice", "ya envié", "ya completé",
                         "estoy listo", "necesito confirmar", "deseo participar"]
    
    palabras_negativas = ["aún no", "todavía no", "no estoy", "no tengo", "no puedo", 
                         "no quiero", "no me interesa", "cancelar", "desistir", "no estoy seguro",
                         "no he decidido", "no tengo claro", "tal vez", "solo estoy", "solo quería"]
    
    count_pos = sum(1 for palabra in palabras_positivas if palabra in texto_clean)
    count_neg = sum(1 for palabra in palabras_negativas if palabra in texto_clean)
    
    if count_pos > count_neg and count_pos > 0:
        return "positivo"
    elif count_neg > count_pos and count_neg > 0:
        return "negativo"
    elif "?" in texto:
        return "neutro"
    elif any(palabra in texto_clean for palabra in ["solo", "tal vez", "aún", "todavía"]):
        return "negativo"
    elif any(palabra in texto_clean for palabra in ["confirmar", "listo", "completado", "participar"]):
        return "positivo"
    else:
        return "neutro"

def extraer_palabras_clave(texto):
    """Extrae palabras clave del texto"""
    PALABRAS_CLAVE = [
        "pago", "garantía", "voucher", "transferencia", "depósito", "confirmar",
        "subasta", "lote", "ofertar", "participar", "registro", "financiamiento",
        "plataforma", "asesor", "precio", "resultado", "comprobante", "visita"
    ]
    
    texto_lower = texto.lower()
    palabras_encontradas = [p for p in PALABRAS_CLAVE if p in texto_lower]
    return palabras_encontradas

def preprocesar_mensaje(mensaje):
    """Preprocesa un mensaje para el modelo"""
    sent_map = {'positivo': 1, 'neutro': 0, 'negativo': -1}
    
    sentimiento = calcular_sentimiento(mensaje)
    num_palabras = len(mensaje.split())
    num_preguntas = mensaje.count("?")
    longitud = len(mensaje)
    palabras_clave = extraer_palabras_clave(mensaje)
    num_keywords = len(palabras_clave)
    sentimiento_num = sent_map.get(sentimiento, 0)
    
    return {
        'num_palabras': num_palabras,
        'num_preguntas': num_preguntas,
        'longitud': longitud,
        'sentimiento_num': sentimiento_num,
        'num_keywords': num_keywords,
        'sentimiento': sentimiento,
        'palabras_clave': palabras_clave
    }

def predecir_intencion(mensaje, model_path='models/modelo_mensajes.joblib', 
                       scaler_path='models/scaler_msg.joblib',
                       le_path='models/label_encoder_msg.joblib'):
    """
    Predice la intención de un mensaje
    
    Args:
        mensaje: Texto del mensaje a clasificar
        model_path: Ruta al modelo entrenado
        scaler_path: Ruta al scaler
        le_path: Ruta al label encoder
    
    Returns:
        dict con la predicción y probabilidades
    """
    # Verificar que los archivos existan
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el modelo en {model_path}. Ejecuta primero: python train_model.py")
    
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"No se encontró el scaler en {scaler_path}")
    
    if not os.path.exists(le_path):
        raise FileNotFoundError(f"No se encontró el label encoder en {le_path}")
    
    # Cargar modelo y preprocesadores
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    le = joblib.load(le_path)
    
    # Preprocesar mensaje
    features_dict = preprocesar_mensaje(mensaje)
    
    # Extraer features numéricas
    features = [
        features_dict['num_palabras'],
        features_dict['num_preguntas'],
        features_dict['longitud'],
        features_dict['sentimiento_num'],
        features_dict['num_keywords']
    ]
    
    # Escalar
    X_scaled = scaler.transform([features])
    
    # Predecir
    prediccion = model.predict(X_scaled)[0]
    probabilidades = model.predict_proba(X_scaled)[0]
    
    # Mapear a etiquetas
    intencion = le.inverse_transform([prediccion])[0]
    
    # Crear diccionario de probabilidades
    prob_dict = {cls: prob for cls, prob in zip(le.classes_, probabilidades)}
    
    return {
        'mensaje': mensaje,
        'intencion': intencion,
        'probabilidades': prob_dict,
        'caracteristicas': features_dict
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PRUEBA DEL MODELO DE CLASIFICACIÓN")
    print("=" * 60)
    
    # Mensajes de prueba
    mensajes_prueba = [
        "Ya hice el pago de la garantía, por favor confirmen",
        "¿Cuál es el costo para participar?",
        "Solo estoy revisando los lotes",
        "He completado el registro y el depósito, ¿pueden confirmar?",
        "Me interesa participar, ¿qué debo hacer?",
        "Tal vez más adelante participe",
        "Estoy listo para ofertar en el lote número 5",
        "Aún no estoy decidido",
    ]
    
    print("\n🔍 Probando con mensajes de ejemplo:\n")
    
    for i, mensaje in enumerate(mensajes_prueba, 1):
        try:
            resultado = predecir_intencion(mensaje)
            
            print(f"{'='*60}")
            print(f"Mensaje {i}: {mensaje}")
            print(f"{'='*60}")
            print(f"📊 Intención predicha: {resultado['intencion'].upper()}")
            print(f"\n📈 Probabilidades:")
            for intencion, prob in sorted(resultado['probabilidades'].items(), 
                                         key=lambda x: x[1], reverse=True):
                barra = "█" * int(prob * 50)
                print(f"   {intencion:6s}: {prob:.3f} {barra}")
            
            print(f"\n🔧 Características:")
            print(f"   - Palabras: {resultado['caracteristicas']['num_palabras']}")
            print(f"   - Preguntas: {resultado['caracteristicas']['num_preguntas']}")
            print(f"   - Longitud: {resultado['caracteristicas']['longitud']}")
            print(f"   - Sentimiento: {resultado['caracteristicas']['sentimiento']}")
            print(f"   - Palabras clave: {resultado['caracteristicas']['palabras_clave']}")
            print()
            
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}\n")
    
    # Modo interactivo
    print("\n" + "=" * 60)
    print("💬 MODO INTERACTIVO")
    print("=" * 60)
    print("Escribe mensajes para clasificar (o 'salir' para terminar):\n")
    
    while True:
        try:
            mensaje = input("> ").strip()
            if mensaje.lower() in ['salir', 'exit', 'quit']:
                break
            
            if not mensaje:
                continue
            
            resultado = predecir_intencion(mensaje)
            
            print(f"\n📊 Intención: {resultado['intencion'].upper()}")
            print(f"📈 Probabilidades:")
            for intencion, prob in sorted(resultado['probabilidades'].items(), 
                                         key=lambda x: x[1], reverse=True):
                print(f"   {intencion}: {prob:.1%}")
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

