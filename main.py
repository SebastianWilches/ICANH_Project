import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import create_tables
from app.routes import marca_vehiculo, persona, vehiculo

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI con configuración desde variables de entorno
app = FastAPI(
    title=os.getenv("APP_TITLE", "API de Gestión de Vehículos - ICANH"),
    description=os.getenv("APP_DESCRIPTION", """
    API RESTful para la gestión de vehículos, marcas, personas y sus relaciones.

    ## Características principales:

    - **Gestión de Marcas de Vehículo**: CRUD completo para marcas con validación de unicidad
    - **Gestión de Personas**: CRUD completo para personas con validación de cédula única
    - **Gestión de Vehículos**: CRUD completo con relación a marcas
    - **Relaciones Many-to-Many**: Gestión de propietarios de vehículos

    ## Endpoints disponibles:

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
    """),
    version=os.getenv("APP_VERSION", "1.0.0"),
    contact={
        "name": os.getenv("APP_CONTACT_NAME", "Jhoan Sebastian Wilches Jimenez"),
        "email": os.getenv("APP_CONTACT_EMAIL", "sebastianwilches2@gmail.com"),
    },
    license_info={
        "name": "MIT",
    },
)

# Configurar CORS con variables de entorno
allow_origins = os.getenv("ALLOW_ORIGINS", "*")
if isinstance(allow_origins, str) and allow_origins != "*":
    # Si es una lista en formato string, convertirla a lista
    import ast
    try:
        allow_origins = ast.literal_eval(allow_origins)
    except (ValueError, SyntaxError):
        allow_origins = [allow_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins if isinstance(allow_origins, list) else [allow_origins],
    allow_credentials=os.getenv("ALLOW_CREDENTIALS", "True").lower() == "true",
    allow_methods=os.getenv("ALLOW_METHODS", "*").split(",") if os.getenv("ALLOW_METHODS", "*") != "*" else ["*"],
    allow_headers=os.getenv("ALLOW_HEADERS", "*").split(",") if os.getenv("ALLOW_HEADERS", "*") != "*" else ["*"],
)

# Incluir routers
app.include_router(marca_vehiculo.router)
app.include_router(persona.router)
app.include_router(vehiculo.router)


@app.on_event("startup")
def startup_event():
    """Crear las tablas de la base de datos al iniciar la aplicación"""
    create_tables()


@app.get("/", summary="Bienvenida", tags=["General"])
def read_root():
    """
    Endpoint de bienvenida de la API.

    Retorna información básica sobre la API.
    """
    return {
        "message": "Bienvenido a la API de Gestión de Vehículos - ICANH",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", summary="Health Check", tags=["General"])
def health_check():
    """
    Endpoint para verificar el estado de la API.

    Retorna el estado actual del servicio.
    """
    return {"status": "healthy", "message": "API funcionando correctamente"}
