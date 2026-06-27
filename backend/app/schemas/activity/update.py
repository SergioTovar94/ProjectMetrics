"""
Schema para ACTUALIZAR una actividad
"""

from pydantic import BaseModel, Field


class ActivityUpdate(BaseModel):
    """
    Campos opcionales para actualizar una actividad.
    El cliente puede enviar solo los campos que quiere modificar.
    """

    name: str | None = Field(None, min_length=1, max_length=255)
    bac: float | None = Field(None, gt=0)
    planned_progress: float | None = Field(None, ge=0.0, le=1.0)
    actual_progress: float | None = Field(None, ge=0.0, le=1.0)
    ac: float | None = Field(None, ge=0.0)
