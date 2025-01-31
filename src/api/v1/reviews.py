import logging

from fastapi import APIRouter, Body, Depends, Path, status, HTTPException
from pydantic import ValidationError
from schemas.reviews import FilmReview, FilmReviewPost
from services.review_service import ReviewsService, get_review_service
from utils.paginator import PaginateQueryParams
from utils.token_helpers import get_user_id_from_access_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.get(
    "/{film_id}",
    response_model=list[FilmReview],
    status_code=status.HTTP_200_OK,
    summary="Get reviews",
    description="Список рецензий фильма",
)
async def get_film_reviews(
    film_id: str = Path(
        title="UUID фильма", examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    ),
    paginate_params: PaginateQueryParams = Depends(PaginateQueryParams),
    review_service: ReviewsService = Depends(get_review_service),
) -> list[FilmReview]:
    """
    Получает отзывы о фильме по его id.
    Параметры:
        film_id: str - ID фильма
        sort_field: str - имя поля для сортировки
    """
    film_reviews = await review_service.get_reviews(
        film_id,
        sort_field="likes",
        page_number=paginate_params.page_number,
        page_size=paginate_params.page_size,
    )

    try:
        film_review_list = [FilmReview(**review) for review in film_reviews]
    except ValidationError:
        raise HTTPException(status_code=400, detail="invalid data")

    return film_review_list


@router.post(
    "/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Post review",
    description="Добавить отзыв о фильме",
)
async def add_film_review(
    film_id: str = Path(
        title="UUID фильма", examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    ),
    film_review_data: FilmReviewPost = Body(),
    user_id: str = Depends(get_user_id_from_access_token),
    review_service: ReviewsService = Depends(get_review_service),
) -> int:
    """
    Добавляет отзыв о фильме по его id.
    Параметры:
        film_id: str - ID фильма
        review_text: str - текст рецензии
        film_score: int - оценка от 0 до 10
    """
    await review_service.add_review(
        film_id=film_id,
        review_text=film_review_data.review_text,
        user_id=user_id,
        film_score=film_review_data.film_score,
    )
    return status.HTTP_201_CREATED


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete review",
    description="Удалить отзыв о фильме",
)
async def delete_film_review(
    review_id: str,
    user_id: str = Depends(get_user_id_from_access_token),
    review_service: ReviewsService = Depends(get_review_service),
) -> None:
    """
    Удаляет отзыв о фильме по id отзыва.
    Параметры:
        review_id: str - ID отзыва
    """
    await review_service.delete_review(user_id=user_id, review_id=review_id)
    return None


@router.post(
    "/{review_id}/like",
    status_code=status.HTTP_200_OK,
    summary="Like review",
    description="Лайкнуть отзыв о фильме",
)
async def like_film_review(
    review_id: str,
    user_id: str = Depends(get_user_id_from_access_token),
    review_service: ReviewsService = Depends(get_review_service),
) -> int:
    """
    Добавляет лайк к отзыву о фильме по id отзыва.
    Параметры:
        review_id: str - ID отзыва
    """
    await review_service.like_review(user_id=user_id, review_id=review_id)
    return status.HTTP_200_OK
