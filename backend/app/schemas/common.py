"""
Schemas base que son reutilizados por Activity y Project
"""

from pydantic import BaseModel, Field


class EVMIndicators(BaseModel):
    """
    Indicadores EVM calculados (reutilizado en Activity y Project)
    """

    pv: float = Field(..., description="Planned Value - Valor planificado")
    ev: float = Field(..., description="Earned Value - Valor ganado")
    cv: float = Field(..., description="Cost Variance - Variación de costo")
    sv: float = Field(..., description="Schedule Variance - Variación de cronograma")
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
