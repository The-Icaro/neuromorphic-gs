from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.database.models import PatientPulse
from app.dtos.data import DataResponse


class GetData(BaseModel):
    fields: List[str]

router = APIRouter()


@router.get(
    "/get-data", status_code=status.HTTP_200_OK, response_model=List[DataResponse]
)
def get_data(
    body: GetData,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
):
    query = db.query(PatientPulse)

    try:
      if body.fields:
          fields_to_select = [getattr(PatientPulse, field) for field in body.fields]
          query = query.with_entities(*fields_to_select)

      if page and page_size:
          query = query.limit(page_size).offset((page - 1) * page_size)

      return query.all()
    except:
      raise HTTPException(status_code=422, detail="The inputed fields are wrong")