from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
from app.models.base import Base
from app.routers import activities, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas al iniciar la aplicación"""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="ProjectMetrics API",
    description="API para gestión de proyectos con indicadores EVM",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(activities.router)


@app.get("/")
def root():
    return {"message": "ProjectMetrics API", "docs": "/docs"}
