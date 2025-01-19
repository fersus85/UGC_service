import uuid
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from db.mongo.mongo_rep import MongoRepository, get_mongo_repository


class FilmScoreService:
    """
    Сервис для работы с оценками фильмов в MongoDB.
    """

    def __init__(self, mongo_repository: MongoRepository):
        """
        Инициализирует сервис оценок фильмов.
        """
        self._mongo_repository = mongo_repository
        self.collection_name = "film_score"

    async def add_score(
        self, film_id: uuid.UUID, user_id: uuid.UUID, film_score: int
    ) -> dict[str, str]:
        """
        Добавляет оценку фильма.
        """
        try:
            result = await self._mongo_repository.insert_one(
                self.collection_name,
                {
                    "film_id": str(film_id),
                    "user_id": str(user_id),
                    "film_score": film_score,
                },
            )
            if result:
                review = await self._mongo_repository.find_one(
                    "film_reviews",
                    {"film_id": str(film_id), "user_id": str(user_id)},
                )
                if review:
                    await self._mongo_repository.update_one(
                        "film_reviews",
                        {"film_id": str(film_id), "user_id": str(user_id)},
                        {"film_score": film_score},
                    )
            return result
        except DuplicateKeyError as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the score has already been added to film_score",
            ) from ex

    async def delete_score(
        self,
        film_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> int | None:
        """
        Удаляет оценку фильма.
        """
        return await self._mongo_repository.delete_one(
            collection_name=self.collection_name,
            query={"film_id": str(film_id), "user_id": str(user_id)},
        )

    async def get_score(
        self,
        film_id: uuid.UUID,
    ) -> float | None:
        """
        Возвращает среднюю оценку фильма.
        """
        film_scores = await self._mongo_repository.find_all(
            collection_name=self.collection_name,
            query={"film_id": str(film_id)},
        )
        if not film_scores:
            return None

        sum_score = sum(
            float(film_score.get("film_score")) for film_score in film_scores
        )
        return sum_score / len(film_scores)


@lru_cache
def get_film_score_service(
    repository: MongoRepository = Depends(get_mongo_repository),
) -> FilmScoreService:
    """
    Возвращает экземпляр сервиса для работы с оценками фильмов.
    """
    return FilmScoreService(repository)
