import joblib
import os
from django.conf import settings

class ModelLoader:
    _instance = None
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_model(self):
        if self._model is None:
            # TODO: Update this path when the user provides the model file
            model_path = os.path.join(settings.BASE_DIR, 'modelo_rf_cienagas.pkl')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}. Please upload the model file.")
            
            print(f"Loading model from {model_path}...")
            self._model = joblib.load(model_path)
            print("Model loaded successfully.")
        return self._model

def get_model():
    return ModelLoader.get_instance().load_model()
