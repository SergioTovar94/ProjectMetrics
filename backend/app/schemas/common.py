"""
Schemas base que son reutilizados por Activity y Project
"""

from pydantic import BaseModel, Field


class EVMIndicators(BaseModel):
    """
    Indicadores EVM calculados (reutilizado en Activity y Project)
    """

    bac: float = Field(..., description="Budget at Completion")
    pv: float = Field(..., description="Planned Value")
    ev: float = Field(..., description="Earned Value")
    ac: float = Field(..., description="Actual Cost")

    cv: float = Field(..., description="Cost Variance")
    sv: float = Field(..., description="Schedule Variance")

    cpi: float = Field(..., description="Cost Performance Index")
    spi: float = Field(..., description="Schedule Performance Index")

    eac: float = Field(..., description="Estimate at Completion")
    vac: float = Field(..., description="Variance at Completion")

    cost_status: str = Field(
        ..., description="bajo presupuesto / sobre presupuesto / en presupuesto"
    )

    schedule_status: str = Field(
        ..., description="adelantado / atrasado / en cronograma"
    )
