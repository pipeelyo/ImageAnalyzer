#!/bin/bash

# Script de inicio rápido para Docker
# Uso: ./docker-start.sh [prod|dev]

set -e

MODE=${1:-prod}

echo "🐳 ImageAnalyzer Docker Starter"
echo "================================"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo"
    echo "   Por favor inicia Docker Desktop y vuelve a intentar"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker está corriendo"

# Crear directorios de datos si no existen
if [ ! -d "$HOME/Downloads/train" ]; then
    echo -e "${YELLOW}!${NC} Creando directorio: ~/Downloads/train"
    mkdir -p "$HOME/Downloads/train"
fi

if [ ! -d "$HOME/Downloads/test" ]; then
    echo -e "${YELLOW}!${NC} Creando directorio: ~/Downloads/test"
    mkdir -p "$HOME/Downloads/test"
fi

echo -e "${GREEN}✓${NC} Directorios de datos verificados"

# Verificar si el modelo existe
if [ ! -f "modelo_rf_cienagas.pkl" ]; then
    echo -e "${YELLOW}!${NC} Advertencia: modelo_rf_cienagas.pkl no encontrado"
    echo "   Necesitarás entrenar el modelo después de iniciar los contenedores"
fi

# Iniciar servicios según el modo
if [ "$MODE" == "dev" ]; then
    echo ""
    echo "🚀 Iniciando en modo DESARROLLO..."
    echo "   - Backend: http://localhost:8000"
    echo "   - Frontend Dev: http://localhost:3000"
    echo ""
    docker-compose --profile dev up -d
else
    echo ""
    echo "🚀 Iniciando en modo PRODUCCIÓN..."
    echo "   - Backend: http://localhost:8000"
    echo "   - Frontend: http://localhost"
    echo ""
    docker-compose up -d backend frontend
fi

# Esperar a que los servicios estén listos
echo ""
echo "⏳ Esperando a que los servicios estén listos..."
sleep 5

# Verificar estado de los contenedores
echo ""
echo "📊 Estado de los contenedores:"
docker-compose ps

# Mostrar logs de inicio
echo ""
echo "📝 Últimas líneas de los logs:"
docker-compose logs --tail=20

echo ""
echo -e "${GREEN}✅ ImageAnalyzer está corriendo!${NC}"
echo ""
echo "Comandos útiles:"
echo "  Ver logs:           docker-compose logs -f"
echo "  Detener:            docker-compose down"
echo "  Reiniciar:          docker-compose restart"
echo "  Entrenar modelo:    curl -X POST http://localhost:8000/api/train/ -H 'Content-Type: application/json' -d '{}'"
echo ""
