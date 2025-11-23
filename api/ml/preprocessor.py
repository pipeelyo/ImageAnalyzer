import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

def resample_banda(banda_origen, perfil, referencia_shape):
    """
    Resample a band to match the reference shape.
    """
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
    """
    Reads bands from a multispectral image and returns them as a dictionary.
    Normalizes values by dividing by 10000.0.
    """
    with rasterio.open(ruta_imagen) as src:
        perfil = src.profile
        num_bandas = src.count
        referencia_shape = src.read(1).shape

        # Mapping based on the provided script
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

def preprocess_image(ruta_imagen):
    """
    Prepares the image data for prediction.
    Returns the flattened feature matrix (X_pred) and the original shape for reconstruction.
    """
    bandas, perfil, referencia_shape = leer_bandas(ruta_imagen)
    caracteristicas = ['blue', 'green', 'red', 'nir', 'swir1']

    bandas_nuevas = []
    for nombre in caracteristicas:
        if nombre in bandas:
            bandas_nuevas.append(bandas[nombre])
        else:
            # If a band is missing, fill with zeros (as per original script logic)
            bandas_nuevas.append(np.zeros(referencia_shape, dtype=np.float32))

    bandas_apil = np.dstack(bandas_nuevas)
    # Flatten for prediction: (pixels, features)
    X_pred = bandas_apil.reshape(-1, bandas_apil.shape[2])
    
    return X_pred, bandas_apil.shape[:2], perfil
