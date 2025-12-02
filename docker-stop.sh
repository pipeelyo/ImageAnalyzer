#!/bin/bash

# Script para detener Docker containers
# Uso: ./docker-stop.sh [clean]

set -e

CLEAN=${1:-}

echo "🛑 Deteniendo ImageAnalyzer Docker containers..."
echo ""

# Detener contenedores
docker-compose down

if [ "$CLEAN" == "clean" ]; then
    echo "🧹 Limpiando volúmenes y datos..."
    docker-compose down -v
    echo "✅ Contenedores y volúmenes eliminados"
else
    echo "✅ Contenedores detenidos (datos preservados)"
    echo ""
    echo "💡 Para eliminar también los datos: ./docker-stop.sh clean"
fi

echo ""
