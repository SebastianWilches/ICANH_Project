from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_db
from ..models.models import MarcaVehiculo as MarcaVehiculoModel
from ..schemas.schemas import (
    MarcaVehiculo,
    MarcaVehiculoCreate,
    MarcaVehiculoUpdate
)

router = APIRouter(
    prefix="/api/marcas-vehiculo",
    tags=["Marcas de Vehículo"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=MarcaVehiculo, summary="Crear una nueva marca de vehículo")
def create_marca_vehiculo(
    marca: MarcaVehiculoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva marca de vehículo.

    - **nombre_marca**: Nombre único de la marca
    - **pais**: País de origen de la marca
    """
    # Verificar si ya existe una marca con el mismo nombre
    db_marca = db.query(MarcaVehiculoModel).filter(
        MarcaVehiculoModel.nombre_marca == marca.nombre_marca
    ).first()
    if db_marca:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una marca con ese nombre"
        )

    db_marca = MarcaVehiculoModel(
        nombre_marca=marca.nombre_marca,
        pais=marca.pais
    )
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca


@router.get("/", response_model=List[MarcaVehiculo], summary="Obtener todas las marcas de vehículo")
def read_marcas_vehiculo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener una lista de todas las marcas de vehículo.

    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a devolver
    """
    marcas = db.query(MarcaVehiculoModel).offset(skip).limit(limit).all()
    return marcas


@router.get("/{marca_id}", response_model=MarcaVehiculo, summary="Obtener una marca de vehículo por ID")
def read_marca_vehiculo(
    marca_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una marca de vehículo específica por su ID.

    - **marca_id**: ID de la marca a obtener
    """
    db_marca = db.query(MarcaVehiculoModel).filter(
        MarcaVehiculoModel.id == marca_id
    ).first()
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return db_marca


@router.put("/{marca_id}", response_model=MarcaVehiculo, summary="Actualizar una marca de vehículo")
def update_marca_vehiculo(
    marca_id: int,
    marca_update: MarcaVehiculoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una marca de vehículo existente.

    - **marca_id**: ID de la marca a actualizar
    - **marca_update**: Datos a actualizar
    """
    db_marca = db.query(MarcaVehiculoModel).filter(
        MarcaVehiculoModel.id == marca_id
    ).first()
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    # Verificar si el nuevo nombre ya existe (solo si se está cambiando)
    if marca_update.nombre_marca and marca_update.nombre_marca != db_marca.nombre_marca:
        existing_marca = db.query(MarcaVehiculoModel).filter(
            MarcaVehiculoModel.nombre_marca == marca_update.nombre_marca
        ).first()
        if existing_marca:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una marca con ese nombre"
            )

    # Actualizar campos proporcionados
    for field, value in marca_update.dict(exclude_unset=True).items():
        setattr(db_marca, field, value)

    db.commit()
    db.refresh(db_marca)
    return db_marca


@router.delete("/{marca_id}", summary="Eliminar una marca de vehículo")
def delete_marca_vehiculo(
    marca_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una marca de vehículo.

    - **marca_id**: ID de la marca a eliminar
    """
    db_marca = db.query(MarcaVehiculoModel).filter(
        MarcaVehiculoModel.id == marca_id
    ).first()
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    # Verificar si hay vehículos asociados a esta marca
    if db_marca.vehiculos:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la marca porque tiene vehículos asociados"
        )

    db.delete(db_marca)
    db.commit()
    return {"message": "Marca eliminada exitosamente"}
