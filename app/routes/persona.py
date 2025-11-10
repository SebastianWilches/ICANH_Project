from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..database.database import get_db
from ..models.models import Persona as PersonaModel, Vehiculo
from ..schemas.schemas import (
    Persona,
    PersonaCreate,
    PersonaUpdate,
    PersonaConVehiculos
)

router = APIRouter(
    prefix="/api/personas",
    tags=["Personas"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Persona, summary="Crear una nueva persona")
def create_persona(
    persona: PersonaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva persona.

    - **nombre**: Nombre completo de la persona
    - **cedula**: Número de cédula único
    """
    # Verificar si ya existe una persona con la misma cédula
    db_persona = db.query(PersonaModel).filter(
        PersonaModel.cedula == persona.cedula
    ).first()
    if db_persona:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una persona con esa cédula"
        )

    db_persona = PersonaModel(
        nombre=persona.nombre,
        cedula=persona.cedula
    )
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona


@router.get("/", response_model=List[Persona], summary="Obtener todas las personas")
def read_personas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener una lista de todas las personas.

    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Número máximo de registros a devolver
    """
    personas = db.query(PersonaModel).offset(skip).limit(limit).all()
    return personas


@router.get("/{persona_id}", response_model=Persona, summary="Obtener una persona por ID")
def read_persona(
    persona_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una persona específica por su ID.

    - **persona_id**: ID de la persona a obtener
    """
    db_persona = db.query(PersonaModel).filter(
        PersonaModel.id == persona_id
    ).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return db_persona


@router.put("/{persona_id}", response_model=Persona, summary="Actualizar una persona")
def update_persona(
    persona_id: int,
    persona_update: PersonaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una persona existente.

    - **persona_id**: ID de la persona a actualizar
    - **persona_update**: Datos a actualizar
    """
    db_persona = db.query(PersonaModel).filter(
        PersonaModel.id == persona_id
    ).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    # Verificar si la nueva cédula ya existe (solo si se está cambiando)
    if persona_update.cedula and persona_update.cedula != db_persona.cedula:
        existing_persona = db.query(PersonaModel).filter(
            PersonaModel.cedula == persona_update.cedula
        ).first()
        if existing_persona:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una persona con esa cédula"
            )

    # Actualizar campos proporcionados
    for field, value in persona_update.dict(exclude_unset=True).items():
        setattr(db_persona, field, value)

    db.commit()
    db.refresh(db_persona)
    return db_persona


@router.delete("/{persona_id}", summary="Eliminar una persona")
def delete_persona(
    persona_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una persona.

    - **persona_id**: ID de la persona a eliminar
    """
    db_persona = db.query(PersonaModel).filter(
        PersonaModel.id == persona_id
    ).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    # Verificar si la persona tiene vehículos asociados
    if db_persona.vehiculos:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la persona porque tiene vehículos asociados"
        )

    db.delete(db_persona)
    db.commit()
    return {"message": "Persona eliminada exitosamente"}


@router.get("/{persona_id}/vehiculos", response_model=PersonaConVehiculos, summary="Obtener vehículos de una persona")
def read_persona_vehiculos(
    persona_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los vehículos de una persona específica.

    - **persona_id**: ID de la persona
    """
    db_persona = db.query(PersonaModel).options(
        joinedload(PersonaModel.vehiculos).joinedload(Vehiculo.marca)
    ).filter(PersonaModel.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return db_persona
