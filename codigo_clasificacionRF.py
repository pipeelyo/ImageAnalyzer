import os
import glob
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, classification_report
import joblib

# ===========================
# 1. PARÁMETROS INICIALES
# ===========================
ruta_carpeta_train = r"C:\Users\ricar\OneDrive\Documentos\ING SISTEMAS\PROYECTO GRADO\imagenes"
ruta_carpeta_test = r"C:\Users\ricar\OneDrive\Documentos\ING SISTEMAS\PROYECTO GRADO\imagencla"

imagenes_train = glob.glob(os.path.join(ruta_carpeta_train, "*.tif"))
imagenes_test = glob.glob(os.path.join(ruta_carpeta_test, "*.tif"))

valores_firma = {
    "nir": 0.11385695,
    "swir1": 0.094874144,
    "swir2": 0.052902829
}

# Umbral ±30%
def calcular_umbral(valor):
    return valor * 0.7, valor * 1.3  # 30% por debajo y 30% por encima

umbrales = {banda: calcular_umbral(valor) for banda, valor in valores_firma.items()}

# ===========================
# 2. FUNCIONES AUXILIARES
# ===========================
def resample_banda(banda_origen, perfil, referencia_shape):
    banda_resample = np.empty(referencia_shape, dtype=banda_origen.dtype)
    reproject(
        source=banda_origen,
        destination=banda_resample,
        src_transform=perfil['transform'],
        src_crs=perfil['crs'],
        dst_transform=perfil['transform'],
        dst_crs=perfil['crs'],
        resampling=Resampling.bilinear
    )
    return banda_resample

def leer_bandas(ruta_imagen):
    with rasterio.open(ruta_imagen) as src:
        perfil = src.profile
        num_bandas = src.count
        referencia_shape = src.read(1).shape

        bandas_disponibles = {}
        if num_bandas >= 1: bandas_disponibles['blue'] = 1
        if num_bandas >= 2: bandas_disponibles['green'] = 2
        if num_bandas >= 3: bandas_disponibles['red'] = 3
        if num_bandas >= 7: bandas_disponibles['nir'] = 7
        if num_bandas >= 9: bandas_disponibles['swir1'] = 9
        if num_bandas >= 10: bandas_disponibles['swir2'] = 10

        bandas = {}
        for nombre, idx in bandas_disponibles.items():
            banda = src.read(idx).astype(np.float32) / 10000.0
            if banda.shape != referencia_shape:
                banda = resample_banda(banda, perfil, referencia_shape)
            bandas[nombre] = banda

    return bandas, perfil, referencia_shape

# ===========================
# 3. EXTRAER MUESTRAS
# ===========================
X_total, y_total = [], []

for ruta_imagen in imagenes_train:
    print(f"📂 Procesando: {os.path.basename(ruta_imagen)}")
    bandas, perfil, referencia_shape = leer_bandas(ruta_imagen)

    # Crear máscara semilla según umbrales
    mascaras = {}
    for nombre in ['nir', 'swir1', 'swir2']:
        if nombre in bandas:
            umbral_inf, umbral_sup = umbrales[nombre]
            mascaras[nombre] = (bandas[nombre] >= umbral_inf) & (bandas[nombre] <= umbral_sup)

    mascara_semilla = np.zeros(referencia_shape, dtype=bool)
    for m in mascaras.values():
        mascara_semilla |= m

    caracteristicas = ['blue', 'green', 'red', 'nir', 'swir1']
    bandas_apiladas = np.dstack([bandas[b] for b in caracteristicas if b in bandas])

    # Clases cienaga = 1
    X_cienaga = bandas_apiladas[mascara_semilla]
    y_cienaga = np.ones(X_cienaga.shape[0], dtype=int)

    # Clases no-ciénaga = 0
    no_cienaga_idx = np.where(~mascara_semilla)
    num_no = min(X_cienaga.shape[0], len(no_cienaga_idx[0]))
    seleccion_no = np.random.choice(len(no_cienaga_idx[0]), num_no, replace=False)
    X_no = bandas_apiladas[no_cienaga_idx[0][seleccion_no],
                            no_cienaga_idx[1][seleccion_no], :]
    y_no = np.zeros(X_no.shape[0], dtype=int)

    X_total.append(np.vstack([X_cienaga, X_no]))
    y_total.append(np.concatenate([y_cienaga, y_no]))

X = np.vstack(X_total)
y = np.concatenate(y_total)

print(f"✅ Total muestras: {X.shape[0]}, características: {X.shape[1]}")
print(f"Distribución de clases: {np.bincount(y)}")

# ===========================
# 4. SPLIT 70%-30% PARA EVALUACIÓN
# ===========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# ===========================
# 5. ENTRENAR RANDOM FOREST
# ===========================
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)
print("✅ Modelo Random Forest entrenado correctamente")

# Guardar modelo
joblib.dump(rf, "modelo_rf_cienagas.pkl")
print("💾 Modelo guardado como 'modelo_rf_cienagas.pkl'")

# ===========================
# 6. FUNCION PARA CLASIFICAR IMÁGENES NUEVAS
# ===========================
def clasificar_imagen(ruta_imagen, modelo):
    bandas, perfil, referencia_shape = leer_bandas(ruta_imagen)
    caracteristicas = ['blue', 'green', 'red', 'nir', 'swir1']

    bandas_nuevas = []
    for nombre in caracteristicas:
        if nombre in bandas:
            bandas_nuevas.append(bandas[nombre])
        else:
            bandas_nuevas.append(np.zeros(referencia_shape, dtype=np.float32))

    bandas_apil = np.dstack(bandas_nuevas)
    X_pred = bandas_apil.reshape(-1, bandas_apil.shape[2])
    y_pred = modelo.predict(X_pred)
    clasificacion = y_pred.reshape(bandas_apil.shape[:2])

    # Guardar GeoTIFF
    salida = os.path.splitext(os.path.basename(ruta_imagen))[0] + "_clasificacion.tif"
    ruta_salida = os.path.join(ruta_carpeta_test, salida)
    perfil.update(dtype=rasterio.uint8, count=1)
    with rasterio.open(ruta_salida, "w", **perfil) as dst:
        dst.write(clasificacion.astype(rasterio.uint8), 1)

    print(f"🗺️ Clasificación guardada: {ruta_salida}")
    return clasificacion

# ===========================
# 7. APLICAR MODELO A TODAS LAS IMÁGENES TEST
# ===========================
rf = joblib.load("modelo_rf_cienagas.pkl")
ultima_clasificacion = None

for ruta_img in imagenes_test:
    print(f"\n🔍 Clasificando imagen: {os.path.basename(ruta_img)}")
    ultima_clasificacion = clasificar_imagen(ruta_img, rf)

# ===========================
# 8. MOSTRAR ÚLTIMA IMAGEN (COLOR VERDADERO + CLASIFICACIÓN)
# ===========================
if ultima_clasificacion is not None:
    # Mostrar color verdadero (RGB) con estiramiento lineal por percentiles
    bandas, perfil, referencia_shape = leer_bandas(ruta_img)
    rgb = np.dstack([bandas[b] for b in ['red', 'green', 'blue']])

    # Estiramiento lineal por percentiles 0.5-99.5
    rgb_stretch = np.zeros_like(rgb)
    for i in range(3):
        p_low, p_high = np.percentile(rgb[:, :, i], [0.5, 99.5])
        rgb_stretch[:, :, i] = np.clip((rgb[:, :, i] - p_low) / (p_high - p_low), 0, 1)

    plt.figure(figsize=(8, 8))
    plt.imshow(rgb_stretch)
    plt.title("Última imagen en color verdadero")
    plt.axis("off")
    plt.show()

    # Mostrar clasificación final
    plt.figure(figsize=(8, 8))
    plt.imshow(ultima_clasificacion, cmap="coolwarm")
    plt.title("Última imagen clasificada")
    plt.axis("off")
    plt.show()

# ===========================
# 9. CALCULAR Y MOSTRAR RECALL FINAL
# ===========================
y_pred_test = rf.predict(X_test)
recall = recall_score(y_test, y_pred_test, average='binary')
print(f"\n🎯 Recall final en conjunto de prueba: {recall:.4f}")
print("\n📊 Reporte de clasificación completo:")
print(classification_report(y_test, y_pred_test))

print("\n🎯 Proceso completo finalizado con éxito.")
