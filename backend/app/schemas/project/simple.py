"""
Schema para RESPUESTA SIMPLE de proyecto (sin actividades)
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectSimpleResponse(BaseModel):
    """
    Respuesta básica sin actividades.
    Se usa en listados de proyectos (GET /projects)
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    created_at: datetime
