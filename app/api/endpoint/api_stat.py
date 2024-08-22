from fastapi import APIRouter, HTTPException, Query

from app.crud import db_stat as statistics_crud
from app.schemas.sh_stat import (
    FormattedStatisticsResponse,
    StatisticsResponse,
)

router = APIRouter()


@router.get("/", response_model=StatisticsResponse)
def get_statistics(period: str):
    try:
        stats = statistics_crud.get_statistics(period)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/formatted", response_model=FormattedStatisticsResponse)
def get_formatted_statistics(period: str = Query()):
    try:
        stats = statistics_crud.get_statistics(period)
        formatted_stats = statistics_crud.format_statistics_response(stats)
        return {"status": 200, "formatted_statistics": formatted_stats}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
