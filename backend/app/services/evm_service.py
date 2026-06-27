# backend/app/services/evm_service.py
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
    cost_status: str  # "bajo presupuesto", "sobre presupuesto", "en presupuesto"
    schedule_status: str  # "adelantado", "atrasado", "en cronograma"


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
    def calculate_activity_evm(
        activity_id: int,
        name: str,
        bac: float,
        planned_progress: float,
        actual_progress: float,
        actual_cost: float,
    ) -> ActivityEVM:
        """
        Calcula todos los indicadores EVM para una actividad individual
        """
        # Validar entradas
        bac = float(bac) if bac else 0.0
        planned_progress = float(planned_progress) if planned_progress else 0.0
        actual_progress = float(actual_progress) if actual_progress else 0.0
        actual_cost = float(actual_cost) if actual_cost else 0.0

        # 1. PV (Planned Value)
        pv = planned_progress * bac

        # 2. EV (Earned Value)
        ev = actual_progress * bac

        # 3. CV (Cost Variance)
        cv = ev - actual_cost

        # 4. SV (Schedule Variance)
        sv = ev - pv

        # 5. CPI (Cost Performance Index)
        if actual_cost > 0:
            cpi = ev / actual_cost
        else:
            # Si AC = 0, asumimos CPI = 1.0 (sin costo)
            cpi = 1.0

        # 6. SPI (Schedule Performance Index)
        if pv > 0:
            spi = ev / pv
        else:
            # Si PV = 0, asumimos SPI = 1.0 (sin planificación)
            spi = 1.0

        # 7. EAC (Estimate at Completion)
        if cpi > 0:
            eac = bac / cpi
        else:
            eac = bac  # Si CPI es 0, usar BAC

        # 8. VAC (Variance at Completion)
        vac = bac - eac

        # Interpretaciones
        cost_status = EVMCalculator._interpret_cpi(cpi)
        schedule_status = EVMCalculator._interpret_spi(spi)

        return ActivityEVM(
            activity_id=activity_id,
            activity_name=name,
            bac=round(bac, 2),
            planned_progress=planned_progress,
            actual_progress=actual_progress,
            actual_cost=round(actual_cost, 2),
            pv=round(pv, 2),
            ev=round(ev, 2),
            cv=round(cv, 2),
            sv=round(sv, 2),
            cpi=round(cpi, 2),
            spi=round(spi, 2),
            eac=round(eac, 2),
            vac=round(vac, 2),
            cost_status=cost_status,
            schedule_status=schedule_status,
        )

    @staticmethod
    def calculate_project_evm(
        project_id: int, project_name: str, activities_data: list[dict[str, Any]]
    ) -> ProjectEVM:
        """
        Calcula indicadores EVM consolidados para un proyecto
        Suma todos los valores base y recalcula las fórmulas
        """
        if not activities_data:
            # Proyecto sin actividades
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

        # Sumar valores base de todas las actividades
        total_bac = 0.0
        total_pv = 0.0
        total_ev = 0.0
        total_ac = 0.0
        activity_results = []

        for activity in activities_data:
            # Calcular EVM individual
            result = EVMCalculator.calculate_activity_evm(
                activity_id=activity.get("id", 0),
                name=activity.get("name", ""),
                bac=activity.get("bac", 0.0),
                planned_progress=activity.get("planned_progress", 0.0),
                actual_progress=activity.get("actual_progress", 0.0),
                actual_cost=activity.get("actual_cost", 0.0),
            )
            activity_results.append(result)

            # Acumular para proyecto
            total_bac += result.bac
            total_pv += result.pv
            total_ev += result.ev
            total_ac += result.actual_cost

        # Calcular indicadores del proyecto
        cv = total_ev - total_ac
        sv = total_ev - total_pv

        if total_ac > 0:
            cpi = total_ev / total_ac
        else:
            cpi = 1.0

        if total_pv > 0:
            spi = total_ev / total_pv
        else:
            spi = 1.0

        if cpi > 0:
            eac = total_bac / cpi
        else:
            eac = total_bac

        vac = total_bac - eac

        return ProjectEVM(
            project_id=project_id,
            project_name=project_name,
            total_bac=round(total_bac, 2),
            total_pv=round(total_pv, 2),
            total_ev=round(total_ev, 2),
            total_ac=round(total_ac, 2),
            cv=round(cv, 2),
            sv=round(sv, 2),
            cpi=round(cpi, 2),
            spi=round(spi, 2),
            eac=round(eac, 2),
            vac=round(vac, 2),
            cost_status=EVMCalculator._interpret_cpi(cpi),
            schedule_status=EVMCalculator._interpret_spi(spi),
            activities=activity_results,
        )

    @staticmethod
    def _interpret_cpi(cpi: float) -> str:
        """Interpreta el CPI"""
        if cpi > 1.0:
            return "bajo presupuesto"
        elif cpi < 1.0:
            return "sobre presupuesto"
        else:
            return "en presupuesto"

    @staticmethod
    def _interpret_spi(spi: float) -> str:
        """Interpreta el SPI"""
        if spi > 1.0:
            return "adelantado"
        elif spi < 1.0:
            return "atrasado"
        else:
            return "en cronograma"
