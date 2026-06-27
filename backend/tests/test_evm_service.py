import pytest
from app.services.evm_service import EVMCalculator, ActivityEVM, ProjectEVM


class TestEVMCalculator:
    """Pruebas para el EVMCalculator"""

    def test_calculate_activity_evm_normal_case(self):
        """Caso normal: todos los valores válidos"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=1,
            name="Desarrollo Frontend",
            bac=10000.0,
            planned_progress=0.50,
            actual_progress=0.40,
            actual_cost=6000.0,
        )

        assert isinstance(result, ActivityEVM)

        assert result.activity_id == 1
        assert result.activity_name == "Desarrollo Frontend"
        assert result.bac == 10000.0

        assert result.pv == 5000.0
        assert result.ev == 4000.0
        assert result.cv == -2000.0
        assert result.sv == -1000.0
        assert result.cpi == 0.67
        assert result.spi == 0.80
        assert result.eac == 15000.00
        assert result.vac == -5000.00

        assert result.cost_status == "sobre presupuesto"
        assert result.schedule_status == "atrasado"

    def test_calculate_activity_evm_bajo_presupuesto(self):
        """Caso: proyecto bajo presupuesto (CPI > 1)"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=2,
            name="Backend API",
            bac=15000.0,
            planned_progress=0.60,
            actual_progress=0.70,
            actual_cost=9000.0,
        )

        assert result.ev == 10500.0
        assert result.cpi == 1.17
        assert result.cost_status == "bajo presupuesto"
        assert result.spi == 1.17
        assert result.schedule_status == "adelantado"

    def test_calculate_activity_evm_actual_cost_zero(self):
        """Edge case: AC = 0 (división por cero en CPI)"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=3,
            name="Sin Costo",
            bac=5000.0,
            planned_progress=0.50,
            actual_progress=0.50,
            actual_cost=0.0,
        )

        assert result.pv == 2500.0
        assert result.ev == 2500.0
        assert result.cpi == 1.0
        assert result.eac == 5000.0
        assert result.vac == 0.0

    def test_calculate_activity_evm_planned_value_zero(self):
        """Edge case: PV = 0 (división por cero en SPI)"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=4,
            name="Sin Plan",
            bac=5000.0,
            planned_progress=0.0,
            actual_progress=0.50,
            actual_cost=2000.0,
        )

        assert result.pv == 0.0
        assert result.ev == 2500.0
        assert result.spi == 1.0

    def test_calculate_activity_evm_bac_zero(self):
        """Edge case: BAC = 0"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=5,
            name="Sin Presupuesto",
            bac=0.0,
            planned_progress=0.50,
            actual_progress=0.50,
            actual_cost=1000.0,
        )

        assert result.bac == 0.0
        assert result.pv == 0.0
        assert result.ev == 0.0
        assert result.cpi == 0.0
        assert result.eac == 0.0

    def test_calculate_activity_evm_zero_progress(self):
        """Edge case: Progreso 0%"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=6,
            name="Sin Avance",
            bac=10000.0,
            planned_progress=0.0,
            actual_progress=0.0,
            actual_cost=0.0,
        )

        assert result.pv == 0.0
        assert result.ev == 0.0
        assert result.cpi == 1.0
        assert result.spi == 1.0

    def test_calculate_activity_evm_completed(self):
        """Caso: Actividad completada 100%"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=7,
            name="Completada",
            bac=10000.0,
            planned_progress=1.0,
            actual_progress=1.0,
            actual_cost=9500.0,
        )

        assert result.pv == 10000.0
        assert result.ev == 10000.0
        assert result.cv == 500.0
        assert result.sv == 0.0
        assert result.cpi == 1.05
        assert result.spi == 1.0
        assert result.cost_status == "bajo presupuesto"
        assert result.schedule_status == "en cronograma"

    def test_calculate_project_evm_normal_case(self):
        """Caso normal: proyecto con múltiples actividades"""
        activities_data = [
            {
                "id": 1,
                "name": "Desarrollo Frontend",
                "bac": 10000.0,
                "planned_progress": 0.50,
                "actual_progress": 0.40,
                "actual_cost": 6000.0,
            },
            {
                "id": 2,
                "name": "Backend API",
                "bac": 15000.0,
                "planned_progress": 0.60,
                "actual_progress": 0.70,
                "actual_cost": 9000.0,
            },
            {
                "id": 3,
                "name": "Documentacion",
                "bac": 15000.0,
                "planned_progress": 0.60,
                "actual_progress": 0.70,
                "actual_cost": 9000.0,
            },
        ]

        result = EVMCalculator.calculate_project_evm(
            project_id=1,
            project_name="Proyecto Demo",
            activities_data=activities_data,
        )

        assert isinstance(result, ProjectEVM)
        assert result.project_id == 1
        assert result.project_name == "Proyecto Demo"
        assert len(result.activities) == 3

        # Verificar sumatorias
        assert result.total_bac == 40000.0  # 10000 + 15000 + 15000
        # PV: 5000 + 9000 + 9000 = 23000
        assert result.total_pv == 23000.0
        # EV: 4000 + 10500 + 10500 = 25000
        assert result.total_ev == 25000.0
        # AC: 6000 + 9000 + 9000 = 24000
        assert result.total_ac == 24000.0

        # Verificar indicadores del proyecto
        assert result.cv == 1000.0  # 25000 - 24000
        assert result.sv == 2000.0  # 25000 - 23000
        assert result.cpi == 1.04  # 25000 / 24000
        assert result.spi == 1.09  # 25000 / 23000

        # Verificar interpretaciones
        assert result.cost_status == "bajo presupuesto"
        assert result.schedule_status == "adelantado"

    def test_calculate_project_evm_empty_activities(self):
        """Edge case: Proyecto sin actividades"""
        result = EVMCalculator.calculate_project_evm(
            project_id=1,
            project_name="Proyecto Vacío",
            activities_data=[],
        )

        assert result.total_bac == 0.0
        assert result.total_pv == 0.0
        assert result.total_ev == 0.0
        assert result.total_ac == 0.0
        assert result.cpi == 1.0
        assert result.spi == 1.0
        assert result.cost_status == "sin actividades"
        assert result.schedule_status == "sin actividades"
        assert len(result.activities) == 0

    def test_calculate_project_evm_single_activity(self):
        """Caso: Proyecto con una sola actividad"""
        activities_data = [
            {
                "id": 1,
                "name": "Única Actividad",
                "bac": 10000.0,
                "planned_progress": 0.50,
                "actual_progress": 0.40,
                "actual_cost": 6000.0,
            }
        ]

        result = EVMCalculator.calculate_project_evm(
            project_id=1,
            project_name="Proyecto Simple",
            activities_data=activities_data,
        )

        assert result.total_bac == 10000.0
        assert result.total_pv == 5000.0
        assert result.total_ev == 4000.0
        assert result.total_ac == 6000.0
        assert result.cpi == 0.67
        assert result.spi == 0.8
        assert result.cost_status == "sobre presupuesto"
        assert result.schedule_status == "atrasado"
        assert len(result.activities) == 1

    def test_calculate_project_evm_all_zero(self):
        """Edge case: Todas las actividades con valores cero"""
        activities_data = [
            {
                "id": 1,
                "name": "Actividad Cero",
                "bac": 0.0,
                "planned_progress": 0.0,
                "actual_progress": 0.0,
                "actual_cost": 0.0,
            }
        ]

        result = EVMCalculator.calculate_project_evm(
            project_id=1,
            project_name="Proyecto Cero",
            activities_data=activities_data,
        )

        assert result.total_bac == 0.0
        assert result.total_pv == 0.0
        assert result.total_ev == 0.0
        assert result.total_ac == 0.0
        assert result.cpi == 1.0
        assert result.spi == 1.0

    def test_interpret_cpi(self):
        """Prueba la interpretación de CPI"""
        # Casos borde
        assert EVMCalculator._interpret_cpi(0.0) == "sobre presupuesto"
        assert EVMCalculator._interpret_cpi(0.5) == "sobre presupuesto"
        assert EVMCalculator._interpret_cpi(1.0) == "en presupuesto"
        assert EVMCalculator._interpret_cpi(1.5) == "bajo presupuesto"
        assert EVMCalculator._interpret_cpi(2.0) == "bajo presupuesto"

    def test_interpret_spi(self):
        """Prueba la interpretación de SPI"""
        # Casos borde
        assert EVMCalculator._interpret_spi(0.0) == "atrasado"
        assert EVMCalculator._interpret_spi(0.5) == "atrasado"
        assert EVMCalculator._interpret_spi(1.0) == "en cronograma"
        assert EVMCalculator._interpret_spi(1.5) == "adelantado"
        assert EVMCalculator._interpret_spi(2.0) == "adelantado"

    def test_activity_calculation_precision(self):
        """Verifica que los cálculos sean precisos (2 decimales)"""
        result = EVMCalculator.calculate_activity_evm(
            activity_id=1,
            name="Precisión",
            bac=1000.0,
            planned_progress=0.333,
            actual_progress=0.666,
            actual_cost=500.0,
        )

        # Verificar que todos los valores tienen 2 decimales
        assert result.pv == round(result.pv, 2)  # 333.00
        assert len(str(result.ev).split(".")[1]) <= 2
        assert len(str(result.cpi).split(".")[1]) <= 2
        assert len(str(result.spi).split(".")[1]) <= 2

    def test_project_calculation_precision(self):
        """Verifica que los cálculos del proyecto sean precisos"""
        activities = [
            {
                "id": 1,
                "name": "Act 1",
                "bac": 1000.0,
                "planned_progress": 0.333,
                "actual_progress": 0.666,
                "actual_cost": 500.0,
            }
        ]

        result = EVMCalculator.calculate_project_evm(
            project_id=1,
            project_name="Precisión Proyecto",
            activities_data=activities,
        )

        assert len(str(result.cpi).split(".")[1]) <= 2
        assert len(str(result.spi).split(".")[1]) <= 2


@pytest.fixture
def sample_activities():
    """Fixture con actividades de ejemplo"""
    return [
        {
            "id": 1,
            "name": "Diseño UI",
            "bac": 5000.0,
            "planned_progress": 0.80,
            "actual_progress": 0.60,
            "actual_cost": 4500.0,
        },
        {
            "id": 2,
            "name": "Frontend",
            "bac": 12000.0,
            "planned_progress": 0.50,
            "actual_progress": 0.40,
            "actual_cost": 7000.0,
        },
    ]


def test_with_fixture(sample_activities):
    """Prueba usando fixture"""
    result = EVMCalculator.calculate_project_evm(
        project_id=1,
        project_name="Proyecto con Fixture",
        activities_data=sample_activities,
    )

    assert len(result.activities) == 2
    assert result.total_bac == 17000.0  # 5000 + 12000
