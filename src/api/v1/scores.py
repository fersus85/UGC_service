import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from schemas.scores import AddScore
from services.score_service import FilmScoreService, get_film_score_service
from utils.helpers import get_user_id_from_access_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scores",
    tags=["Scores"],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Add score",
    description="Добавляет оценку к фильму",
)
async def add_film_score(
    data: AddScore,
    user_id: str = Depends(get_user_id_from_access_token),
    score_service: FilmScoreService = Depends(get_film_score_service),
) -> None:
    """
    Добавляет оценку к фильму.
    Параметры:
        film_id: UUID - UUID фильма
        film_score: int - Оценка, от 0 до 10
    """
    result = await score_service.add_score(
        data.film_id, user_id, data.film_score
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error when adding a record",
        )
    return None
