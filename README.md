# ImageAnalyzer

Sistema de análisis y clasificación de imágenes satelitales usando Python, Django y Machine Learning (Random Forest) para la detección de ciénagas en imágenes Sentinel-2.

## Características

- ✅ Entrenamiento de modelos Random Forest con 7M+ muestras
- ✅ Clasificación de imágenes satelitales (.tif) mediante interfaz web moderna (React + shadcn/ui)
- ✅ API REST para entrenamiento y análisis
- ✅ Comandos CLI para entrenamiento y pruebas
- ✅ Visualización de resultados de clasificación
- ✅ Frontend React con TypeScript y Vite

## Requisitos Previos

### Backend
- Python 3.8 o superior
- Django 4.0+
- Las siguientes librerías (ver `requirements.txt`):
  - Django>=4.0,<5.0
  - djangorestframework>=3.14,<4.0
  - django-cors-headers>=4.0.0
  - scikit-learn
  - pandas
  - numpy
  - joblib
  - Pillow>=9.0,<11.0
  - rasterio
  - matplotlib

### Frontend
- Node.js 20.19.0 o superior (recomendado 22.12.0+)
- npm 10.1.0 o superior

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <repository-url>
   cd ImageAnalyzer
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Aplicar migraciones de base de datos:**
   ```bash
   python manage.py migrate
   ```

4. **Verificar que el modelo existe:**
   El modelo entrenado debe estar en la raíz del proyecto como `modelo_rf_cienagas.pkl`. Si no existe, deberás entrenarlo primero (ver sección de Entrenamiento).

## Uso

### Iniciar el Backend (Django)

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

### Iniciar el Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

**Nota:** Asegúrate de iniciar ambos servidores para que la aplicación funcione correctamente.

### Interfaz Web (React)

1. **Navegar a la aplicación:**
   ```
   http://localhost:3000
   ```

2. **Subir una imagen .tif:**
   - Haz clic en "Seleccionar archivo" y elige una imagen satelital en formato .tif
   - Haz clic en "Analizar"
   - Se mostrará el mapa de clasificación resultante

### Interfaz Web Legacy (Django Templates)

También puedes usar la interfaz legacy basada en templates Django:

```
http://localhost:8000/api/analyze/
```

### Comandos CLI

#### Entrenar el Modelo

Entrena un nuevo modelo usando imágenes de entrenamiento:

```bash
python manage.py train_model_cli --train_path "C:\ruta\a\imagenes\train"
```

Con imágenes de test opcionales:

```bash
python manage.py train_model_cli --train_path "C:\ruta\a\imagenes\train" --test_path "C:\ruta\a\imagenes\test"
```

El modelo entrenado se guardará como `modelo_rf_cienagas.pkl` en la raíz del proyecto.

#### Probar el Modelo

Prueba el modelo con una imagen específica:

```bash
python manage.py test_model --image "C:\ruta\a\imagen.tif"
```

Guardar el resultado de clasificación:

```bash
python manage.py test_model --image "C:\ruta\a\imagen.tif" --output "C:\ruta\a\resultado.tif"
```

### API REST

#### Entrenar Modelo (POST)

```http
POST /api/train/
Content-Type: application/json

{
  "train_path": "C:\\ruta\\a\\imagenes\\train",
  "test_path": "C:\\ruta\\a\\imagenes\\test"  // opcional
}
```

Respuesta:
```json
{
  "message": "Training completed successfully",
  "metrics": {
    "model_path": "..."
  }
}
```

#### Analizar Imagen

**API JSON (Recomendado para React):**
```
POST /api/analyze-api/
Content-Type: multipart/form-data

image: [archivo .tif]
```

Respuesta:
```json
{
  "result_image_url": "data:image/png;base64,...",
  "uploaded_file_url": "/media/uploads/imagen.tif",
  "message": "Imagen clasificada exitosamente"
}
```

**HTML Legacy:**
```
GET /api/analyze/          # Muestra el formulario de carga
POST /api/analyze/         # Procesa la imagen subida
Content-Type: multipart/form-data

image: [archivo .tif]
```

## Estructura del Proyecto

```
ImageAnalyzer/
├── api/                          # Aplicación Django principal
│   ├── ml/                       # Servicios de Machine Learning
│   │   ├── preprocessor.py      # Preprocesamiento de imágenes
│   │   ├── model_loader.py      # Carga del modelo entrenado
│   │   ├── classifier.py        # Servicio de clasificación
│   │   └── trainer.py           # Entrenamiento del modelo
│   ├── management/commands/     # Comandos CLI
│   │   ├── train_model_cli.py   # Comando de entrenamiento
│   │   └── test_model.py        # Comando de prueba
│   ├── templates/api/           # Templates HTML (legacy)
│   │   ├── upload.html          # Formulario de carga
│   │   └── result.html          # Visualización de resultados
│   ├── views_ui.py              # Vistas para interfaz web (legacy)
│   ├── views_api.py             # Vistas API para React
│   ├── views_ml.py              # Vistas para API ML
│   └── urls.py                  # URLs de la API
├── frontend/                     # Aplicación React
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   │   ├── ui/              # Componentes shadcn/ui
│   │   │   ├── UploadImage.tsx  # Componente de carga
│   │   │   └── ResultView.tsx   # Componente de resultados
│   │   ├── services/
│   │   │   └── api.ts           # Servicio de API
│   │   ├── lib/
│   │   │   └── utils.ts        # Utilidades
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── ImageAnalyzer/               # Configuración Django
│   ├── settings.py
│   └── urls.py
├── media/uploads/               # Imágenes subidas por usuarios
├── modelo_rf_cienagas.pkl       # Modelo entrenado (generado)
├── requirements.txt             # Dependencias Python
└── manage.py                    # Script de gestión Django
```

## Formato de Imágenes

El sistema espera imágenes satelitales en formato GeoTIFF (.tif) con las siguientes características:

- **Bandas requeridas:**
  - Banda 1: Blue
  - Banda 2: Green
  - Banda 3: Red
  - Banda 7: NIR (Near Infrared)
  - Banda 9: SWIR1 (Shortwave Infrared 1)
  - Banda 10: SWIR2 (Shortwave Infrared 2) - opcional para entrenamiento

- **Formato:** Imágenes Sentinel-2 con valores normalizados (divididos por 10000.0)

## Clasificación

El modelo clasifica cada píxel de la imagen en dos clases:
- **Clase 0:** No-Ciénaga
- **Clase 1:** Ciénega

El resultado se muestra como un mapa de clasificación con colores que representan las diferentes clases.

## Desarrollo

### Estado del Proyecto

✅ **Completado:**
- Entrenamiento del modelo con 7M+ muestras
- Backend completo (preprocessor, model_loader, classifier, trainer)
- Comandos CLI (train_model_cli, test_model)
- Interfaz Web (templates HTML y vista Django)
- Endpoints API (/api/train/, /api/analyze/)

🔄 **Próximos Pasos:**
- Verificación end-to-end completa
- Validación con conjunto de datos de test
- Mejoras en visualización de resultados
- Optimización de rendimiento

## Deployment con Docker

Este proyecto también puede ser desplegado usando Docker y Docker Compose.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1. **Navigate to the deploy directory:**
   ```bash
   cd deploy
   ```

2. **Build and start the services:**
   ```bash
   docker-compose up --build
   ```

   - The Django application will be available at `http://localhost:8001`.
   - The TensorFlow Jupyter server will be available at `http://localhost:8888`.

### Stopping the Application

To stop and remove the containers:
```bash
docker-compose down
```

## Solución de Problemas

### Error: "Model file not found"
- Asegúrate de que `modelo_rf_cienagas.pkl` existe en la raíz del proyecto
- Si no existe, entrena el modelo usando `train_model_cli` o el endpoint `/api/train/`

### Error: "No .tif images found"
- Verifica que las imágenes estén en formato .tif o .tiff
- Asegúrate de que la ruta al directorio sea correcta

### Error al procesar imagen
- Verifica que la imagen tenga las bandas requeridas (al menos 7 bandas para NIR)
- Asegúrate de que la imagen esté en formato GeoTIFF válido

## Licencia

[Especificar licencia si aplica]

## Contacto

[Información de contacto si aplica]
