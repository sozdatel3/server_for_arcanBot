from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.crud import db_broadcasts as broadcasts_crud

router = APIRouter()


class BroadcastCreate(BaseModel):
    broadcast_name: str


class BroadcastMark(BaseModel):
    user_id: int
    broadcast_name: str


class BroadcastStatistics(BaseModel):
    date: str
    delivered: int
    failed: int


class AllBroadcastsStatistics(BaseModel):
    date: str
    statistics: Dict[str, Dict[str, int]]


@router.post("/create", response_model=dict)
async def create_broadcast(broadcast: BroadcastCreate):
    try:
        broadcasts_crud.create_broadcast(broadcast.broadcast_name)
        return {
            "message": f"Рассылка {broadcast.broadcast_name} успешно создана"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Не удалось создать рассылку: {str(e)}"
        )


@router.post("/mark_delivered", response_model=dict)
async def mark_broadcast_delivered(broadcast_mark: BroadcastMark):
    try:
        broadcasts_crud.mark_broadcast_delivered(
            broadcast_mark.user_id, broadcast_mark.broadcast_name
        )
        return {
            "message": f"Рассылка {broadcast_mark.broadcast_name} отмечена как доставленная для пользователя {broadcast_mark.user_id}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Не удалось отметить рассылку как доставленную: {str(e)}",
        )


@router.post("/mark_failed", response_model=dict)
async def mark_broadcast_failed(broadcast_mark: BroadcastMark):
    try:
        broadcasts_crud.mark_broadcast_failed(
            broadcast_mark.user_id, broadcast_mark.broadcast_name
        )
        return {
            "message": f"Рассылка {broadcast_mark.broadcast_name} отмечена как неудачная для пользователя {broadcast_mark.user_id}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Не удалось отметить рассылку как неудачную: {str(e)}",
        )


@router.get(
    "/statistics/{broadcast_name}", response_model=List[BroadcastStatistics]
)
async def get_broadcast_statistics(broadcast_name: str):
    try:
        statistics = broadcasts_crud.get_broadcast_statistics(broadcast_name)
        return [
            BroadcastStatistics(
                date=str(date), delivered=delivered, failed=failed
            )
            for date, delivered, failed in statistics
        ]
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Не удалось получить статистику рассылки: {str(e)}",
        )


@router.get("/statistics", response_model=List[AllBroadcastsStatistics])
async def get_all_broadcasts_statistics():
    try:
        statistics, columns = broadcasts_crud.get_all_broadcasts_statistics()
        result = []
        for row in statistics:
            date = str(row[0])
            stats = {}
            for i, col in enumerate(columns):
                delivered = row[i * 2 + 1]
                failed = row[i * 2 + 2]
                stats[col] = {"delivered": delivered, "failed": failed}
            result.append(AllBroadcastsStatistics(date=date, statistics=stats))
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Не удалось получить статистику рассылок: {str(e)}",
        )


# Здесь можно добавить дополнительные эндпоинты, например, для получения статистики по рассылкам
