# API de Entrenamiento del Modelo

## Configuración Completada ✅

### Carpetas Creadas
- **Train**: `~/Downloads/train` (30 imágenes .tif)
- **Test**: `~/Downloads/test` (30 imágenes .tif)

### Rutas por Defecto
Las rutas están configuradas en `settings.py`:
```python
ML_TRAIN_PATH = "~/Downloads/train"
ML_TEST_PATH = "~/Downloads/test"
```

## Uso del API REST

### Endpoint
```
POST http://localhost:8000/api/train/
```

### Opción 1: Usar rutas por defecto (más simple)
Envía un POST vacío o con JSON vacío:

```bash
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

O desde Python:
```python
import requests

response = requests.post('http://localhost:8000/api/train/')
print(response.json())
```

### Opción 2: Especificar rutas personalizadas
```bash
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{
    "train_path": "/ruta/personalizada/train",
    "test_path": "/ruta/personalizada/test"
  }'
```

O desde Python:
```python
import requests

data = {
    "train_path": "/ruta/personalizada/train",
    "test_path": "/ruta/personalizada/test"
}

response = requests.post('http://localhost:8000/api/train/', json=data)
print(response.json())
```

## Respuesta del API

### Éxito (200 OK)
```json
{
  "message": "Training completed successfully",
  "train_path": "/Users/andresgarcia/Downloads/train",
  "test_path": "/Users/andresgarcia/Downloads/test",
  "metrics": {
    "model_path": "/path/to/modelo_rf_cienagas.pkl"
  }
}
```

### Error (400 Bad Request)
```json
{
  "error": "Train path does not exist: /ruta/inexistente"
}
```

### Error (500 Internal Server Error)
```json
{
  "error": "Error message",
  "train_path": "/Users/andresgarcia/Downloads/train",
  "test_path": "/Users/andresgarcia/Downloads/test"
}
```

## Prueba Rápida

1. **Iniciar el servidor Django:**
   ```bash
   cd "/Users/andresgarcia/Library/Mobile Documents/com~apple~CloudDocs/Semestre/ImageAnalyzer"
   python manage.py runserver
   ```

2. **En otra terminal, probar el API:**
   ```bash
   curl -X POST http://localhost:8000/api/train/ \
     -H "Content-Type: application/json" \
     -d '{}'
   ```

3. **El modelo se guardará en:**
   ```
   /Users/andresgarcia/Library/Mobile Documents/com~apple~CloudDocs/Semestre/ImageAnalyzer/modelo_rf_cienagas.pkl
   ```

## Notas Importantes

- El entrenamiento puede tardar varios minutos dependiendo del número de imágenes
- Las imágenes deben ser archivos .tif con las bandas Sentinel-2
- El API valida que las carpetas existan antes de iniciar el entrenamiento
- Si no especificas rutas, usará automáticamente `~/Downloads/train` y `~/Downloads/test`
