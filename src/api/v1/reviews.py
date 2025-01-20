import datetime
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from schemas.reviews import FilmReview, FilmReviewPost
from services.review_service import ReviewsService, get_review_service
from utils.helpers import PaginateQueryParams, get_user_id_from_access_token

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
    film_id: UUID = Path(
        title="UUID фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ),
    paginate_params: PaginateQueryParams = Depends(PaginateQueryParams),
    review_service: ReviewsService = Depends(get_review_service),
) -> list[FilmReview]:
    """
    Получает отзывы о фильме по его id.
    """
    film_reviews = await review_service.get_reviews(
        film_id,
        page_number=paginate_params.page_number,
        page_size=paginate_params.page_size,
    )
    if not film_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="film reviews not found",
        )
    return [
        FilmReview(review_id=str(review.get("_id")), **review)
        for review in film_reviews
    ]


@router.post(
    "/{film_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Post review",
    description="Добавить отзыв о фильме",
)
async def add_film_review(
    film_id: UUID = Path(
        title="UUID фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ),
    film_review_data: FilmReviewPost = Body(),
    user_id: str = Depends(get_user_id_from_access_token),
    review_service: ReviewsService = Depends(get_review_service),
) -> None:
    """
    Добавляет отзыв о фильме по его id.
    """
    result = await review_service.add_review(
        film_id=film_id,
        review_text=film_review_data.review_text,
        user_id=user_id,
        film_score=film_review_data.film_score,
        create_at=datetime.datetime.now(),
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error adding review.",
        )
    return None


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_200_OK,
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
    """
    result = await review_service.delete_review(
        user_id=user_id, review_id=review_id
    )
    if result is None or result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error deleting review.",
        )
    return None


@router.patch(
    "/{review_id}",
    response_model=FilmReview,
    status_code=status.HTTP_200_OK,
    summary="Update review",
    description="Изменить отзыв о фильме",
)
async def edit_film_review(
    review_id: str,
    review_update_data: FilmReviewPost,
    user_id: str = Depends(get_user_id_from_access_token),
    review_service: ReviewsService = Depends(get_review_service),
) -> FilmReview:
    """
    Редактирует отзыв о фильме по id отзыва.
    """
    updated_review = await review_service.update_review(
        user_id=user_id,
        review_id=review_id,
        new_review_text=review_update_data.review_text,
        new_film_score=review_update_data.film_score,
    )
    if updated_review is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating review.",
        )
    return FilmReview(
        review_id=str(updated_review.get("_id")), **updated_review
    )
