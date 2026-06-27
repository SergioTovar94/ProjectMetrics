"""
Endpoints CRUD para Proyectos
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectSimpleResponse,
    ProjectUpdate,
)
from app.utils.response_builders import build_project_response

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo proyecto",
    description="Crea un nuevo proyecto con nombre y descripción opcional",
)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """Crea un nuevo proyecto"""
    existing = db.query(Project).filter(Project.name == project_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un proyecto con este nombre",
        )

    new_project = Project(name=project_data.name, description=project_data.description)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get(
    "/",
    response_model=list[ProjectSimpleResponse],
    summary="Listar todos los proyectos",
    description="Retorna todos los proyectos sin sus actividades",
)
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los proyectos (sin actividades)"""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Obtener proyecto por ID",
    description="Retorna un proyecto con todas sus actividades y EVM consolidado",
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Obtiene un proyecto por su ID con todas las actividades"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
        )

    return build_project_response(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Actualizar proyecto parcialmente",
    description="Actualiza solo los campos enviados del proyecto",
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,  # Todos los campos son Optional
    db: Session = Depends(get_db),
):
    """Actualiza parcialmente un proyecto"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
        )

    if project_data.name is not None and project_data.name != project.name:
        existing = db.query(Project).filter(Project.name == project_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un proyecto con este nombre",
            )

    update_data = project_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar proyecto",
    description="Elimina un proyecto y todas sus actividades (CASCADE)",
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Elimina un proyecto (las actividades se eliminan en cascada)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
        )

    db.delete(project)
    db.commit()
