from pydantic import BaseModel
from datetime import date


class DataResponse(BaseModel):
    id: int
    temperature: float
    pulse_rate: float
    air_quality: float
    created_at: date

    class Config:
        from_attributes = True
        populate_by_name = True


class PatientPulseDTO(BaseModel):
    id: int
    pulse_rate: float
    temperature: float
    air_quality: float
    created_at: date