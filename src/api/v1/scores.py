import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from schemas.scores import AddScore
from utils.helpers import get_user_id_from_access_token
from services.score_service import FilmScoreService, get_film_score_service

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
    """Добавляет оценку к фильму."""
    logger.info(f"user_id: {user_id}")
    logger.info(f"data: {data}")
    result = await score_service.add_score(data.film_id, user_id, data.film_score)
    logger.info(f"result: {result}")
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error when adding a record",
        )
    return None
