from datetime import datetime

from pydantic import BaseModel, Field


class AddScore(BaseModel):
    """
    Модель для добавления и обновления оценки фильма.
    """

    film_id: str = Field(
        ...,
        description="UUID фильма",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
    film_score: int = Field(
        ..., description="Оценка", ge=0, le=10, examples=[10]
    )


class AverageScore(BaseModel):
    """
    Модель для получения средней оценки фильма.
    """

    average_score: float


class ScoreGRPC(AddScore):
    id: str
    created_at: datetime
