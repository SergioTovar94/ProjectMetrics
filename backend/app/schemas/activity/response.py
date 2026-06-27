"""
Schema para RESPUESTA COMPLETA de actividad (con EVM calculado)
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import EVMIndicators


class ActivityResponse(BaseModel):
    """
    Respuesta completa de una actividad con todos sus datos + EVM.
    Se usa en GET /activities/{id} y GET /projects/{id}/activities
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    bac: float
    planned_progress: float
    actual_progress: float
    ac: float
    created_at: datetime
    updated_at: datetime | None = None

    evm: EVMIndicators = Field(..., description="Indicadores EVM calculados")
