"""
Configuración para tests de integración
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models.activity import Activity
from app.models.base import Base
from app.models.project import Project

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Sobrescribe la dependencia de base de datos para usar la de prueba"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Crea una sesión de base de datos para cada test"""
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Crea un cliente de prueba con sesión de base de datos"""

    def override_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_project(db_session):
    """Crea un proyecto de ejemplo para los tests"""
    project = Project(
        name="Proyecto Test", description="Proyecto para pruebas de integración"
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


@pytest.fixture(scope="function")
def sample_activities(db_session, sample_project):
    """Crea actividades de ejemplo para los tests"""
    activities = [
        Activity(
            project_id=sample_project.id,
            name="Desarrollo Frontend",
            bac=10000.0,
            planned_progress=0.50,
            actual_progress=0.40,
            ac=6000.0,
        ),
        Activity(
            project_id=sample_project.id,
            name="Backend API",
            bac=15000.0,
            planned_progress=0.60,
            actual_progress=0.70,
            ac=9000.0,
        ),
        Activity(
            project_id=sample_project.id,
            name="Documentacion",
            bac=15000.0,
            planned_progress=0.60,
            actual_progress=0.70,
            ac=9000.0,
        ),
    ]
    for activity in activities:
        db_session.add(activity)
    db_session.commit()
    for activity in activities:
        db_session.refresh(activity)
    return activities
