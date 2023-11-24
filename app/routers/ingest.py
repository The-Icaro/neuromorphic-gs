from logging import getLogger

import asyncio
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


@router.post("/gather-data", status_code=status.HTTP_201_CREATED)
async def ingest(db: Session = Depends(get_db)):
    logger.info("Getting patience health data in thingspeak api")
    thingspeak_list = await asyncio.wait_for(thingspeak_api_client.get_data(), None)

    logger.info("Saving patience data in the database")
    logger.info(thingspeak_list)

    for data in thingspeak_list:
      for thingspeak_data in data.feeds:
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
