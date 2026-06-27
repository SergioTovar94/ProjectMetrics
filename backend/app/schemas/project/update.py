"""
Schema para ACTUALIZAR un proyecto
"""

from pydantic import BaseModel, Field


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None)
