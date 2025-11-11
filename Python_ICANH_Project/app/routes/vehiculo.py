from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..database.database import get_db
from ..models.models import Vehiculo as VehiculoModel, MarcaVehiculo
from ..schemas.schemas import (
    Vehiculo,
    VehiculoCreate,
    VehiculoUpdate,
    VehiculoConPropietarios,
    AsignarPropietario
)

router = APIRouter(
    prefix="/api/vehiculos",
    tags=["Vehículos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Vehiculo, summary="Crear un nuevo vehículo")
def create_vehiculo(
    vehiculo: VehiculoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo vehículo.

    - **modelo**: Modelo del vehículo
    - **marca_id**: ID de la marca del vehículo
    - **numero_puertas**: Número de puertas del vehículo
    - **color**: Color del vehículo
    """
    # Verificar si la marca existe
    db_marca = db.query(MarcaVehiculo).filter(
        MarcaVehiculo.id == vehiculo.marca_id
    ).first()
    if not db_marca:
        raise HTTPException(
            status_code=400,
            detail="La marca especificada no existe"
        )

    db_vehiculo = VehiculoModel(
        modelo=vehiculo.modelo,
        marca_id=vehiculo.marca_id,
        numero_puertas=vehiculo.numero_puertas,
        color=vehiculo.color
    )
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo


@router.get("/", response_model=List[Vehiculo], summary="Obtener todos los vehículos")
def read_vehiculos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener una lista de todos los vehículos con información de su marca.

    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a devolver
    """
    vehiculos = db.query(VehiculoModel).options(
        joinedload(VehiculoModel.marca)
    ).offset(skip).limit(limit).all()
    return vehiculos


@router.get("/{vehiculo_id}", response_model=Vehiculo, summary="Obtener un vehículo por ID")
def read_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un vehículo específico por su ID con información de su marca.

    - **vehiculo_id**: ID del vehículo a obtener
    """
    db_vehiculo = db.query(VehiculoModel).options(
        joinedload(VehiculoModel.marca)
    ).filter(VehiculoModel.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo


@router.put("/{vehiculo_id}", response_model=Vehiculo, summary="Actualizar un vehículo")
def update_vehiculo(
    vehiculo_id: int,
    vehiculo_update: VehiculoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un vehículo existente.

    - **vehiculo_id**: ID del vehículo a actualizar
    - **vehiculo_update**: Datos a actualizar
    """
    db_vehiculo = db.query(VehiculoModel).filter(
        VehiculoModel.id == vehiculo_id
    ).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Verificar si la nueva marca existe (solo si se está cambiando)
    if vehiculo_update.marca_id is not None:
        db_marca = db.query(MarcaVehiculo).filter(
            MarcaVehiculo.id == vehiculo_update.marca_id
        ).first()
        if not db_marca:
            raise HTTPException(
                status_code=400,
                detail="La marca especificada no existe"
            )

    # Actualizar campos proporcionados
    for field, value in vehiculo_update.dict(exclude_unset=True).items():
        setattr(db_vehiculo, field, value)

    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo


@router.delete("/{vehiculo_id}", summary="Eliminar un vehículo")
def delete_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un vehículo.

    - **vehiculo_id**: ID del vehículo a eliminar
    """
    db_vehiculo = db.query(VehiculoModel).filter(
        VehiculoModel.id == vehiculo_id
    ).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    db.delete(db_vehiculo)
    db.commit()
    return {"message": "Vehículo eliminado exitosamente"}


@router.get("/{vehiculo_id}/propietarios", response_model=VehiculoConPropietarios, summary="Obtener propietarios de un vehículo")
def read_vehiculo_propietarios(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los propietarios de un vehículo específico.

    - **vehiculo_id**: ID del vehículo
    """
    db_vehiculo = db.query(VehiculoModel).options(
        joinedload(VehiculoModel.marca),
        joinedload(VehiculoModel.propietarios)
    ).filter(VehiculoModel.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo


@router.post("/{vehiculo_id}/propietarios", summary="Asignar propietario a un vehículo")
def assign_propietario_to_vehiculo(
    vehiculo_id: int,
    asignacion: AsignarPropietario,
    db: Session = Depends(get_db)
):
    """
    Asignar un propietario a un vehículo (relación Many-to-Many).

    - **vehiculo_id**: ID del vehículo
    - **persona_id**: ID de la persona a asignar como propietario
    """
    # Verificar que el vehículo existe
    db_vehiculo = db.query(VehiculoModel).filter(
        VehiculoModel.id == vehiculo_id
    ).first()
    if not db_vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Verificar que la persona existe
    from ..models.models import Persona
    db_persona = db.query(Persona).filter(
        Persona.id == asignacion.persona_id
    ).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    # Verificar si la relación ya existe
    if db_persona in db_vehiculo.propietarios:
        raise HTTPException(
            status_code=400,
            detail="Esta persona ya es propietaria de este vehículo"
        )

    # Agregar la relación
    db_vehiculo.propietarios.append(db_persona)
    db.commit()

    return {"message": "Propietario asignado exitosamente al vehículo"}
