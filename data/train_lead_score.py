import pandas as pd
import numpy as np
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

W_SCORE_PROMEDIO = 0.50
W_PREGUNTAS = 0.20
W_PRESUPUESTO = 0.10
W_SENTIMIENTO = 0.10
W_NUM_MENSAJES = 0.10

def obtener_mensajes():
    response = supabase.table("mensajes").select("*").execute()
    df = pd.DataFrame(response.data)
    if df.empty:
        raise ValueError("⚠️ No se encontraron mensajes en la tabla 'messages'.")
    return df

def calcular_score_msg(row):
    # valores de intención
    pesos_intencion = {"alta": 1.0, "media": 0.5, "baja": 0.1}
    peso = pesos_intencion.get(row.get("label_intencion"), 0.1)
    return row.get("score_msg", 0) * peso

def construir_dataset_leads(df_msgs):
    df_msgs["score_ponderado"] = df_msgs.apply(calcular_score_msg, axis=1)
    leads = []

    for lead_id, df_lead in df_msgs.groupby("lead_id"):
        data = {
            "lead_id": lead_id,
            "num_palabras": df_lead["num_palabras"].mean(),
            "num_preguntas": df_lead["num_preguntas"].mean(),
            "longitud": df_lead["longitud"].mean(),
            "score_promedio_msg": df_lead["score_ponderado"].mean(),
            "num_mensajes_total": df_lead.shape[0],
            "num_preguntas_total": df_lead["num_preguntas"].sum(),
            "mencion_presupuesto": int(df_lead["mensaje"].str.contains("presupuesto|precio|pagar", case=False).any()),
            "sentimiento_promedio": df_lead["sentimiento_num"].mean(),
        }
        leads.append(data)

    df_leads = pd.DataFrame(leads)
    return df_leads

def calcular_score_total(row):
    norm = lambda x: min(x / 10, 1)
    norm_sent = (row["sentimiento_promedio"] + 1) / 2
    return round(min(
        W_SCORE_PROMEDIO * row["score_promedio_msg"] +
        W_PREGUNTAS * norm(row["num_preguntas_total"]) +
        W_PRESUPUESTO * row["mencion_presupuesto"] +
        W_SENTIMIENTO * norm_sent +
        W_NUM_MENSAJES * norm(row["num_mensajes_total"]),
        1
    ), 3)

def clasificar_lead(score):
    if score >= 0.7:
        return "caliente"
    elif score >= 0.45:
        return "tibio"
    else:
        return "frio"

def pipeline_scoring():
    print("📥 Obteniendo mensajes desde Supabase...")
    df_msgs = obtener_mensajes()
    print(f"✅ {len(df_msgs)} mensajes obtenidos.")

    print("🧮 Calculando dataset de leads...")
    df_leads = construir_dataset_leads(df_msgs)

    print("⚙️ Calculando score total ponderado...")
    df_leads["score_total"] = df_leads.apply(calcular_score_total, axis=1)
    df_leads["label_pred"] = df_leads["score_total"].apply(clasificar_lead)

    print("\n🔥 Ejemplo de resultados:")
    print(df_leads[["lead_id", "score_promedio_msg", "score_total", "label_pred"]].head())

    print("\n💾 Subiendo resultados a Supabase...")
    for _, row in df_leads.iterrows():
        supabase.table("leads_scores").upsert({
            "lead_id": row["lead_id"],
            "score_total": row["score_total"],
            "categoria": row["label_pred"],
            "score_promedio_msg": row["score_promedio_msg"],
            "sentimiento_promedio": row["sentimiento_promedio"]
        }).execute()

    print(f"✅ {len(df_leads)} registros de leads actualizados en Supabase.")
    df_leads.to_csv("resultados_leads.csv", index=False)
    print("💾 Archivo local generado: resultados_leads.csv")

if __name__ == "__main__":
    pipeline_scoring()
