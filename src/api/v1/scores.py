import logging

from fastapi import APIRouter, HTTPException, status, Path
from fastapi.params import Depends
from uuid import UUID
from schemas.scores import AddScore, AverageScore
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


@router.delete(
    "/{film_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete score",
    description="Удаляет оценку фильма",
)
async def delete_film_score(
    film_id: UUID = Path(
        title="UUID фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ),
    user_id: str = Depends(get_user_id_from_access_token),
    score_service: FilmScoreService = Depends(get_film_score_service),
) -> None:
    """Удаляет оценку фильма по его id."""
    result = await score_service.delete_score(film_id, user_id)
    if result is None or result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error deleting a record",
        )
    return None


@router.get("/{film_id}", response_model=AverageScore)
async def get_film_score(
    film_id: UUID = Path(
        title="UUID фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ),
    score_service: FilmScoreService = Depends(get_film_score_service),
) -> AverageScore:
    """Получает среднюю оценку фильма по его id."""
    average_score = await score_service.get_score(film_id)
    if average_score is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильм еще никто не оценил",
        )
    return AverageScore(average_score=average_score)
