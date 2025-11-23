import os
import glob
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, classification_report
from django.conf import settings
from api.ml.preprocessor import leer_bandas

def train_model(ruta_carpeta_train, ruta_carpeta_test):
    """
    Trains the Random Forest model using images from the specified directories.
    Saves the trained model to the base directory.
    """
    print(f"Training started. Train dir: {ruta_carpeta_train}, Test dir: {ruta_carpeta_test}")
    
    imagenes_train = glob.glob(os.path.join(ruta_carpeta_train, "*.tif"))
    imagenes_test = glob.glob(os.path.join(ruta_carpeta_test, "*.tif"))

    if not imagenes_train:
        raise ValueError(f"No .tif images found in training directory: {ruta_carpeta_train}")

    # Parameters from original script
    valores_firma = {
        "nir": 0.11385695,
        "swir1": 0.094874144,
        "swir2": 0.052902829
    }

    def calcular_umbral(valor):
        return valor * 0.7, valor * 1.3

    umbrales = {banda: calcular_umbral(valor) for banda, valor in valores_firma.items()}

    X_total, y_total = [], []

    for ruta_imagen in imagenes_train:
        print(f"Processing training image: {os.path.basename(ruta_imagen)}")
        try:
            bandas, perfil, referencia_shape = leer_bandas(ruta_imagen)
        except Exception as e:
            print(f"Error reading {ruta_imagen}: {e}")
            continue

        # Create seed mask based on thresholds
        mascaras = {}
        for nombre in ['nir', 'swir1', 'swir2']:
            if nombre in bandas:
                umbral_inf, umbral_sup = umbrales[nombre]
                mascaras[nombre] = (bandas[nombre] >= umbral_inf) & (bandas[nombre] <= umbral_sup)

        if not mascaras:
            print(f"Skipping {ruta_imagen}: Missing required bands for mask generation.")
            continue

        mascara_semilla = np.zeros(referencia_shape, dtype=bool)
        for m in mascaras.values():
            mascara_semilla |= m

        caracteristicas = ['blue', 'green', 'red', 'nir', 'swir1']
        # Ensure all features exist
        valid_features = [b for b in caracteristicas if b in bandas]
        if len(valid_features) != len(caracteristicas):
             # If missing features, we might need to handle it or skip. 
             # For now, let's assume we need all of them or just use what we have, 
             # but the model expects specific features.
             # The original script just stacks what is available in 'caracteristicas'
             pass

        bandas_apiladas = np.dstack([bandas[b] for b in caracteristicas if b in bandas])

        # Class 1: Cienaga
        X_cienaga = bandas_apiladas[mascara_semilla]
        y_cienaga = np.ones(X_cienaga.shape[0], dtype=int)

        # Class 0: Non-Cienaga
        no_cienaga_idx = np.where(~mascara_semilla)
        # Handle case where there are no pixels for a class
        if X_cienaga.shape[0] == 0:
            print(f"No cienaga pixels found in {ruta_imagen}")
            continue
            
        num_no = min(X_cienaga.shape[0], len(no_cienaga_idx[0]))
        if num_no == 0:
             continue

        seleccion_no = np.random.choice(len(no_cienaga_idx[0]), num_no, replace=False)
        X_no = bandas_apiladas[no_cienaga_idx[0][seleccion_no],
                                no_cienaga_idx[1][seleccion_no], :]
        y_no = np.zeros(X_no.shape[0], dtype=int)

        X_total.append(np.vstack([X_cienaga, X_no]))
        y_total.append(np.concatenate([y_cienaga, y_no]))

    if not X_total:
        raise ValueError("No training data could be extracted from the images.")

    X = np.vstack(X_total)
    y = np.concatenate(y_total)

    print(f"Total samples: {X.shape[0]}, Features: {X.shape[1]}")

    # Train Random Forest
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X, y)
    print("Model trained successfully.")

    # Save Model
    model_path = os.path.join(settings.BASE_DIR, "modelo_rf_cienagas.pkl")
    joblib.dump(rf, model_path)
    print(f"Model saved to {model_path}")

    # Evaluation (Optional, if test images exist)
    metrics = {"model_path": model_path}
    if imagenes_test:
        # Logic to evaluate on test set could go here, 
        # but for now we just return success.
        pass

    return metrics
