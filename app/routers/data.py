from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import PatientPulse

router = APIRouter()


@router.get("/get-data", status_code=status.HTTP_200_OK)
def get_data(
    fields: List[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
):
    query = db.query(PatientPulse)

    try:
        if fields:
            fields_to_select = [getattr(PatientPulse, field) for field in fields]
            query = query.with_entities(*fields_to_select)

        if page and page_size:
            query = query.limit(page_size).offset((page - 1) * page_size)

        results = query.all()

        filtered_results = []
        for result in results:
            filtered_result = {
                key: value
                for key, value in result._asdict().items()
                if value is not None
            }
            filtered_results.append(filtered_result)

        return filtered_results
    except Exception as error:
        raise HTTPException(
            status_code=422, detail=f"The inputed fields are wrong: {error}"
        )
