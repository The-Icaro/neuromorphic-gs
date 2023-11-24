from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DataResponse(BaseModel):
    id: Optional[int] = None
    temperature: Optional[float] = None
    pulse_rate: Optional[float] = None
    air_quality: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
