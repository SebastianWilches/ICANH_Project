from pydantic import BaseModel
from typing import List, Optional


# Esquemas para MarcaVehiculo
class MarcaVehiculoBase(BaseModel):
    nombre_marca: str
    pais: str


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
    nombre: str
    cedula: str


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
    modelo: str
    marca_id: int
    numero_puertas: int
    color: str


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
