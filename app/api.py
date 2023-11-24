from logging import getLogger

from fastapi import FastAPI
from dynaconf import settings
from starlette_exporter import PrometheusMiddleware, handle_metrics
from sqlalchemy import create_engine

from app.routers import root
from app.routers import health_check
from app.routers import ingest
from app.routers import data
from app.database.models import Base
from app.database.connection import get_connection_string


logger = getLogger()

app = FastAPI(
    title=settings.get("application_name"),
    description=settings.get("application_description"),
    version="v1.0.0",
)

app_v1 = FastAPI(
    title=settings.get("application_name"),
    description=settings.get("application_description"),
    version="v1.0.0",
)

@app.on_event("startup")
def startup_event():
    try:
        engine = create_engine(get_connection_string())
        Base.metadata.create_all(bind=engine)
    except Exception as error:
        logger.error(error)

app.mount("/v1", app_v1)

app.add_middleware(PrometheusMiddleware, app_name=settings.get("application_name"))
app.add_route("/metrics", handle_metrics)
app.include_router(root.router)
app.include_router(health_check.router)

app_v1.include_router(root.router, include_in_schema=False)
app_v1.include_router(health_check.router, include_in_schema=False)
app_v1.include_router(ingest.router, prefix="/ingest")
app_v1.include_router(data.router, prefix="/data")
