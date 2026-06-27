from dataclasses import dataclass
from typing import Any


@dataclass
class ActivityEVM:
    """Resultados EVM para una actividad individual"""

    activity_id: int
    activity_name: str
    bac: float
    planned_progress: float
    actual_progress: float
    actual_cost: float

    # Indicadores calculados
    pv: float  # Planned Value
    ev: float  # Earned Value
    cv: float  # Cost Variance
    sv: float  # Schedule Variance
    cpi: float  # Cost Performance Index
    spi: float  # Schedule Performance Index
    eac: float  # Estimate at Completion
    vac: float  # Variance at Completion

    # Interpretaciones
    cost_status: str
    schedule_status: str


@dataclass
class ProjectEVM:
    """Resultados EVM consolidados para un proyecto"""

    project_id: int
    project_name: str
    total_bac: float
    total_pv: float
    total_ev: float
    total_ac: float
    cv: float
    sv: float
    cpi: float
    spi: float
    eac: float
    vac: float
    cost_status: str
    schedule_status: str
    activities: list[ActivityEVM]


class EVMCalculator:
    """
    Calculadora de indicadores de Earned Value Management (EVM)

    Fórmulas implementadas:
    - PV = Planned Progress % * BAC
    - EV = Actual Progress % * BAC
    - CV = EV - AC
    - SV = EV - PV
    - CPI = EV / AC (con manejo de división por cero)
    - SPI = EV / PV (con manejo de división por cero)
    - EAC = BAC / CPI (con manejo de división por cero)
    - VAC = BAC - EAC
    """

    @staticmethod
    def _to_float(value: Any, default: float = 0.0) -> float:
        """Convierte un valor a float, con default seguro"""
        return float(value) if value else default

    @staticmethod
    def _calculate_indicators(
        bac: float, pv: float, ev: float, actual_cost: float
    ) -> dict[str, float]:
        """
        Calcula los indicadores derivados: CV, SV, CPI, SPI, EAC, VAC
        """
        cv = ev - actual_cost
        sv = ev - pv

        # CPI (con manejo de división por cero)
        cpi = ev / actual_cost if actual_cost > 0 else 1.0

        # SPI (con manejo de división por cero)
        spi = ev / pv if pv > 0 else 1.0

        # EAC (con manejo de división por cero)
        eac = bac / cpi if cpi > 0 else bac

        # VAC
        vac = bac - eac

        return {
            "cv": cv,
            "sv": sv,
            "cpi": cpi,
            "spi": spi,
            "eac": eac,
            "vac": vac,
        }

    @staticmethod
    def calculate_activity_evm(
        activity_id: int,
        name: str,
        bac: float,
        planned_progress: float,
        actual_progress: float,
        actual_cost: float,
    ) -> ActivityEVM:
        """Calcula todos los indicadores EVM para una actividad individual"""
        # Validar entradas
        bac = EVMCalculator._to_float(bac)
        planned_progress = EVMCalculator._to_float(planned_progress)
        actual_progress = EVMCalculator._to_float(actual_progress)
        actual_cost = EVMCalculator._to_float(actual_cost)

        # PV y EV (fórmulas base)
        pv = planned_progress * bac
        ev = actual_progress * bac

        # Indicadores derivados
        indicators = EVMCalculator._calculate_indicators(bac, pv, ev, actual_cost)

        return ActivityEVM(
            activity_id=activity_id,
            activity_name=name,
            bac=round(bac, 2),
            planned_progress=planned_progress,
            actual_progress=actual_progress,
            actual_cost=round(actual_cost, 2),
            pv=round(pv, 2),
            ev=round(ev, 2),
            cv=round(indicators["cv"], 2),
            sv=round(indicators["sv"], 2),
            cpi=round(indicators["cpi"], 2),
            spi=round(indicators["spi"], 2),
            eac=round(indicators["eac"], 2),
            vac=round(indicators["vac"], 2),
            cost_status=EVMCalculator._interpret_cpi(indicators["cpi"]),
            schedule_status=EVMCalculator._interpret_spi(indicators["spi"]),
        )

    @staticmethod
    def calculate_project_evm(
        project_id: int, project_name: str, activities_data: list[dict[str, Any]]
    ) -> ProjectEVM:
        """Calcula indicadores EVM consolidados para un proyecto"""
        if not activities_data:
            return ProjectEVM(
                project_id=project_id,
                project_name=project_name,
                total_bac=0.0,
                total_pv=0.0,
                total_ev=0.0,
                total_ac=0.0,
                cv=0.0,
                sv=0.0,
                cpi=1.0,
                spi=1.0,
                eac=0.0,
                vac=0.0,
                cost_status="sin actividades",
                schedule_status="sin actividades",
                activities=[],
            )

        # Calcular cada actividad y acumular
        activity_results = []
        total_bac = 0.0
        total_pv = 0.0
        total_ev = 0.0
        total_ac = 0.0

        for activity in activities_data:
            result = EVMCalculator.calculate_activity_evm(
                activity_id=EVMCalculator._to_float(activity.get("id", 0), 0),
                name=activity.get("name", ""),
                bac=EVMCalculator._to_float(activity.get("bac")),
                planned_progress=EVMCalculator._to_float(
                    activity.get("planned_progress")
                ),
                actual_progress=EVMCalculator._to_float(
                    activity.get("actual_progress")
                ),
                actual_cost=EVMCalculator._to_float(activity.get("actual_cost")),
            )
            activity_results.append(result)
            total_bac += result.bac
            total_pv += result.pv
            total_ev += result.ev
            total_ac += result.actual_cost

        # Calcular indicadores del proyecto (reusa la misma lógica)
        indicators = EVMCalculator._calculate_indicators(
            total_bac, total_pv, total_ev, total_ac
        )

        return ProjectEVM(
            project_id=project_id,
            project_name=project_name,
            total_bac=round(total_bac, 2),
            total_pv=round(total_pv, 2),
            total_ev=round(total_ev, 2),
            total_ac=round(total_ac, 2),
            cv=round(indicators["cv"], 2),
            sv=round(indicators["sv"], 2),
            cpi=round(indicators["cpi"], 2),
            spi=round(indicators["spi"], 2),
            eac=round(indicators["eac"], 2),
            vac=round(indicators["vac"], 2),
            cost_status=EVMCalculator._interpret_cpi(indicators["cpi"]),
            schedule_status=EVMCalculator._interpret_spi(indicators["spi"]),
            activities=activity_results,
        )

    @staticmethod
    def _interpret_cpi(cpi: float) -> str:
        """Interpreta el CPI"""
        if cpi > 1.0:
            return "bajo presupuesto"
        if cpi < 1.0:
            return "sobre presupuesto"
        return "en presupuesto"

    @staticmethod
    def _interpret_spi(spi: float) -> str:
        """Interpreta el SPI"""
        if spi > 1.0:
            return "adelantado"
        if spi < 1.0:
            return "atrasado"
        return "en cronograma"
