"""
Schema para CREAR un proyecto
"""

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None)
