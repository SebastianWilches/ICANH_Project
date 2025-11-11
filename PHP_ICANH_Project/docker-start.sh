#!/bin/bash

# Script para iniciar la aplicación ICANH con Docker
# Uso: ./docker-start.sh

echo "🚀 Iniciando API de Gestión de Vehículos - ICANH con Docker"
echo "=========================================================="

# Función para verificar si Docker está ejecutándose
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "❌ Error: Docker no está ejecutándose. Por favor inicia Docker primero."
        exit 1
    fi
}

# Función para verificar si el puerto 8080 está disponible
check_port() {
    if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Advertencia: El puerto 8080 ya está en uso."
        echo "   La aplicación podría no estar disponible en http://localhost:8080"
        echo ""
    fi
}

# Verificar Docker
check_docker

# Verificar puerto
check_port

echo "📦 Construyendo imagen de Docker..."
docker-compose build

echo ""
echo "🚀 Iniciando servicios..."
docker-compose up -d

echo ""
echo "⏳ Esperando a que la aplicación esté lista..."
sleep 10

echo ""
echo "🔍 Verificando estado de la aplicación..."

# Verificar health check
if curl -f http://localhost:8080/api/health > /dev/null 2>&1; then
    echo "✅ ¡Aplicación iniciada exitosamente!"
    echo ""
    echo "🌐 URLs de acceso:"
    echo "   API:         http://localhost:8080/api/"
    echo "   Swagger:     http://localhost:8080/api/documentation"
    echo "   Health:      http://localhost:8080/api/health"
    echo ""
    echo "📊 Ver logs en tiempo real:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Para detener:"
    echo "   docker-compose down"
else
    echo "❌ Error: La aplicación no responde."
    echo ""
    echo "🔍 Verificar logs:"
    echo "   docker-compose logs icanh-api"
    echo ""
    echo "🐛 Debug:"
    echo "   docker-compose exec icanh-api bash"
fi

