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

Para entrenar el modelo, necesitas montar tus imágenes satelitales:

```bash
# 1. Crear carpetas locales
mkdir -p ~/Downloads/train ~/Downloads/test

# 2. Copiar tus imágenes .tif
cp /ruta/a/imagenes/*.tif ~/Downloads/train/
cp /ruta/a/imagenes/*.tif ~/Downloads/test/

# 3. Actualizar docker-compose.yml para montar las carpetas
# Ya está configurado en la sección volumes del servicio backend
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
