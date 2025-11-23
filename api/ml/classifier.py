import os
import rasterio
import numpy as np
from api.ml.preprocessor import preprocess_image
from api.ml.model_loader import get_model

class ClassifierService:
    def predict(self, image_path):
        """
        Loads the model, preprocesses the image, and returns the classification result.
        """
        # 1. Load Model
        model = get_model()

        # 2. Preprocess Image
        X_pred, original_shape, perfil = preprocess_image(image_path)

        # 3. Predict
        y_pred = model.predict(X_pred)

        # 4. Reshape to original image dimensions
        classification_map = y_pred.reshape(original_shape)

        return classification_map, perfil

    def save_classification(self, classification_map, perfil, output_path):
        """
        Saves the classification result as a GeoTIFF.
        """
        # Update profile for the output
        perfil.update(dtype=rasterio.uint8, count=1)
        
        with rasterio.open(output_path, "w", **perfil) as dst:
            dst.write(classification_map.astype(rasterio.uint8), 1)
        
        return output_path
