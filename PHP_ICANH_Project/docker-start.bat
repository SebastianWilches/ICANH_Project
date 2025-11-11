@echo off
REM Script para iniciar la aplicación ICANH con Docker (Windows)
REM Uso: docker-start.bat

echo 🚀 Iniciando API de Gestión de Vehículos - ICANH con Docker
echo ===========================================================

REM Verificar si Docker está ejecutándose
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Docker no está ejecutándose. Por favor inicia Docker primero.
    pause
    exit /b 1
)

REM Verificar si el puerto 8080 está disponible
netstat -an | find "8080" | find "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Advertencia: El puerto 8080 ya está en uso.
    echo    La aplicación podría no estar disponible en http://localhost:8080
    echo.
)

echo 📦 Construyendo imagen de Docker...
docker-compose build

echo.
echo 🚀 Iniciando servicios...
docker-compose up -d

echo.
echo ⏳ Esperando a que la aplicación esté lista...
timeout /t 10 /nobreak >nul

echo.
echo 🔍 Verificando estado de la aplicación...

REM Verificar health check usando PowerShell para curl
powershell -Command "& {try { $response = Invoke-WebRequest -Uri 'http://localhost:8080/api/health' -TimeoutSec 10; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }}" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ¡Aplicación iniciada exitosamente!
    echo.
    echo 🌐 URLs de acceso:
    echo    API:         http://localhost:8080/api/
    echo    Swagger:     http://localhost:8080/api/documentation
    echo    Health:      http://localhost:8080/api/health
    echo.
    echo 📊 Ver logs en tiempo real:
    echo    docker-compose logs -f
    echo.
    echo 🛑 Para detener:
    echo    docker-compose down
) else (
    echo ❌ Error: La aplicación no responde.
    echo.
    echo 🔍 Verificar logs:
    echo    docker-compose logs icanh-api
    echo.
    echo 🐛 Debug:
    echo    docker-compose exec icanh-api bash
)

echo.
pause

