"""
Tests de integración para endpoints de Projects
"""

from fastapi import status


class TestProjectsAPI:
    """Pruebas para endpoints de proyectos"""

    def test_create_project_success(self, client):
        """Test: Crear proyecto exitosamente"""
        response = client.post(
            "/projects/",
            json={"name": "Nuevo Proyecto", "description": "Descripción del proyecto"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Nuevo Proyecto"
        assert data["description"] == "Descripción del proyecto"
        assert "id" in data
        assert "created_at" in data

    def test_create_project_missing_name(self, client):
        """Test: Crear proyecto sin nombre (debe fallar)"""
        response = client.post("/projects/", json={"description": "Sin nombre"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_project_duplicate_name(self, client, sample_project):
        """Test: Crear proyecto con nombre duplicado (debe fallar)"""
        response = client.post(
            "/projects/",
            json={"name": sample_project.name, "description": "Proyecto duplicado"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ya existe un proyecto con este nombre" in response.text

    def test_list_projects_empty(self, client):
        """Test: Listar proyectos cuando no hay ninguno"""
        response = client.get("/projects/")

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    def test_list_projects_with_data(self, client, sample_project):
        """Test: Listar proyectos con datos existentes"""
        response = client.get("/projects/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == sample_project.name
        # Verificar que NO incluye actividades (es ProjectSimpleResponse)
        assert "activities" not in data[0]

    def test_get_project_success(self, client, sample_project, sample_activities):
        """Test: Obtener proyecto por ID exitosamente"""
        response = client.get(f"/projects/{sample_project.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_project.id
        assert data["name"] == sample_project.name
        assert "activities" in data
        assert len(data["activities"]) == 3
        assert "evm" in data

        # Verificar EVM consolidado
        evm = data["evm"]
        assert evm["bac"] == 40000.0
        assert evm["pv"] == 23000.0
        assert evm["ev"] == 25000.0
        assert evm["ac"] == 24000.0
        assert evm["cpi"] == 1.04
        assert evm["spi"] == 1.09
        assert evm["cost_status"] == "bajo presupuesto"
        assert evm["schedule_status"] == "adelantado"

    def test_get_project_not_found(self, client):
        """Test: Obtener proyecto que no existe"""
        response = client.get("/projects/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Proyecto no encontrado" in response.text

    def test_update_project_success(self, client, sample_project):
        """Test: Actualizar proyecto exitosamente"""
        response = client.patch(
            f"/projects/{sample_project.id}",
            json={"name": "Proyecto Actualizado", "description": "Nueva descripción"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Proyecto Actualizado"
        assert data["description"] == "Nueva descripción"

    def test_update_project_partial(self, client, sample_project):
        """Test: Actualizar solo un campo del proyecto"""
        response = client.patch(
            f"/projects/{sample_project.id}", json={"name": "Solo Nombre Actualizado"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Solo Nombre Actualizado"
        assert data["description"] == sample_project.description  # Sin cambios

    def test_update_project_not_found(self, client):
        """Test: Actualizar proyecto que no existe"""
        response = client.patch("/projects/9999", json={"name": "No existe"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_project_success(self, client, sample_project):
        """Test: Eliminar proyecto exitosamente"""
        response = client.delete(f"/projects/{sample_project.id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que ya no existe
        get_response = client.get(f"/projects/{sample_project.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_project_not_found(self, client):
        """Test: Eliminar proyecto que no existe"""
        response = client.delete("/projects/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
