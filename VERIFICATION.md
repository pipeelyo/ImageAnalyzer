# Verificación del Sistema ImageAnalyzer

## Estado de Verificación

### ✅ Componentes Verificados

1. **Modelo ML**
   - ✅ Modelo `modelo_rf_cienagas.pkl` existe en la raíz del proyecto
   - ✅ ModelLoader configurado correctamente
   - ✅ Ruta del modelo configurada en `api/ml/model_loader.py`

2. **Backend ML**
   - ✅ `preprocessor.py`: Preprocesamiento de imágenes con bandas Sentinel-2
   - ✅ `model_loader.py`: Carga del modelo con patrón Singleton
   - ✅ `classifier.py`: Servicio de clasificación completo
   - ✅ `trainer.py`: Entrenamiento del modelo con Random Forest

3. **Comandos CLI**
   - ✅ `train_model_cli`: Comando para entrenar el modelo
   - ✅ `test_model`: Comando para probar el modelo con imágenes

4. **Interfaz Web**
   - ✅ Template `upload.html`: Formulario de carga con manejo de errores
   - ✅ Template `result.html`: Visualización de resultados
   - ✅ Vista `AnalyzeImageView`: Procesamiento de imágenes con visualización

5. **API REST**
   - ✅ Endpoint `/api/train/`: Entrenamiento del modelo
   - ✅ Endpoint `/api/analyze/`: Análisis de imágenes (GET y POST)

6. **Configuración**
   - ✅ URLs configuradas correctamente
   - ✅ Media files configurados
   - ✅ Matplotlib configurado con backend no interactivo

### 🔄 Pasos para Verificación End-to-End

#### 1. Iniciar el Servidor

```bash
cd C:\Users\J14Z\Documents\FELIPE\ImageAnalyzer
python manage.py runserver
```

El servidor debería iniciar en `http://localhost:8000`

#### 2. Acceder a la Interfaz Web

Navegar a: `http://localhost:8000/api/analyze/`

Deberías ver el formulario de carga de imágenes.

#### 3. Probar con una Imagen

1. Hacer clic en "Choose File"
2. Seleccionar una imagen .tif del directorio de test:
   - `C:\Users\J14Z\Documents\FELIPE\Images\test`
3. Hacer clic en "Analyze"
4. Verificar que se muestre el mapa de clasificación

#### 4. Probar con Comando CLI

```bash
# Probar con una imagen específica
python manage.py test_model --image "C:\Users\J14Z\Documents\FELIPE\Images\test\imagen.tif"

# Probar y guardar resultado
python manage.py test_model --image "C:\Users\J14Z\Documents\FELIPE\Images\test\imagen.tif" --output "resultado.tif"
```

#### 5. Probar API REST

**Entrenar modelo:**
```bash
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{"train_path": "C:\\ruta\\a\\imagenes\\train"}'
```

**Analizar imagen (usando Python requests):**
```python
import requests

url = "http://localhost:8000/api/analyze/"
files = {'image': open('imagen.tif', 'rb')}
response = requests.post(url, files=files)
print(response.status_code)
```

### ⚠️ Posibles Problemas y Soluciones

1. **Error: "Model file not found"**
   - Solución: Asegúrate de que `modelo_rf_cienagas.pkl` existe en la raíz
   - Si no existe, entrena el modelo primero

2. **Error: "No module named 'rasterio'"**
   - Solución: `pip install rasterio`

3. **Error: "No .tif images found"**
   - Solución: Verifica que las imágenes estén en formato .tif
   - Verifica que la ruta sea correcta (usar rutas absolutas en Windows)

4. **Error al procesar imagen**
   - Verifica que la imagen tenga al menos 7 bandas (para NIR)
   - Verifica que la imagen esté en formato GeoTIFF válido

5. **Error de matplotlib en servidor**
   - Ya configurado: `matplotlib.use('Agg')` en `views_ui.py`

### 📝 Notas de Validación

- El modelo espera imágenes con valores normalizados (divididos por 10000.0)
- El preprocesador busca bandas en índices específicos:
  - Banda 1: Blue
  - Banda 2: Green
  - Banda 3: Red
  - Banda 7: NIR
  - Banda 9: SWIR1
  - Banda 10: SWIR2 (opcional)

- El modelo clasifica en dos clases:
  - Clase 0: No-Ciénaga
  - Clase 1: Ciénega

### 🎯 Próximos Pasos Recomendados

1. **Validación con Datos de Test**
   - Probar con múltiples imágenes del directorio de test
   - Verificar que los resultados sean consistentes
   - Comparar resultados con datos de referencia si están disponibles

2. **Mejoras en Visualización**
   - Agregar leyenda de colores para las clases
   - Mostrar estadísticas de clasificación (porcentajes por clase)
   - Agregar opción para descargar el resultado como GeoTIFF

3. **Optimización**
   - Implementar caché para el modelo cargado
   - Optimizar procesamiento de imágenes grandes
   - Agregar progreso de procesamiento para imágenes grandes

4. **Documentación Adicional**
   - Agregar ejemplos de uso de la API
   - Documentar formato de respuesta de la API
   - Crear guía de desarrollo

