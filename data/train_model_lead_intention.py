# ============================================================
# - Modelo 2: Scoring de leads agregados
# ============================================================

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import joblib

# === Cargar datasets ===
df_lead = pd.read_json('dataset_leads.json')

# ============================================================
# 🧮 MODELO 2: Scoring de leads
# ============================================================

# Pesos por parámetro (ajustables)
w_score_promedio = 0.5
w_preguntas = 0.2
w_presupuesto = 0.1
w_sentimiento = 0.1
w_num_mensajes = 0.1

def calcular_score_lead(row):
    norm = lambda x: min(x / 10, 1)
    return (
        w_score_promedio * row['score_promedio_msg'] +
        w_preguntas * norm(row['num_preguntas_total']) +
        w_presupuesto * row['mencion_presupuesto'] +
        w_sentimiento * ((row['sentimiento_promedio'] + 1) / 2) +
        w_num_mensajes * norm(row['num_mensajes_total'])
    )

df_lead['score_total'] = df_lead.apply(calcular_score_lead, axis=1)
df_lead['label_pred'] = pd.cut(df_lead['score_total'],
                               bins=[0,0.4,0.7,1],
                               labels=['frío','tibio','caliente'])

print('\n🔥 Scoring de leads (ejemplo):')
print(df_lead[['lead_id','score_total','label_lead','label_pred']])

# Guardar
df_lead.to_csv('resultados_leads.csv', index=False)
print('\n💾 Archivos generados: modelo_mensajes.joblib, resultados_leads.csv')
