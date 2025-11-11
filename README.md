# API de Gestión de Vehículos - ICANH

Proyecto desarrollado para ICANH que consiste en dos implementaciones completas de una API RESTful para la gestión de vehículos, marcas, personas y sus relaciones Many-to-Many. Cada versión mantiene exactamente la misma funcionalidad, estructura de base de datos y documentación.

## 🚀 Versiones Disponibles

### Python con FastAPI
- **Framework**: FastAPI con Python 3.8+
- **ORM**: SQLAlchemy 2.0
- **Documentación**: Swagger UI automática
- **Testing**: pytest con 65+ tests y 94% cobertura
- **Contenerización**: Docker completa

### PHP con Laravel
- **Framework**: Laravel 12.x
- **ORM**: Eloquent
- **Documentación**: L5-Swagger (Swagger UI)
- **Testing**: PHPUnit con factories
- **Contenerización**: Docker completa

## 📊 Diagrama de Base de Datos

Ambas versiones utilizan exactamente la misma estructura de base de datos SQLite:

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
        integer vehiculo_id PK FK
        integer persona_id PK FK
    }
```

### 📋 Relaciones Normalizadas

- **MarcaVehiculo → Vehiculo**: Relación **One-to-Many**
  - Una marca puede tener múltiples vehículos
  - Cada vehículo pertenece a una sola marca

- **Persona → Vehiculo_Persona**: Relación **One-to-Many**
  - Una persona puede tener múltiples registros en vehiculo_persona
  - Cada registro vehiculo_persona pertenece a una sola persona

- **Vehiculo → Vehiculo_Persona**: Relación **One-to-Many**
  - Un vehículo puede tener múltiples registros en vehiculo_persona
  - Cada registro vehiculo_persona pertenece a un solo vehículo

La tabla `Vehiculo_Persona` implementa la relación **Many-to-Many** entre `Persona` y `Vehiculo` mediante normalización con una **clave primaria compuesta** (vehiculo_id, persona_id), permitiendo que:
- Una **persona** pueda tener **múltiples vehículos**
- Un **vehículo** pueda tener **múltiples propietarios**

## 🛠️ Instalación y Configuración

### Requisitos Generales
- **Git**: Para clonar el repositorio
- **Docker** (opcional): Para ejecutar con contenedores

### Proyecto Python (FastAPI)

#### 📋 Requisitos Específicos
- **Python 3.8+** (probado con Python 3.13.7 en Windows)
- **pip**: Gestor de paquetes de Python

#### 🚀 Instalación Rápida
```bash
# Navegar al proyecto Python
cd ICANH_Project/Python_ICANH_Project

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python run.py
```

#### 🐳 Con Docker (Recomendado)
```bash
# Navegar al proyecto Python
cd ICANH_Project/Python_ICANH_Project

# Construir y ejecutar
docker-compose up --build

# O para desarrollo
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

### Proyecto PHP (Laravel)

#### 📋 Requisitos Específicos
- **PHP 8.2+**
- **Composer**: Gestor de dependencias de PHP

#### 🚀 Instalación Rápida
```bash
# Navegar al proyecto PHP
cd ICANH_Project/PHP_ICANH_Project

# Instalar dependencias
composer install

# Configurar entorno
cp .env.example .env
php artisan key:generate

# Ejecutar migraciones
php artisan migrate

# Ejecutar la aplicación
php artisan serve
```

#### 🐳 Con Docker (Recomendado)
```bash
# Navegar al proyecto PHP
cd ICANH_Project/PHP_ICANH_Project

# Construir y ejecutar
docker-compose up --build
```

## 🧪 Ejecutar Tests

### Proyecto Python
```bash
# Navegar al proyecto
cd ICANH_Project/Python_ICANH_Project

# Ejecutar todos los tests (recomendado)
python run_tests.py

# O ejecutar manualmente
pytest

# Con reporte de cobertura
pytest --cov=app --cov-report=html
```

### Proyecto PHP
```bash
# Navegar al proyecto
cd ICANH_Project/PHP_ICANH_Project

# Ejecutar todos los tests
php artisan test

# Tests específicos
php artisan test --filter=MarcaVehiculoRoutesTest
```

## 🌐 Acceder a las Aplicaciones

### Proyecto Python
- **API**: `http://localhost:8000`
- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### Proyecto PHP
- **API**: `http://localhost:8000/api/`
- **Documentación Swagger**: `http://localhost:8000/api/documentation`
- **Health Check**: `http://localhost:8000/api/health`

## 📚 API Endpoints

Ambas versiones implementan exactamente los mismos endpoints:

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

## 🧪 Testing con Postman

Ambas versiones son completamente compatibles con la colección de Postman incluida:

- **Archivo**: `ICANH_Project/Python_ICANH_Project/ICANH_Vehiculos_Postman_Collection.json`
- **Uso**: Importar en Postman para testing completo de todos los endpoints
- **Configuración**: Ajustar la variable `base_url` según el proyecto en uso

## 📖 Documentación Detallada

Para información técnica completa, consultar la documentación específica de cada proyecto:

- [**📚 Documentación Python (FastAPI)**](ICANH_Project/Python_ICANH_Project/README.md)
- [**📚 Documentación PHP (Laravel)**](ICANH_Project/PHP_ICANH_Project/README.md)
- [**🤖 Uso de IA en el Desarrollo**](IA_USAGE.md)

## 🔍 Validaciones Implementadas

### MarcaVehiculo
- `nombre_marca`: Requerido, único, string
- `pais`: Requerido, string

### Persona
- `nombre`: Requerido, string
- `cedula`: Requerido, único, string

### Vehiculo
- `modelo`: Requerido, string
- `marca_id`: Requerido, debe existir en MarcaVehiculo
- `numero_puertas`: Requerido, integer
- `color`: Requerido, string

### Relaciones
- Una marca puede tener múltiples vehículos
- Una persona puede tener múltiples vehículos (Many-to-Many)
- Un vehículo puede tener múltiples propietarios (Many-to-Many)
- Validación de existencia de entidades relacionadas
- Prevención de duplicados en relaciones Many-to-Many

## 👨‍💻 Desarrollador

**Jhoan Sebastian Wilches Jimenez**
- **Email**: sebastianwilches2@gmail.com
- **Rol**: Developer

---

**Desarrollado con ❤️ para el ICANH**
