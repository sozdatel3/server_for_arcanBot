from fastapi import APIRouter, Body, HTTPException, Query

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


@router.post("/incriment-counter/{counter_id}", response_model=dict)
def incriment_counter(counter_id: int):
    statistics_crud.incriment_stat_counter(counter_id)
    return {"status": 200}


@router.get("/all-count", response_model=dict)
def get_all_count():
    count = statistics_crud.get_all_count()
    return {"status": 200, "count": count}


@router.get("/important-mes-id/{mes_name}", response_model=dict)
def get_important_mes_id(mes_name: str):
    message_id = statistics_crud.get_important_mes_id(mes_name)
    return {"status": 200, "message_id": message_id}


@router.post("/important-mes-id/{mes_name}", response_model=dict)
def set_important_mes_id(
    mes_name: str, message_id: int = Body(..., embed=True)
):
    statistics_crud.set_important_mes_id(mes_name, message_id)
    return {"status": 200}
