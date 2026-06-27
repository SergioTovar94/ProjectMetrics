"""
Schema para CREAR una actividad
"""

from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):
    """
    Campos requeridos para crear una actividad.
    Todos son obligatorios porque una actividad sin estos datos no tiene sentido.
    """

    project_id: int = Field(..., gt=0, description="ID del proyecto")
    name: str = Field(..., min_length=1, max_length=255, description="Nombre")
    bac: float = Field(..., gt=0, description="Budget at Completion")
    planned_progress: float = Field(..., ge=0.0, le=1.0, description="% planificado")
    actual_progress: float = Field(..., ge=0.0, le=1.0, description="% real")
    ac: float = Field(..., ge=0.0, description="Costo real")
