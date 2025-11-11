# 🚀 API de Gestión de Vehículos - ICANH (Docker)

Esta guía explica cómo ejecutar la aplicación Laravel usando Docker y Docker Compose.

## 📋 Prerrequisitos

- **Docker**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Incluido con Docker Desktop

## 🏗️ Estructura de Docker

```
PHP_ICANH_Project/
├── Dockerfile              # Configuración del contenedor Laravel
├── docker-compose.yml      # Orquestación de servicios
├── .dockerignore          # Archivos excluidos del build
└── DOCKER_README.md       # Esta guía
```

## 🚀 Ejecutar la Aplicación

### **Opción 1: Desarrollo (Recomendado)**

```bash
# Construir y ejecutar la aplicación
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f
```

### **Opción 2: Producción**

```bash
# Construir imagen de producción
docker-compose -f docker-compose.yml up --build -d
```

## 🌐 URLs de Acceso

Después de ejecutar Docker Compose:

- **API Base**: `http://localhost:8080/api/`
- **Documentación Swagger**: `http://localhost:8080/api/documentation`
- **Health Check**: `http://localhost:8080/api/health`

## 🛠️ Comandos Útiles de Docker

### **Gestión del Contenedor**

```bash
# Ver estado de servicios
docker-compose ps

# Ejecutar comandos en el contenedor
docker-compose exec icanh-api bash

# Ver logs del contenedor
docker-compose logs icanh-api

# Detener la aplicación
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache
```

### **Debugging y Mantenimiento**

```bash
# Ejecutar tests dentro del contenedor
docker-compose exec icanh-api php artisan test

# Generar nueva documentación Swagger
docker-compose exec icanh-api php artisan l5-swagger:generate

# Limpiar cache de Laravel
docker-compose exec icanh-api php artisan cache:clear
docker-compose exec icanh-api php artisan config:clear

# Ejecutar migraciones
docker-compose exec icanh-api php artisan migrate

# Acceder al shell del contenedor
docker-compose exec icanh-api bash
```

## 📊 Servicios Incluidos

### **icanh-api**
- **Imagen base**: PHP 8.4 con Apache
- **Puerto**: 8080 (mapeado desde el puerto 80 del contenedor)
- **Base de datos**: SQLite (archivo local en `./database/database.sqlite`)
- **Volúmenes**:
  - `./storage` → `/var/www/html/storage` (logs, cache, sesiones)
  - `./database` → `/var/www/html/database` (base de datos SQLite)

## 🔧 Configuración

### **Variables de Entorno**
El contenedor está configurado con variables de producción:
- `APP_ENV=production`
- `APP_DEBUG=false`
- `DB_CONNECTION=sqlite`
- Puerto: 8080

### **Persistencia de Datos**
- **Base de datos SQLite**: Se mantiene en `./database/database.sqlite`
- **Storage**: Logs y archivos temporales se mantienen en `./storage/`

## 🧪 Testing con Docker

```bash
# Ejecutar todos los tests
docker-compose exec icanh-api php artisan test

# Ejecutar tests específicos
docker-compose exec icanh-api php artisan test --filter=MarcaVehiculoRoutesTest

# Ejecutar tests con verbose
docker-compose exec icanh-api php artisan test -v
```

## 🔍 Health Check

El contenedor incluye health checks automáticos:
- **Endpoint**: `/api/health`
- **Intervalo**: 30 segundos
- **Timeout**: 10 segundos
- **Retries**: 3

## 🐛 Troubleshooting

### **Problema: Puerto 8080 ocupado**
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8081:80"  # Cambiar 8080 por 8081
```

### **Problema: Contenedor no inicia**
```bash
# Ver logs detallados
docker-compose logs icanh-api

# Reconstruir sin cache
docker-compose build --no-cache
docker-compose up -d
```

### **Problema: Error de permisos**
```bash
# Ajustar permisos en el host
sudo chown -R $USER:$USER storage/
sudo chown -R $USER:$USER database/
```

### **Problema: Base de datos corrupta**
```bash
# Recrear base de datos
docker-compose exec icanh-api php artisan migrate:fresh --force
```

## 📈 Monitoreo

```bash
# Ver estado de salud
curl http://localhost:8080/api/health

# Ver métricas del contenedor
docker stats icanh-laravel-api

# Ver uso de recursos
docker-compose top
```

## 🛑 Detener y Limpiar

```bash
# Detener aplicación
docker-compose down

# Limpiar contenedores e imágenes
docker-compose down --volumes --rmi all

# Limpiar sistema Docker
docker system prune -f
```

## 🎯 API Endpoints Disponibles

### **Marcas de Vehículo** (`/api/marcas-vehiculo/`)
- `GET /` - Listar marcas
- `POST /` - Crear marca
- `GET /{id}` - Obtener marca
- `PUT /{id}` - Actualizar marca
- `DELETE /{id}` - Eliminar marca

### **Personas** (`/api/personas/`)
- `GET /` - Listar personas
- `POST /` - Crear persona
- `GET /{id}` - Obtener persona
- `PUT /{id}` - Actualizar persona
- `DELETE /{id}` - Eliminar persona
- `GET /{id}/vehiculos/` - Vehículos de una persona

### **Vehículos** (`/api/vehiculos/`)
- `GET /` - Listar vehículos
- `POST /` - Crear vehículo
- `GET /{id}` - Obtener vehículo
- `PUT /{id}` - Actualizar vehículo
- `DELETE /{id}` - Eliminar vehículo
- `GET /{id}/propietarios/` - Propietarios de un vehículo
- `POST /{id}/propietarios/` - Asignar propietario

---

**¡La aplicación está lista para usar con Docker!** 🚀

