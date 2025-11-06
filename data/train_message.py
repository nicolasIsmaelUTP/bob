import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_sample_weight
import xgboost as xgb
from xgboost import XGBClassifier
import joblib
import os

print("=" * 60)
print("🚀 ENTRENAMIENTO DEL MODELO DE CLASIFICACIÓN DE INTENCIÓN")
print("=" * 60)

# 1. Cargar dataset
print("\n📂 Cargando dataset...")
dataset_path = 'dataset_mensajes.json'

if not os.path.exists(dataset_path):
    print(f"❌ ERROR: No se encontró el archivo {dataset_path}")
    exit(1)

with open(dataset_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ Dataset cargado: {len(data)} registros")

# 2. Convertir a DataFrame
print("\n🔄 Convirtiendo a DataFrame...")
df_msg = pd.DataFrame(data)
print(f"✓ DataFrame creado: {df_msg.shape[0]} filas x {df_msg.shape[1]} columnas")

# 3. Preprocesamiento
print("\n🔧 Preprocesando datos...")

# Convertir sentimiento a valor numérico
sent_map = {'positivo': 1, 'neutro': 0, 'negativo': -1}
df_msg['sentimiento_num'] = df_msg['sentimiento'].map(sent_map)

# Contar número de palabras clave
df_msg['num_keywords'] = df_msg['palabras_clave'].apply(len)

print(f"✓ Sentimiento convertido a numérico")
print(f"✓ Número de palabras clave calculado")

# Verificar valores nulos
if df_msg['sentimiento_num'].isna().any():
    print("⚠️  ADVERTENCIA: Se encontraron valores nulos en sentimiento_num")
    df_msg['sentimiento_num'] = df_msg['sentimiento_num'].fillna(0)

# 4. Seleccionar features
features = [
    "num_palabras", "num_preguntas", "longitud", "sentimiento_num", "num_keywords"
]

print(f"\n📊 Features seleccionadas: {features}")

# Verificar que todas las features existan
for feat in features:
    if feat not in df_msg.columns:
        print(f"❌ ERROR: La feature '{feat}' no existe en el DataFrame")
        exit(1)

X = df_msg[features]
y = df_msg['label_intencion']

print(f"✓ Features shape: {X.shape}")
print(f"✓ Target shape: {y.shape}")

# Mostrar distribución de clases
print(f"\n📈 Distribución de clases:")
print(y.value_counts())
print(f"  - Alta: {(y == 'alta').sum()}")
print(f"  - Media: {(y == 'media').sum()}")
print(f"  - Baja: {(y == 'baja').sum()}")

# 5. Codificación de etiquetas
print("\n🏷️  Codificando etiquetas...")
le = LabelEncoder()
y_enc = le.fit_transform(y)
print(f"✓ Etiquetas codificadas: {le.classes_}")
print(f"  Mapeo: {dict(zip(le.classes_, range(len(le.classes_))))}")

# 6. Escalado de features
print("\n⚖️  Escalando features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(f"✓ Features escaladas (media=0, std=1)")

# 7. Balanceo de clases
print("\n⚖️  Calculando pesos para balanceo de clases...")
weights = compute_sample_weight("balanced", y_enc)
print(f"✓ Pesos calculados")

# 8. División train/test
print("\n✂️  Dividiendo en conjunto de entrenamiento y prueba...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

print(f"✓ Train: {X_train.shape[0]} muestras")
print(f"✓ Test: {X_test.shape[0]} muestras")

# Distribución en train
print(f"\n📊 Distribución en conjunto de entrenamiento:")
unique_train, counts_train = np.unique(y_train, return_counts=True)
for cls, cnt in zip(unique_train, counts_train):
    print(f"  - {le.classes_[cls]}: {cnt}")

# 9. Entrenar modelo
print("\n🤖 Entrenando modelo XGBoost...")
print("   (esto puede tomar unos momentos...)")

model = XGBClassifier(
    n_estimators=500,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1  # Usar todos los cores disponibles
)

model.fit(
    X_train, y_train, 
    sample_weight=weights[:len(y_train)],
    verbose=False
)

print(f"✓ Modelo entrenado exitosamente")

# 10. Predicciones
print("\n🔮 Generando predicciones...")
y_pred = model.predict(X_test)
print(f"✓ Predicciones generadas")

# 11. Evaluación
print("\n" + "=" * 60)
print("📊 REPORTE DE CLASIFICACIÓN")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=le.classes_))

print("\n" + "=" * 60)
print("📈 MATRIZ DE CONFUSIÓN")
print("=" * 60)
cm = confusion_matrix(y_test, y_pred)
print(cm)
print("\n(Matriz: filas=real, columnas=predicho)")

# Calcular accuracy
accuracy = (y_test == y_pred).mean()
print(f"\n✓ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

# 12. Importancia de features
print("\n" + "=" * 60)
print("🔥 IMPORTANCIA DE CADA FEATURE")
print("=" * 60)
importances = pd.DataFrame({
    "feature": features,
    "importancia": model.feature_importances_
}).sort_values(by="importancia", ascending=False)

print(importances.to_string(index=False))

# 13. Guardar modelo y preprocesadores
print("\n💾 Guardando modelo y preprocesadores...")

# Crear directorio de modelos si no existe
models_dir = 'models'
if not os.path.exists(models_dir):
    os.makedirs(models_dir)
    print(f"✓ Directorio '{models_dir}' creado")

model_path = os.path.join(models_dir, 'modelo_mensajes.joblib')
le_path = os.path.join(models_dir, 'label_encoder_msg.joblib')
scaler_path = os.path.join(models_dir, 'scaler_msg.joblib')

joblib.dump(model, model_path)
joblib.dump(le, le_path)
joblib.dump(scaler, scaler_path)

print(f"✓ Modelo guardado en: {model_path}")
print(f"✓ LabelEncoder guardado en: {le_path}")
print(f"✓ StandardScaler guardado en: {scaler_path}")

# 14. Guardar información adicional
info = {
    'features': features,
    'classes': le.classes_.tolist(),
    'accuracy': float(accuracy),
    'n_estimators': 500,
    'max_depth': 7,
    'learning_rate': 0.05,
    'train_size': int(X_train.shape[0]),
    'test_size': int(X_test.shape[0])
}

info_path = os.path.join(models_dir, 'model_info.json')
with open(info_path, 'w', encoding='utf-8') as f:
    json.dump(info, f, indent=2, ensure_ascii=False)

print(f"✓ Información del modelo guardada en: {info_path}")

