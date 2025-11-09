from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


# Tabla de rompimiento para la relación Many-to-Many entre Vehiculo y Persona
vehiculo_persona = Table(
    'vehiculo_persona',
    Base.metadata,
    Column('vehiculo_id', Integer, ForeignKey('vehiculo.id'), primary_key=True),
    Column('persona_id', Integer, ForeignKey('persona.id'), primary_key=True)
)


class MarcaVehiculo(Base):
    __tablename__ = "marca_vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    nombre_marca = Column(String, unique=True, nullable=False)
    pais = Column(String, nullable=False)

    # Relación con Vehiculo
    vehiculos = relationship("Vehiculo", back_populates="marca")


class Persona(Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False)

    # Relación Many-to-Many con Vehiculo a través de la tabla vehiculo_persona
    vehiculos = relationship("Vehiculo", secondary=vehiculo_persona, back_populates="propietarios")


class Vehiculo(Base):
    __tablename__ = "vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String, nullable=False)
    marca_id = Column(Integer, ForeignKey("marca_vehiculo.id"), nullable=False)
    numero_puertas = Column(Integer, nullable=False)
    color = Column(String, nullable=False)

    # Relación con MarcaVehiculo
    marca = relationship("MarcaVehiculo", back_populates="vehiculos")

    # Relación Many-to-Many con Persona a través de la tabla vehiculo_persona
    propietarios = relationship("Persona", secondary=vehiculo_persona, back_populates="vehiculos")
