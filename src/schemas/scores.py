from uuid import UUID

from pydantic import BaseModel, Field


class AddScore(BaseModel):
    film_id: UUID = Field(..., description="UUID фильма")
    film_score: int = Field(..., description="Оценка", ge=0, le=10)
