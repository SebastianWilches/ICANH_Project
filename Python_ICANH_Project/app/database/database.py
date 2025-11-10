import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from ..models.models import Base

# Cargar variables de entorno
load_dotenv()

# Configuración de base de datos desde variables de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vehiculos.db")

# Crear engine con configuraciones específicas para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
