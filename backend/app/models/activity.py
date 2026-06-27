from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.project import Project


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    budget_at_completion: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    planned_progress: Mapped[float] = mapped_column(
        nullable=False,
    )

    actual_progress: Mapped[float] = mapped_column(
        nullable=False,
    )

    actual_cost: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        back_populates="activities",
    )
