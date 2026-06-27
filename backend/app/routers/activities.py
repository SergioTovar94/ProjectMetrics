# backend/app/routers/activities.py
"""
Endpoints CRUD para Actividades
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.activity import Activity
from app.models.project import Project
from app.schemas.activity import (
    ActivityCreate,
    ActivityResponse,
    ActivityUpdate,
)
from app.utils.response_builders import build_activity_response

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post(
    "/",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva actividad",
    description="Crea una nueva actividad asociada a un proyecto",
)
def create_activity(activity_data: ActivityCreate, db: Session = Depends(get_db)):
    """Crea una nueva actividad"""
    project = db.query(Project).filter(Project.id == activity_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
        )

    existing = (
        db.query(Activity)
        .filter(
            Activity.project_id == activity_data.project_id,
            Activity.name == activity_data.name,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una actividad con este nombre en el proyecto",
        )

    new_activity = Activity(
        project_id=activity_data.project_id,
        name=activity_data.name,
        bac=activity_data.bac,
        planned_progress=activity_data.planned_progress,
        actual_progress=activity_data.actual_progress,
        actual_cost=activity_data.actual_cost,
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return build_activity_response(new_activity)


@router.get(
    "/project/{project_id}",
    response_model=list[ActivityResponse],
    summary="Listar actividades de un proyecto",
    description="Retorna todas las actividades de un proyecto con sus indicadores EVM",
)
def list_activities_by_project(
    project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Lista todas las actividades de un proyecto con EVM"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado"
        )

    activities = (
        db.query(Activity)
        .filter(Activity.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [build_activity_response(activity) for activity in activities]


@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Obtener actividad por ID",
    description="Retorna una actividad con todos sus indicadores EVM",
)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Obtiene una actividad por su ID con EVM"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Actividad no encontrada"
        )

    return build_activity_response(activity)


@router.patch(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Actualizar actividad",
    description="Actualiza los datos de una actividad existente",
)
def update_activity(
    activity_id: int, activity_data: ActivityUpdate, db: Session = Depends(get_db)
):
    """Actualiza una actividad existente"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Actividad no encontrada"
        )

    if activity_data.name and activity_data.name != activity.name:
        existing = (
            db.query(Activity)
            .filter(
                Activity.project_id == activity.project_id,
                Activity.name == activity_data.name,
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una actividad con este nombre en el proyecto",
            )

    if activity_data.name is not None:
        activity.name = activity_data.name
    if activity_data.bac is not None:
        activity.bac = activity_data.bac
    if activity_data.planned_progress is not None:
        activity.planned_progress = activity_data.planned_progress
    if activity_data.actual_progress is not None:
        activity.actual_progress = activity_data.actual_progress
    if activity_data.actual_cost is not None:
        activity.actual_cost = activity_data.actual_cost

    db.commit()
    db.refresh(activity)

    return build_activity_response(activity)


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar actividad",
    description="Elimina una actividad",
)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """Elimina una actividad"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Actividad no encontrada"
        )

    db.delete(activity)
    db.commit()
