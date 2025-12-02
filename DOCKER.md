# 🐳 Guía de Docker para ImageAnalyzer

Esta guía explica cómo ejecutar ImageAnalyzer usando Docker y Docker Compose.

## 📋 Requisitos Previos

- [Docker](https://docs.docker.com/get-docker/) instalado (versión 20.10 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) instalado (versión 2.0 o superior)
- Al menos 4GB de RAM disponible
- Espacio en disco: ~3GB para imágenes + ~1.1GB para el modelo entrenado

## 🏗️ Arquitectura

El proyecto incluye tres contenedores:

1. **backend**: Django API (puerto 8000)
2. **frontend**: React + Nginx (puerto 80)
3. **frontend-dev**: React + Vite Dev Server (puerto 3000) - Solo para desarrollo

## 🚀 Inicio Rápido

### Opción 1: Producción (Recomendado)

```bash
# 1. Construir e iniciar los servicios
docker-compose up -d

# 2. Verificar que los contenedores estén corriendo
docker-compose ps

# 3. Ver logs (opcional)
docker-compose logs -f

# 4. Acceder a la aplicación
# Frontend: http://localhost
# Backend API: http://localhost:8000
```

### Opción 2: Desarrollo

```bash
# Iniciar backend + frontend de desarrollo
docker-compose --profile dev up -d

# Acceder a:
# Frontend Dev: http://localhost:3000
# Backend API: http://localhost:8000
```

## 📂 Preparar Datos de Entrenamiento

### 📁 Ubicación de las Imágenes

Las imágenes para entrenar el modelo deben estar en estas carpetas de tu máquina:

```
~/Downloads/train/    → 30 imágenes satelitales .tif para entrenamiento
~/Downloads/test/     → 30 imágenes satelitales .tif para pruebas
```

### 🔄 Cómo Cargar las Imágenes

**Opción 1: Crear las carpetas y copiar imágenes**

```bash
# 1. Crear las carpetas si no existen
mkdir -p ~/Downloads/train ~/Downloads/test

# 2. Copiar tus imágenes .tif desde su ubicación actual
cp /ruta/donde/tienes/imagenes/train/*.tif ~/Downloads/train/
cp /ruta/donde/tienes/imagenes/test/*.tif ~/Downloads/test/

# 3. Verificar que se copiaron correctamente
ls ~/Downloads/train/*.tif | wc -l   # Debería mostrar 30
ls ~/Downloads/test/*.tif | wc -l    # Debería mostrar 30
```

**Opción 2: Mover carpetas existentes**

```bash
# Si ya tienes las carpetas train y test en otra ubicación
mv /ruta/donde/tienes/train ~/Downloads/
mv /ruta/donde/tienes/test ~/Downloads/

# Verificar
ls ~/Downloads/train/*.tif | wc -l   # 30 imágenes
ls ~/Downloads/test/*.tif | wc -l    # 30 imágenes
```

### ✅ Verificar desde Docker

Una vez que los contenedores estén corriendo, verifica que Docker puede ver las imágenes:

```bash
# Verificar cantidad de imágenes de entrenamiento
docker-compose exec backend ls /training-data/train/ | wc -l    # 30

# Verificar cantidad de imágenes de prueba  
docker-compose exec backend ls /training-data/test/ | wc -l     # 30

# Ver detalles de las imágenes montadas
docker-compose exec backend ls -lh /training-data/train/
docker-compose exec backend ls -lh /training-data/test/

# Verificar que una imagen es accesible
docker-compose exec backend file /training-data/train/Sentinel2_*.tif | head -1
```

### 📋 Cómo Funcionan los Volúmenes

En el `docker-compose.yml` tenemos configurado:

```yaml
volumes:
  - ~/Downloads/train:/training-data/train
  - ~/Downloads/test:/training-data/test
```

Esto significa:
- **Host** `~/Downloads/train/` → **Contenedor** `/training-data/train/`
- **Host** `~/Downloads/test/` → **Contenedor** `/training-data/test/`

**Importante:** Los cambios en `~/Downloads/train/` o `~/Downloads/test/` se reflejan **inmediatamente** dentro del contenedor porque es un montaje directo (no una copia).

## 🎓 Entrenar el Modelo

Una vez que tengas las imágenes cargadas en `~/Downloads/train` y `~/Downloads/test`, y los contenedores estén corriendo, puedes entrenar el modelo.

### Opción 1: Via API REST (Recomendado)

```bash
# Entrenar el modelo con las rutas por defecto
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{}'

# O especificar rutas personalizadas (dentro del contenedor)
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{
    "train_path": "/training-data/train",
    "test_path": "/training-data/test"
  }'
```

### Opción 2: Via CLI dentro del contenedor

```bash
# Entrenar con rutas por defecto
docker-compose exec backend python manage.py train_model_cli \
  --train_path /training-data/train \
  --test_path /training-data/test

# Ver el progreso en tiempo real
docker-compose logs -f backend
```

### 📊 Resultado Esperado

El entrenamiento procesará todas las imágenes y debería mostrar:

```
Training started. Train dir: /training-data/train, Test dir: /training-data/test
Processing training image: Sentinel2_10bandas_*.tif
Processing training image: Sentinel2_10bandas_*.tif
...
Total samples: 7040495, Features: 5
Model trained successfully.
Model saved to /app/modelo_rf_cienagas.pkl
```

**Tiempo estimado:** 10-15 minutos dependiendo de tu hardware.

### ✅ Verificar que el Modelo se Entrenó

```bash
# Verificar que el archivo del modelo existe
docker-compose exec backend ls -lh modelo_rf_cienagas.pkl

# Debería mostrar algo como:
# -rw-r--r-- 1 root root 1.1G Dec  1 23:59 modelo_rf_cienagas.pkl
```

## 🚀 Usar la Aplicación

Una vez que el modelo esté entrenado, puedes usar el frontend para analizar imágenes:

### Acceso

- **Modo Desarrollo:** http://localhost:3000
- **Modo Producción:** http://localhost

### Probar el Análisis

1. Abre el navegador en la URL correspondiente
2. Haz clic en "Choose File" o "Cargar Imagen"
3. Selecciona una imagen satelital .tif de tu computadora
4. Haz clic en "Analizar"
5. Espera ~30 segundos (dependiendo del tamaño de la imagen)
6. Verás el resultado:
   - **Azul:** Áreas clasificadas como ciénagas
   - **Rojo:** Áreas clasificadas como no ciénagas

### Ver Logs del Análisis

```bash
# Monitorear en tiempo real
docker-compose logs -f backend

# Deberías ver:
# Loading model from /app/modelo_rf_cienagas.pkl...
# Model loaded successfully.
# POST /api/analyze-api/ HTTP/1.1" 200
```

## 🎯 Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Ver estado de los contenedores
docker-compose ps

# Detener y eliminar todo (incluyendo volúmenes)
docker-compose down -v
```

### Rebuild de Imágenes

```bash
# Reconstruir todas las imágenes
docker-compose build

# Reconstruir sin caché
docker-compose build --no-cache

# Reconstruir un servicio específico
docker-compose build backend
docker-compose build frontend

# Reconstruir e iniciar
docker-compose up -d --build
```

### Ejecutar Comandos en Contenedores

```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Ejecutar migraciones
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Entrenar modelo
docker-compose exec backend python manage.py train_model_cli --train_path /training-data/train

# Verificar contenido del contenedor
docker-compose exec backend ls -la
```

### Gestión de Volúmenes

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar volumen de training
docker volume inspect imageanalyzer_training-data

# Eliminar volúmenes no utilizados
docker volume prune
```

## 🔧 Configuración

### Variables de Entorno

Puedes personalizar la configuración creando un archivo `.env`:

```bash
# .env
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
ML_TRAIN_PATH=/training-data/train
ML_TEST_PATH=/training-data/test
```

Luego actualiza `docker-compose.yml` para usar el archivo:

```yaml
services:
  backend:
    env_file:
      - .env
```

### Puertos Personalizados

Para cambiar los puertos, edita `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Host:Contenedor
  
  frontend:
    ports:
      - "8081:80"
```

## 🧪 Entrenar el Modelo con Docker

### Método 1: Via API (Recomendado)

```bash
# 1. Asegurarte de que el backend esté corriendo
docker-compose ps backend

# 2. Entrenar usando curl
curl -X POST http://localhost:8000/api/train/ \
  -H "Content-Type: application/json" \
  -d '{}'

# 3. Ver progreso en los logs
docker-compose logs -f backend
```

### Método 2: Via CLI

```bash
# Entrenar directamente en el contenedor
docker-compose exec backend python manage.py train_model_cli \
  --train_path /training-data/train \
  --test_path /training-data/test
```

### Método 3: Copiar Modelo Pre-entrenado

```bash
# Si ya tienes un modelo entrenado localmente
docker cp modelo_rf_cienagas.pkl imageanalyzer-backend:/app/modelo_rf_cienagas.pkl

# Reiniciar el backend
docker-compose restart backend
```

## 📊 Monitoreo

### Ver Uso de Recursos

```bash
# Estadísticas en tiempo real
docker stats

# Uso de un contenedor específico
docker stats imageanalyzer-backend
```

### Inspeccionar Contenedores

```bash
# Información detallada del contenedor
docker inspect imageanalyzer-backend

# Procesos corriendo en el contenedor
docker top imageanalyzer-backend
```

## 🐛 Solución de Problemas

### El backend no inicia

```bash
# Ver logs detallados
docker-compose logs backend

# Verificar que las dependencias se instalaron
docker-compose exec backend pip list

# Reconstruir la imagen
docker-compose build --no-cache backend
docker-compose up -d backend
```

### El frontend no carga

```bash
# Verificar logs
docker-compose logs frontend

# Probar acceso directo al backend
curl http://localhost:8000/api/

# Reconstruir frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Error de permisos

```bash
# Cambiar permisos de las carpetas montadas
chmod -R 755 ~/Downloads/train ~/Downloads/test

# O ejecutar con permisos de usuario
docker-compose exec -u $(id -u):$(id -g) backend bash
```

### El modelo no se encuentra

```bash
# Verificar que el modelo existe en el contenedor
docker-compose exec backend ls -lh /app/modelo_rf_cienagas.pkl

# Copiar modelo al contenedor si es necesario
docker cp modelo_rf_cienagas.pkl imageanalyzer-backend:/app/
```

### Error de conexión entre frontend y backend

```bash
# Verificar la red de Docker
docker network ls
docker network inspect imageanalyzer_imageanalyzer-network

# Probar conectividad
docker-compose exec frontend ping backend
```

## 🔒 Producción

Para un despliegue en producción, considera:

### 1. Usar Gunicorn en lugar de runserver

Actualiza el `Dockerfile.backend`:

```dockerfile
# Instalar gunicorn
RUN pip install gunicorn

# Cambiar CMD
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "ImageAnalyzer.wsgi:application"]
```

### 2. Configurar Variables de Entorno Seguras

```bash
# Generar SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Usar en .env
DEBUG=False
SECRET_KEY=<tu-secret-key-generada>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

### 3. Usar un Reverse Proxy (Nginx/Traefik)

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx/prod.conf:/etc/nginx/nginx.conf
      - ./certbot/conf:/etc/letsencrypt
    depends_on:
      - backend
      - frontend
```

### 4. Agregar Health Checks

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 📝 Estructura de Archivos Docker

```
ImageAnalyzer/
├── Dockerfile.backend          # Dockerfile del backend Django
├── docker-compose.yml          # Orquestación de servicios
├── .dockerignore              # Archivos a ignorar en backend
└── frontend/
    ├── Dockerfile             # Dockerfile producción (Nginx)
    ├── Dockerfile.dev         # Dockerfile desarrollo (Vite)
    ├── nginx.conf            # Configuración de Nginx
    └── .dockerignore         # Archivos a ignorar en frontend
```

## 🎓 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Vite Build for Production](https://vitejs.dev/guide/build.html)

## 💡 Tips

1. **Desarrollo**: Usa `docker-compose --profile dev up -d` para hot-reload
2. **Logs**: Siempre revisa los logs con `docker-compose logs -f`
3. **Volúmenes**: Los volúmenes persisten los datos incluso si eliminas los contenedores
4. **Red**: Los servicios se comunican por nombre (ej: `backend:8000`)
5. **Caché**: Usa `--no-cache` si tienes problemas con builds antiguos

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica el estado: `docker-compose ps`
3. Reinicia los servicios: `docker-compose restart`
4. Reconstruye las imágenes: `docker-compose build --no-cache`
