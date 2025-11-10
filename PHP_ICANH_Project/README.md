# API de Gestión de Vehículos - ICANH (Laravel)

API RESTful desarrollada con Laravel y SQLite para la gestión de vehículos, marcas, personas y sus relaciones.

## 🚀 Características

- **Framework**: Laravel 12.x
- **Base de datos**: SQLite
- **ORM**: Eloquent
- **Validación**: Form Request Classes
- **Documentación**: Swagger UI automática (L5-Swagger)
- **Testing**: PHPUnit con factories y RefreshDatabase
- **Arquitectura**: MVC con separación clara de responsabilidades

## 📊 Diagrama de Base de Datos

```mermaid
erDiagram
    MarcaVehiculo ||--o{ Vehiculo : "tiene"
    Persona ||--o{ Vehiculo_Persona : "posee"
    Vehiculo ||--o{ Vehiculo_Persona : "es_poseido_por"

    MarcaVehiculo {
        integer id PK
        string nombre_marca UK "Nombre único de la marca"
        string pais "País de origen"
    }

    Persona {
        integer id PK
        string nombre "Nombre completo"
        string cedula UK "Cédula única"
    }

    Vehiculo {
        integer id PK
        string modelo "Modelo del vehículo"
        integer marca_id FK "Referencia a MarcaVehiculo"
        integer numero_puertas "Número de puertas"
        string color "Color del vehículo"
    }

    Vehiculo_Persona {
        integer vehiculo_id FK "Referencia a Vehiculo"
        integer persona_id FK "Referencia a Persona"
        PRIMARY KEY(vehiculo_id, persona_id) "Clave compuesta"
    }
```

## 🏗️ Estructura del Proyecto

```
PHP_ICANH_Project/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── GeneralController.php
│   │   │   ├── MarcaVehiculoController.php
│   │   │   ├── PersonaController.php
│   │   │   └── VehiculoController.php
│   │   └── Requests/
│   │       ├── AssignPropietarioRequest.php
│   │       ├── StoreMarcaVehiculoRequest.php
│   │       ├── StorePersonaRequest.php
│   │       ├── StoreVehiculoRequest.php
│   │       ├── UpdateMarcaVehiculoRequest.php
│   │       ├── UpdatePersonaRequest.php
│   │       └── UpdateVehiculoRequest.php
│   ├── Models/
│   │   ├── MarcaVehiculo.php
│   │   ├── Persona.php
│   │   └── Vehiculo.php
│   └── database.sqlite
├── database/
│   ├── factories/
│   │   ├── MarcaVehiculoFactory.php
│   │   ├── PersonaFactory.php
│   │   └── VehiculoFactory.php
│   └── migrations/
│       ├── 2025_11_10_232533_create_marca_vehiculo_table.php
│       ├── 2025_11_10_232539_create_persona_table.php
│       ├── 2025_11_10_232544_create_vehiculo_table.php
│       └── 2025_11_10_232549_create_vehiculo_persona_table.php
├── routes/
│   └── api.php
├── tests/
│   └── Feature/
│       ├── Models/
│       │   └── MarcaVehiculoTest.php
│       └── MarcaVehiculoRoutesTest.php
└── config/
    ├── app.php
    ├── cors.php
    └── l5-swagger.php
```

## 📋 Requisitos

- **PHP 8.2+**
- **Composer**
- **SQLite** (incluido con PHP)

## 🛠️ Instalación y Configuración

### 1. Instalar dependencias
```bash
composer install
```

### 2. Configurar entorno
```bash
# Copiar archivo de configuración
cp .env.example .env

# Generar key de aplicación
php artisan key:generate
```

### 3. Ejecutar migraciones
```bash
php artisan migrate
```

### 4. Ejecutar la aplicación
```bash
php artisan serve
```

### 5. Acceder a la aplicación
- **API**: `http://localhost:8000/api/`
- **Documentación Swagger**: `http://localhost:8000/api/documentation`

## 🌍 Variables de Entorno

El proyecto utiliza las mismas variables de entorno que el proyecto Python:

```env
# Configuración personalizada para ICANH
APP_TITLE="API de Gestión de Vehículos - ICANH"
APP_DESCRIPTION="API RESTful para la gestión de vehículos, marcas, personas y sus relaciones"
APP_VERSION=1.0.0
APP_CONTACT_NAME="Jhoan Sebastian Wilches Jimenez"
APP_CONTACT_EMAIL=sebastianwilches2@gmail.com

# Configuración del Servidor
HOST=0.0.0.0
PORT=8000
RELOAD=True

# Configuración de Desarrollo
DEBUG=True
ENVIRONMENT=development

# Configuración de CORS
ALLOW_ORIGINS=*
ALLOW_CREDENTIALS=True
ALLOW_METHODS=*
ALLOW_HEADERS=*
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
php artisan test

# Tests específicos
php artisan test --filter=MarcaVehiculoRoutesTest
php artisan test --filter=MarcaVehiculoTest
```

### Tests Implementados
- ✅ **Modelos**: Constraints únicos, relaciones
- ✅ **Endpoints REST**: CRUD completo
- ✅ **Validación**: Request classes
- ✅ **Relaciones Many-to-Many**: Asignación de propietarios

## 📚 API Endpoints

### Marcas de Vehículo
- `GET /api/marcas-vehiculo/` - Listar todas las marcas
- `POST /api/marcas-vehiculo/` - Crear nueva marca
- `GET /api/marcas-vehiculo/{id}` - Obtener marca por ID
- `PUT /api/marcas-vehiculo/{id}` - Actualizar marca
- `DELETE /api/marcas-vehiculo/{id}` - Eliminar marca

### Personas
- `GET /api/personas/` - Listar todas las personas
- `POST /api/personas/` - Crear nueva persona
- `GET /api/personas/{id}` - Obtener persona por ID
- `PUT /api/personas/{id}` - Actualizar persona
- `DELETE /api/personas/{id}` - Eliminar persona
- `GET /api/personas/{id}/vehiculos/` - Obtener vehículos de una persona

### Vehículos
- `GET /api/vehiculos/` - Listar todos los vehículos
- `POST /api/vehiculos/` - Crear nuevo vehículo
- `GET /api/vehiculos/{id}` - Obtener vehículo por ID
- `PUT /api/vehiculos/{id}` - Actualizar vehículo
- `DELETE /api/vehiculos/{id}` - Eliminar vehículo
- `GET /api/vehiculos/{id}/propietarios/` - Obtener propietarios de un vehículo
- `POST /api/vehiculos/{id}/propietarios/` - Asignar propietario a vehículo

### Endpoints Generales
- `GET /api/` - Bienvenida
- `GET /api/health` - Health check
- `GET /api/docs` - Redirección a documentación
- `GET /api/redoc` - Redirección a documentación

## 🔍 Validaciones Implementadas

### MarcaVehiculo
- `nombre_marca`: Requerido, único, string mínimo 1 caracter
- `pais`: Requerido, string mínimo 1 caracter

### Persona
- `nombre`: Requerido, string mínimo 1 caracter
- `cedula`: Requerido, único, string mínimo 1 caracter

### Vehiculo
- `modelo`: Requerido, string mínimo 1 caracter
- `marca_id`: Requerido, debe existir en MarcaVehiculo
- `numero_puertas`: Requerido, integer entre 2 y 5
- `color`: Requerido, string mínimo 1 caracter

### Relaciones
- Una marca puede tener múltiples vehículos (One-to-Many)
- Una persona puede tener múltiples vehículos (Many-to-Many)
- Un vehículo puede tener múltiples propietarios (Many-to-Many)
- Validación de existencia de entidades relacionadas
- Prevención de duplicados en relaciones Many-to-Many

## 🤝 Comparación con Proyecto Python

| Aspecto | Python (FastAPI) | PHP (Laravel) |
|---------|------------------|---------------|
| Framework | FastAPI + SQLAlchemy | Laravel + Eloquent |
| Base de datos | SQLite | SQLite |
| Validación | Pydantic | Form Request Classes |
| Testing | pytest + faker | PHPUnit + factories |
| Documentación | Swagger automático | L5-Swagger |
| CORS | Middleware personalizado | Laravel Sanctum |
| Serialización | Pydantic models | Eloquent API Resources |

## 📞 Soporte

Para soporte técnico:
- **Email**: sebastianwilches2@gmail.com
- **Dev**: Jhoan Sebastian Wilches Jimenez

---

**Desarrollado con ❤️ para el ICANH**