from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.core.database import engine
from app.models.base import Base

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


@app.get("/")
def root():
    return {"message": "ProjectMetrics API"}
