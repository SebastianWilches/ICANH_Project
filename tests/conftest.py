import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import Base, get_db
from app.models.models import MarcaVehiculo, Persona, Vehiculo
import main
from faker import Faker

# Cargar variables de entorno para pruebas
load_dotenv()

# Configuración de base de datos para pruebas
TEST_DATABASE_URL = "sqlite:///./test_vehiculos.db"

# Crear engine de prueba
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Habilitar foreign keys en SQLite para tests
from sqlalchemy import event

@event.listens_for(test_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Crear SessionLocal para pruebas
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Fixture que proporciona una sesión de base de datos limpia para cada test"""
    # Crear todas las tablas
    Base.metadata.create_all(bind=test_engine)

    # Crear sesión
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()

    # Limpiar tablas después de cada test
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def faker():
    """Fixture que proporciona un generador de datos falsos"""
    return Faker('es_ES')  # Datos en español


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de pruebas para FastAPI"""
    from fastapi.testclient import TestClient

    # Asegurar que las tablas estén creadas
    Base.metadata.create_all(bind=test_engine)

    # Override the dependency to use the test database
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    main.app.dependency_overrides[get_db] = override_get_db

    with TestClient(main.app) as test_client:
        yield test_client

    # Limpiar overrides después del test
    main.app.dependency_overrides.clear()

    # Limpiar tablas después del test
    Base.metadata.drop_all(bind=test_engine)


# Fixtures para crear datos de prueba
@pytest.fixture
def sample_marca(db_session, faker):
    """Fixture que crea y retorna una marca de vehículo de prueba"""
    marca = MarcaVehiculo(
        nombre_marca=faker.company(),
        pais=faker.country()
    )
    db_session.add(marca)
    db_session.commit()
    db_session.refresh(marca)
    return marca


@pytest.fixture
def sample_persona(db_session, faker):
    """Fixture que crea y retorna una persona de prueba"""
    persona = Persona(
        nombre=faker.name(),
        cedula=str(faker.random_number(digits=10, fix_len=True))
    )
    db_session.add(persona)
    db_session.commit()
    db_session.refresh(persona)
    return persona


@pytest.fixture
def sample_vehiculo(db_session, sample_marca, faker):
    """Fixture que crea y retorna un vehículo de prueba"""
    vehiculo = Vehiculo(
        modelo=faker.word().capitalize(),
        marca_id=sample_marca.id,
        numero_puertas=faker.random_element([2, 3, 4, 5]),
        color=faker.color_name()
    )
    db_session.add(vehiculo)
    db_session.commit()
    db_session.refresh(vehiculo)
    return vehiculo


@pytest.fixture
def multiple_marcas(db_session, faker):
    """Fixture que crea múltiples marcas para pruebas"""
    marcas = []
    for _ in range(3):
        marca = MarcaVehiculo(
            nombre_marca=faker.company(),
            pais=faker.country()
        )
        db_session.add(marca)
        marcas.append(marca)
    db_session.commit()
    for marca in marcas:
        db_session.refresh(marca)
    return marcas


@pytest.fixture
def multiple_personas(db_session, faker):
    """Fixture que crea múltiples personas para pruebas"""
    personas = []
    for _ in range(3):
        persona = Persona(
            nombre=faker.name(),
            cedula=str(faker.random_number(digits=10, fix_len=True))
        )
        db_session.add(persona)
        personas.append(persona)
    db_session.commit()
    for persona in personas:
        db_session.refresh(persona)
    return personas


@pytest.fixture
def vehiculo_con_propietario(db_session, sample_vehiculo, sample_persona):
    """Fixture que crea un vehículo con un propietario asignado"""
    sample_vehiculo.propietarios.append(sample_persona)
    db_session.commit()
    db_session.refresh(sample_vehiculo)
    return sample_vehiculo
