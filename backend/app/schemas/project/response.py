"""
Schema para RESPUESTA COMPLETA de proyecto (con actividades y EVM)
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.activity.response import ActivityResponse
from app.schemas.common import EVMIndicators


class ProjectResponse(BaseModel):
    """
    Respuesta completa de un proyecto con sus actividades y EVM consolidado.
    Se usa en GET /projects/{id}
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    created_at: datetime

    activities: list[ActivityResponse] = Field(default_factory=list)

    evm: EVMIndicators | None = Field(None, description="EVM consolidado del proyecto")
