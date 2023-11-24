from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session
from dynaconf import settings

from app.database.connection import get_db
from app.database.models import PatientPulse as PatientPulseModel
from app.services.thingspeak_api import ThingspeakApiClient


router = APIRouter()
logger = getLogger()
thingspeak_api_client = ThingspeakApiClient(uri=settings("thingspeak_api_url"))


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest(db: Session = Depends(get_db)):
    logger.info("Getting patience health data in thingspeak api")
    thingspeak_list = thingspeak_api_client.get_data()

    logger.info("Saving patience data in the database")

    for thingspeak_data in thingspeak_list.feeds:
        try:
            db_temperature = PatientPulseModel(
                pulse_rate=thingspeak_data.pulse_rate,
                temperature=thingspeak_data.temperature,
                air_quality=thingspeak_data.air_quality,
                created_at=thingspeak_data.created_at
            )
            db.add(db_temperature)
            db.commit()
        except Exception as error:
            logger.error(error)
