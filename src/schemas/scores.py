from uuid import UUID

from pydantic import BaseModel, Field


class AddScore(BaseModel):
    film_id: UUID = Field(
        ...,
        description="UUID фильма",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    )
    film_score: int = Field(..., description="Оценка", ge=0, le=10, example=10)


class AverageScore(BaseModel):
    average_score: float
