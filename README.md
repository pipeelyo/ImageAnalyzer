# ImageAnalyzer 🛰️

Sistema de análisis y clasificación de imágenes satelitales usando Python, Django y Machine Learning (Random Forest) para la detección de ciénagas en imágenes Sentinel-2.

## 🚀 Inicio Rápido (TL;DR)

### Con Docker 🐳 (Recomendado)

```bash
# 1. Iniciar con un comando
./docker-start.sh

# 2. Abrir http://localhost
```

### Sin Docker (Desarrollo Local)

```bash
# 1. Preparar entorno
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# 2. Preparar imágenes
mkdir -p ~/Downloads/train ~/Downloads/test
# Copiar 30 imágenes .tif en cada carpeta

# 3. Iniciar backend
python manage.py runserver  # Terminal 1

# 4. Entrenar modelo (nueva terminal)
curl -X POST http://localhost:8000/api/train/ -H "Content-Type: application/json" -d '{}'

# 5. Iniciar frontend (nueva terminal)
cd frontend && npm install && npm run dev

# 6. Abrir http://localhost:3000
```

## Características

- ✅ Entrenamiento de modelos Random Forest con 7M+ muestras
- ✅ Clasificación de imágenes satelitales (.tif) mediante interfaz web moderna (React + shadcn/ui)
- ✅ API REST para entrenamiento y análisis
- ✅ Comandos CLI para entrenamiento y pruebas
- ✅ Visualización de resultados de clasificación
- ✅ Frontend React con TypeScript y Vite
- ✅ Configuración de rutas por defecto para facilitar el uso

## Requisitos Previos

### Backend
- Python 3.9 o superior
- Django 4.0+
- pip 21.0 o superior

### Frontend
- Node.js 20.19.0 o superior (recomendado 22.12.0+)
- npm 10.1.0 o superior

### Con Docker (Alternativa Recomendada)
- Docker 20.10 o superior
- Docker Compose 2.0 o superior
- 4GB RAM mínimo disponible

## 🐳 Despliegue con Docker (Recomendado)

La forma más rápida y confiable de ejecutar el proyecto es usando Docker. Ver [DOCKER.md](./DOCKER.md) para documentación completa.

### 📋 Requisitos Previos para Docker

- Docker 20.10 o superior
- Docker Compose 2.0 o superior  
- 4GB RAM mínimo disponible
- 30 imágenes .tif en `~/Downloads/train` y 30 en `~/Downloads/test`

### 🚀 Guía Paso a Paso con Docker

#### Paso 1: Preparar las Imágenes de Entrenamiento

```bash
# Crear las carpetas si no existen
mkdir -p ~/Downloads/train ~/Downloads/test

# Copiar tus imágenes satelitales .tif
# - 30 imágenes en ~/Downloads/train/
# - 30 imágenes en ~/Downloads/test/
```

#### Paso 2: Levantar los Servicios

**Opción A: Modo Desarrollo (con hot-reload en puerto 3000)**
```bash
# Iniciar backend y frontend de desarrollo
docker compose --profile dev up -d

# Verificar que estén corriendo
docker compose ps
```

**Opción B: Modo Producción (puerto 80)**
```bash
# Iniciar backend y frontend optimizado
docker compose up -d backend frontend

# Verificar que estén corriendo
docker compose ps
```

#### Paso 3: Entrenar el Modelo

Una vez que los contenedores estén corriendo, entrena el modelo:

**Opción A: Via API REST**
```bash
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Opción B: Via CLI dentro del contenedor**
```bash
docker compose exec backend python manage.py train_model_cli \
  --train_path /training-data/train \
  --test_path /training-data/test
```

**Tiempo estimado:** 10-15 minutos (procesa ~7M muestras)

**Resultado esperado:**
```
Total samples: 7040495, Features: 5
Model trained successfully.
Model saved to /app/modelo_rf_cienagas.pkl
```

#### Paso 4: Usar la Aplicación

Una vez entrenado el modelo, accede al frontend:

- **Desarrollo**: http://localhost:3000
- **Producción**: http://localhost

**Probar el análisis de imágenes:**
1. Haz clic en "Choose File" 
2. Selecciona una imagen .tif
3. Haz clic en "Analizar"
4. Espera a que procese (puede tardar ~30 segundos)
5. Verás el mapa de clasificación (azul = ciénagas, rojo = no ciénagas)

### 🔧 Comandos Docker Útiles

```bash
# Ver logs en tiempo real
docker compose logs -f backend
docker compose logs -f frontend-dev

# Ver todos los logs
docker compose logs -f

# Reiniciar un servicio
docker compose restart backend
docker compose restart frontend-dev

# Detener todos los servicios
docker compose down

# Detener y limpiar todo (incluyendo volúmenes)
docker compose down -v

# Reconstruir las imágenes
docker compose build --no-cache

# Ver estado de los contenedores
docker compose ps

# Entrar a un contenedor
docker compose exec backend bash
docker compose exec frontend-dev sh
```

### 📊 Verificar que Todo Funciona

```bash
# 1. Verificar que los contenedores estén corriendo
docker compose ps
# Deberías ver: backend (Up), frontend-dev (Up)

# 2. Verificar que el backend responde
curl http://localhost:8000/api/train/ -X OPTIONS

# 3. Verificar que el modelo existe
docker compose exec backend ls -lh modelo_rf_cienagas.pkl

# 4. Ver las imágenes de entrenamiento
docker compose exec backend ls /training-data/train/ | wc -l  # Debería mostrar 30
docker compose exec backend ls /training-data/test/ | wc -l   # Debería mostrar 30
```

### ⚠️ Solución de Problemas con Docker

**Problema: Error "ECONNREFUSED" en el frontend**
```bash
# Verificar que el backend esté corriendo
docker compose ps backend

# Reiniciar los servicios
docker compose restart backend frontend-dev
```

**Problema: "Train path does not exist"**
```bash
# Verificar que las imágenes estén montadas
docker compose exec backend ls /training-data/train/
docker compose exec backend ls /training-data/test/

# Si están vacías, verifica que ~/Downloads/train y ~/Downloads/test tengan imágenes
ls ~/Downloads/train/*.tif | wc -l
ls ~/Downloads/test/*.tif | wc -l
```

**Problema: "Model file not found"**
```bash
# Entrenar el modelo primero
curl -X POST http://localhost:8000/api/train/ -H "Content-Type: application/json" -d '{}'

# O usar el CLI
docker compose exec backend python manage.py train_model_cli \
  --train_path /training-data/train --test_path /training-data/test
```

**Problema: Cambios en el código no se reflejan**
```bash
# Para el backend, Django recarga automáticamente
# Para el frontend en dev, Vite recarga automáticamente

# Si no funcionan, reconstruir:
docker compose down
docker compose build
docker compose --profile dev up -d
```

## 🚀 Guía de Inicio Rápido (Sin Docker)

Sigue estos pasos en orden para levantar el proyecto completo:

### Paso 1: Preparar el Entorno

1. **Clonar el repositorio:**
   ```bash
   git clone <repository-url>
   cd ImageAnalyzer
   ```

2. **Crear entorno virtual de Python:**
   ```bash
   python3 -m venv venv
   ```

3. **Activar el entorno virtual:**
   
   En macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   En Windows:
   ```bash
   venv\Scripts\activate
   ```

### Paso 2: Configurar el Backend

1. **Instalar dependencias de Python:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Aplicar migraciones de base de datos:**
   ```bash
   python manage.py migrate
   ```

### Paso 3: Preparar Imágenes de Entrenamiento

1. **Crear carpetas para imágenes:**
   ```bash
   mkdir -p ~/Downloads/train
   mkdir -p ~/Downloads/test
   ```

2. **Copiar imágenes satelitales (.tif):**
   - Coloca 30 imágenes en `~/Downloads/train/` para entrenamiento
   - Coloca 30 imágenes en `~/Downloads/test/` para pruebas
   - Las imágenes deben ser archivos Sentinel-2 en formato .tif

   **Nota:** Las rutas por defecto están configuradas en `ImageAnalyzer/settings.py`:
   ```python
   ML_TRAIN_PATH = os.path.expanduser("~/Downloads/train")
   ML_TEST_PATH = os.path.expanduser("~/Downloads/test")
   ```

### Paso 4: Iniciar el Backend

1. **Iniciar el servidor Django:**
   ```bash
   python manage.py runserver
   ```

   El servidor estará disponible en `http://localhost:8000`

2. **Verificar que el backend está corriendo:**
   Abre tu navegador en `http://localhost:8000`

### Paso 5: Entrenar el Modelo

**Opción A: Vía API REST (Recomendado)**

Con el backend corriendo, abre una nueva terminal y ejecuta:

```bash
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

O usa el script de prueba incluido:
```bash
python test_training_api.py
```

**Opción B: Vía Comando CLI**

```bash
python manage.py train_model_cli --train_path ~/Downloads/train --test_path ~/Downloads/test
```

**Tiempo estimado:** 10-15 minutos dependiendo de las imágenes.

**Resultado:** Se creará el archivo `modelo_rf_cienagas.pkl` (~1.1GB) en la raíz del proyecto.

### Paso 6: Configurar el Frontend

1. **Navegar a la carpeta frontend:**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias de Node.js:**
   ```bash
   npm install
   ```

### Paso 7: Iniciar el Frontend

1. **Iniciar el servidor de desarrollo:**
   ```bash
   npm run dev
   ```

   El frontend estará disponible en `http://localhost:3000`

2. **Abrir la aplicación:**
   Abre tu navegador en `http://localhost:3000`

### ✅ Verificación Final

Deberías tener corriendo:
- ✅ Backend Django en `http://localhost:8000`
- ✅ Frontend React en `http://localhost:3000`
- ✅ Modelo entrenado `modelo_rf_cienagas.pkl` en la raíz del proyecto

## 📝 Uso de la Aplicación

### Interfaz Web (React)

1. **Navegar a la aplicación:**
   ```
   http://localhost:3000
   ```

2. **Analizar una imagen:**
   - Haz clic en "Seleccionar archivo" y elige una imagen satelital en formato .tif
   - Haz clic en "Analizar"
   - Espera mientras se procesa la imagen
   - Se mostrará el mapa de clasificación resultante

### Interfaz Web Legacy (Django Templates)

También puedes usar la interfaz legacy basada en templates Django:

```
http://localhost:8000/api/analyze/
```

## 🔧 Comandos Útiles

### Gestión del Backend

```bash
# Activar entorno virtual
source venv/bin/activate              # macOS/Linux
venv\Scripts\activate                 # Windows

# Iniciar servidor Django
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario para admin
python manage.py createsuperuser
```

### Gestión del Frontend

```bash
# Instalar dependencias
cd frontend
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build

# Vista previa de producción
npm run preview
```

### Comandos CLI de Machine Learning

#### Entrenar el Modelo (Línea de Comandos)

```bash
# Usar rutas por defecto (~/Downloads/train y ~/Downloads/test)
python manage.py train_model_cli --train_path ~/Downloads/train --test_path ~/Downloads/test

# Usar rutas personalizadas
python manage.py train_model_cli --train_path "/ruta/custom/train"
```

#### Probar el Modelo

```bash
# Probar con una imagen
python manage.py test_model --image "ruta/a/imagen.tif"

# Guardar resultado de clasificación
python manage.py test_model --image "ruta/a/imagen.tif" --output "ruta/resultado.tif"
```

### API REST

#### Entrenar Modelo (POST)

**Usar rutas por defecto (sin parámetros):**
```bash
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Especificar rutas personalizadas:**
```bash
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{
    "train_path": "/ruta/custom/train",
    "test_path": "/ruta/custom/test"
  }'
```

**Respuesta exitosa:**
```json
{
  "message": "Training completed successfully",
  "train_path": "/Users/usuario/Downloads/train",
  "test_path": "/Users/usuario/Downloads/test",
  "metrics": {
    "model_path": "/ruta/al/modelo_rf_cienagas.pkl"
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

## ⚠️ Solución de Problemas

### Backend

**Error: "ModuleNotFoundError: No module named 'django'"**
- Solución: Asegúrate de activar el entorno virtual antes de ejecutar comandos:
  ```bash
  source venv/bin/activate  # macOS/Linux
  ```

**Error: "Model file not found"**
- Solución: El modelo no ha sido entrenado. Sigue el **Paso 5** de la guía de inicio rápido para entrenar el modelo
- Verifica que existe el archivo `modelo_rf_cienagas.pkl` en la raíz del proyecto

**Error: "No .tif images found in training directory"**
- Solución: Verifica que las carpetas `~/Downloads/train` y `~/Downloads/test` contengan imágenes .tif
- Asegúrate de que las rutas en `settings.py` apunten a las carpetas correctas

**Error: "Train path does not exist"**
- Solución: Crea las carpetas necesarias:
  ```bash
  mkdir -p ~/Downloads/train ~/Downloads/test
  ```

### Frontend

**Error: "npm: command not found"**
- Solución: Instala Node.js desde https://nodejs.org/

**Error: "CORS policy" al hacer peticiones al backend**
- Solución: Verifica que el backend esté corriendo en `http://localhost:8000`
- Confirma que `CORS_ALLOWED_ORIGINS` en `settings.py` incluye `http://localhost:3000`

**El frontend no carga**
- Solución: Verifica que instalaste las dependencias:
  ```bash
  cd frontend
  npm install
  ```

### Entrenamiento

**El entrenamiento toma mucho tiempo**
- Esto es normal con 7M+ muestras. Puede tardar 10-15 minutos
- Puedes reducir el número de imágenes de entrenamiento para pruebas más rápidas

**Error al leer imágenes: "Missing required bands"**
- Solución: Verifica que las imágenes Sentinel-2 tengan al menos 7 bandas (incluyendo NIR)
- Asegúrate de usar imágenes en formato GeoTIFF válido

**"No cienaga pixels found in [image]"**
- Este es un aviso, no un error. Algunas imágenes pueden no contener píxeles clasificados como ciénaga
- El entrenamiento continuará con las imágenes que sí tienen datos válidos

## 💡 Tips y Mejores Prácticas

### Rendimiento

- **Entrenamiento inicial:** Usa un conjunto pequeño de imágenes (5-10) para validar que todo funciona
- **Producción:** Usa el conjunto completo de 30+ imágenes para mejor precisión
- **Hardware:** El entrenamiento se beneficia de múltiples CPU cores (usa todos con `n_jobs=-1`)

### Organización de Datos

```
~/Downloads/
├── train/          # 30 imágenes para entrenamiento
│   ├── imagen1.tif
│   ├── imagen2.tif
│   └── ...
├── test/           # 30 imágenes para validación
│   ├── imagen31.tif
│   ├── imagen32.tif
│   └── ...
└── nuevas/         # Carpeta para imágenes a clasificar
    └── imagen_nueva.tif
```

### Desarrollo

- **Backend:** Usa `nodemon` o similar para hot-reload automático
- **Frontend:** Vite proporciona hot-reload por defecto con `npm run dev`
- **API Testing:** Usa Postman o `curl` para probar endpoints
- **Script de prueba:** Ejecuta `python test_training_api.py` para validar el API

### Producción

- Cambia `DEBUG = False` en `settings.py`
- Configura un servidor web (Nginx, Apache) para servir archivos estáticos
- Usa Gunicorn o uWSGI para el backend Django
- Compila el frontend: `npm run build` y sirve desde `/dist`

## 📂 Archivos Importantes

- **`modelo_rf_cienagas.pkl`** (~1.1GB): Modelo entrenado de Random Forest
- **`requirements.txt`**: Dependencias de Python
- **`settings.py`**: Configuración de Django (incluye rutas ML por defecto)
- **`test_training_api.py`**: Script para probar el API de entrenamiento
- **`ML_TRAINING_API.md`**: Documentación detallada del API de entrenamiento

## Licencia

[Especificar licencia si aplica]

## Contacto

[Información de contacto si aplica]
