from pydantic import BaseModel, Field
from typing import List, Optional


# Esquemas para MarcaVehiculo
class MarcaVehiculoBase(BaseModel):
    nombre_marca: str = Field(..., min_length=1, description="Nombre único de la marca")
    pais: str = Field(..., min_length=1, description="País de origen de la marca")


class MarcaVehiculoCreate(MarcaVehiculoBase):
    pass


class MarcaVehiculoUpdate(BaseModel):
    nombre_marca: Optional[str] = None
    pais: Optional[str] = None


class MarcaVehiculo(MarcaVehiculoBase):
    id: int

    class Config:
        from_attributes = True


# Esquemas para Persona
class PersonaBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre completo de la persona")
    cedula: str = Field(..., min_length=1, description="Número de cédula único")


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(BaseModel):
    nombre: Optional[str] = None
    cedula: Optional[str] = None


class Persona(PersonaBase):
    id: int

    class Config:
        from_attributes = True


# Esquemas para Vehiculo
class VehiculoBase(BaseModel):
    modelo: str = Field(..., min_length=1, description="Modelo del vehículo")
    marca_id: int = Field(..., gt=0, description="ID de la marca del vehículo")
    numero_puertas: int = Field(..., ge=2, le=5, description="Número de puertas (2-5)")
    color: str = Field(..., min_length=1, description="Color del vehículo")


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoUpdate(BaseModel):
    modelo: Optional[str] = None
    marca_id: Optional[int] = None
    numero_puertas: Optional[int] = None
    color: Optional[str] = None


class Vehiculo(VehiculoBase):
    id: int
    marca: Optional[MarcaVehiculo] = None
    propietarios: List[Persona] = []

    class Config:
        from_attributes = True


# Esquemas para relaciones
class VehiculoConPropietarios(Vehiculo):
    propietarios: List[Persona] = []


class PersonaConVehiculos(Persona):
    vehiculos: List[Vehiculo] = []


# Esquema para asignar propietario a vehiculo
class AsignarPropietario(BaseModel):
    persona_id: int
