"""
Tests de integración para endpoints de Activities
"""

from fastapi import status


class TestActivitiesAPI:
    """Pruebas para endpoints de actividades"""

    def test_create_activity_success(self, client, sample_project):
        """Test: Crear actividad exitosamente"""
        response = client.post(
            "/activities/",
            json={
                "project_id": sample_project.id,
                "name": "Nueva Actividad",
                "bac": 10000.0,
                "planned_progress": 0.50,
                "actual_progress": 0.40,
                "ac": 6000.0,
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Nueva Actividad"
        assert data["project_id"] == sample_project.id
        assert data["bac"] == 10000.0
        assert "evm" in data

        # Verificar EVM
        evm = data["evm"]
        assert evm["pv"] == 5000.0
        assert evm["ev"] == 4000.0
        assert evm["cpi"] == 0.67
        assert evm["cost_status"] == "sobre presupuesto"

    def test_create_activity_project_not_found(self, client):
        """Test: Crear actividad con proyecto inexistente"""
        response = client.post(
            "/activities/",
            json={
                "project_id": 9999,
                "name": "Actividad Huérfana",
                "bac": 10000.0,
                "planned_progress": 0.50,
                "actual_progress": 0.40,
                "ac": 6000.0,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Proyecto no encontrado" in response.text

    def test_create_activity_duplicate_name(
        self, client, sample_project, sample_activities
    ):
        """Test: Crear actividad con nombre duplicado en el mismo proyecto"""
        response = client.post(
            "/activities/",
            json={
                "project_id": sample_project.id,
                "name": sample_activities[
                    0
                ].name,  # Mismo nombre que la primera actividad
                "bac": 10000.0,
                "planned_progress": 0.50,
                "actual_progress": 0.40,
                "ac": 6000.0,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe una actividad con este nombre" in response.text

    def test_list_activities_by_project(
        self, client, sample_project, sample_activities
    ):
        """Test: Listar actividades de un proyecto"""
        response = client.get(f"/activities/project/{sample_project.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        assert data[0]["project_id"] == sample_project.id

        # Verificar que cada actividad tiene EVM
        for activity in data:
            assert "evm" in activity
            assert "pv" in activity["evm"]
            assert "ev" in activity["evm"]
            assert "cpi" in activity["evm"]

    def test_list_activities_project_not_found(self, client):
        """Test: Listar actividades de proyecto inexistente"""
        response = client.get("/activities/project/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Proyecto no encontrado" in response.text

    def test_get_activity_success(self, client, sample_activities):
        """Test: Obtener actividad por ID"""
        activity = sample_activities[0]
        response = client.get(f"/activities/{activity.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == activity.id
        assert data["name"] == activity.name
        assert "evm" in data

        # Verificar EVM de Frontend (0.50 planificado, 0.40 real)
        evm = data["evm"]
        assert evm["pv"] == 5000.0
        assert evm["ev"] == 4000.0
        assert evm["cpi"] == 0.67
        assert evm["cost_status"] == "sobre presupuesto"

    def test_get_activity_not_found(self, client):
        """Test: Obtener actividad que no existe"""
        response = client.get("/activities/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Actividad no encontrada" in response.text

    def test_update_activity_success(self, client, sample_activities):
        """Test: Actualizar actividad exitosamente"""
        activity = sample_activities[0]
        response = client.patch(
            f"/activities/{activity.id}",
            json={
                "name": "Frontend Actualizado",
                "actual_progress": 0.60,
                "ac": 7000.0,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Frontend Actualizado"
        assert data["actual_progress"] == 0.60
        assert data["ac"] == 7000.0

        # Verificar que EVM se recalcula
        evm = data["evm"]
        assert evm["ev"] == 6000.0  # 0.60 * 10000
        assert evm["cpi"] == 0.86  # 6000 / 7000

    def test_update_activity_partial(self, client, sample_activities):
        """Test: Actualizar solo un campo de la actividad"""
        activity = sample_activities[0]
        original_name = activity.name

        response = client.patch(
            f"/activities/{activity.id}", json={"actual_progress": 0.75}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == original_name  # Sin cambios
        assert data["actual_progress"] == 0.75

        # EVM debe recalcularse
        evm = data["evm"]
        assert evm["ev"] == 7500.0  # 0.75 * 10000

    def test_update_activity_not_found(self, client):
        """Test: Actualizar actividad que no existe"""
        response = client.patch("/activities/9999", json={"name": "No existe"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_activity_success(self, client, sample_activities):
        """Test: Eliminar actividad exitosamente"""
        activity = sample_activities[0]
        response = client.delete(f"/activities/{activity.id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que ya no existe
        get_response = client.get(f"/activities/{activity.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_activity_not_found(self, client):
        """Test: Eliminar actividad que no existe"""
        response = client.delete("/activities/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_activity_evm_recalculation_on_update(self, client, sample_activities):
        """Test: Verificar que EVM se recalcula al actualizar"""
        activity = sample_activities[1]  # Backend API

        # Actualizar progreso real
        response = client.patch(
            f"/activities/{activity.id}",
            json={"actual_progress": 0.90, "ac": 12000.0},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        evm = data["evm"]

        # Recalcular manualmente
        # BAC = 15000, planned = 0.60, actual = 0.90, cost = 12000
        assert evm["pv"] == 9000.0  # 0.60 * 15000
        assert evm["ev"] == 13500.0  # 0.90 * 15000
        assert evm["cv"] == 1500.0  # 13500 - 12000
        assert evm["cpi"] == 1.12  # 13500 / 12000
        assert evm["cost_status"] == "bajo presupuesto"
