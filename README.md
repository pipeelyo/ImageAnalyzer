# ImageAnalyzer 🛰️

Análisis de imágenes satelitales Sentinel-2 para detectar ciénagas usando Machine Learning.

## 🚀 Inicio Rápido

### 1️⃣ Preparar tus imágenes

Copia tus imágenes satelitales .tif en estas carpetas:
```bash
~/Downloads/train/  # 30 imágenes para entrenar
~/Downloads/test/   # 30 imágenes para probar
```

### 2️⃣ Iniciar el proyecto

```bash
docker compose up -d
```

### 3️⃣ Entrenar el modelo

```bash
curl -X POST http://localhost:8000/api/train/ -H "Content-Type: application/json" -d '{}'
```
⏱️ Espera 10-15 minutos mientras entrena

### 4️⃣ Usar la aplicación

Abre tu navegador en: **http://localhost:3000**

1. Sube una imagen .tif
2. Haz clic en "Analizar"
3. Ve el resultado (azul = ciénagas, rojo = no ciénagas)

## 📋 Requisitos

- Docker y Docker Compose instalados
- 4GB RAM mínimo
- 60 imágenes satelitales .tif (30 train, 30 test)

## 🛠️ Comandos Útiles

```bash
# Ver logs en tiempo real
docker compose logs -f

# Detener todo
docker compose down

# Reiniciar servicios
docker compose restart

# Ver estado
docker compose ps
```

## 📚 Documentación Completa

- **[DOCKER.md](./DOCKER.md)** - Guía completa de Docker
- **[ML_TRAINING_API.md](./ML_TRAINING_API.md)** - API de entrenamiento

## ⚙️ Configuración Avanzada

### Cambiar ubicación de las imágenes

Si tus imágenes están en otra carpeta, crea un archivo `.env`:

```bash
TRAIN_DATA_PATH=/tu/carpeta/train
TEST_DATA_PATH=/tu/carpeta/test
```

Ver más en [DOCKER.md](./DOCKER.md#configuración-para-diferentes-ambientes)

### Correr sin Docker

<details>
<summary>Instrucciones para desarrollo local (sin Docker)</summary>

**Backend:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Entrenar:**
```bash
curl -X POST http://localhost:8000/api/train/ -H "Content-Type: application/json" -d '{}'
```

Accede a http://localhost:3000

</details>

## 🔧 Tecnologías

- **Backend:** Django 4.x, Python 3.9+, scikit-learn
- **Frontend:** React, TypeScript, Vite, shadcn/ui
- **ML:** Random Forest con 7M+ muestras
- **Docker:** Containerización completa

## 📝 Licencia

MIT

---

**¿Problemas?** Revisa [DOCKER.md](./DOCKER.md) o abre un issue en GitHub.
