from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime
)


Base = declarative_base()


class PatientPulse(Base):
    __tablename__ = "patient_pulse"
    id = Column(Integer, primary_key=True, index=True)
    pulse_rate = Column(Float)
    temperature = Column(Float)
    air_quality = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
