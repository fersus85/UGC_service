import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.empty_pb2 import Empty
from grpc_health.v1 import health_pb2, health_pb2_grpc

import grpc_server.generated.activities_pb2 as pb2
import grpc_server.generated.activities_pb2_grpc as pb2_grpc
from grpc_server.utils.transformators import (
    transform_film_score,
    transform_film_bookmark,
    transform_film_review
)
from init_services import init_mongo, init_casher
from models.mongo_models import (
    FilmScoreModel,
    FilmBookmarkModel,
    FilmReviewModel
)
from services.bookmark_service import get_bookmark_service
from services.review_service import get_review_service
from services.model_poller import ModelPoller
from services.score_service import get_film_score_service

logger = logging.getLogger(__name__)


activities = (
    pb2.Activity(
        id="act1",
        user_id="d7047039-c610-4e15-9296-86ee5a578656",
        activity_type=0,
        created_at=Timestamp().FromDatetime(
            datetime.now() + timedelta(seconds=1)
        ),
        rating=pb2.Rating(film_id="1", rating=8),
    ),
    pb2.Activity(
        id="act2",
        user_id="d7047039-c610-4e15-9296-86ee5a578656",
        activity_type=2,
        created_at=Timestamp().FromDatetime(
            datetime.now() + timedelta(seconds=1)
        ),
        review=pb2.Review(film_id="2", review_text="So so"),
    ),
    pb2.Activity(
        id="act3",
        user_id="user2",
        activity_type=1,
        created_at=Timestamp().FromDatetime(
            datetime.now() + timedelta(seconds=2)
        ),
        bookmark=pb2.Bookmark(film_id="1"),
    ),
    pb2.Activity(
        id="act4",
        user_id="user3",
        activity_type=0,
        created_at=Timestamp().FromDatetime(
            datetime.now() + timedelta(seconds=2)
        ),
        rating=pb2.Rating(film_id="2", rating=5),
    ),
    pb2.Activity(
        id="act5",
        user_id="user3",
        activity_type=2,
        created_at=Timestamp().FromDatetime(
            datetime.now() + timedelta(seconds=3)
        ),
        review=pb2.Review(film_id="1", review_text="Wow"),
    ),
)


async def form_activities(user_id: str) -> List[pb2.Activity]:
    bookmarks = await get_bookmark_service().get_bookmark_films_schema(user_id)
    reviews = await get_review_service().get_user_reviews(user_id)
    scores = await get_film_score_service().get_user_scores(user_id)

    ret = []
    # Обработка закладок
    for bookmark in bookmarks:
        ret.append(pb2.Activity(
            id=bookmark.id,
            user_id=user_id,
            activity_type=pb2.ActivityType.ACTIVITY_TYPE_BOOKMARK,
            created_at=bookmark.created_at,
            bookmark=pb2.Bookmark(film_id=bookmark.film_id),
        ))

    # Обработка рецензий
    for review in reviews:
        ret.append(pb2.Activity(
            id=review.id,
            user_id=user_id,
            activity_type=pb2.ActivityType.ACTIVITY_TYPE_REVIEW,
            created_at=review.created_at,
            review=pb2.Review(
                film_id=review.film_id,
                review_text=review.review_text,
            )
        ))

    # Обработка оценок
    for score in scores:
        ret.append(pb2.Activity(
            id=score.id,
            user_id=user_id,
            activity_type=pb2.ActivityType.ACTIVITY_TYPE_RATING,
            created_at=score.created_at,
            rating=pb2.Rating(
                film_id=score.film_id,
                rating=score.film_score,
            )
        ))

    return ret


class HealthServicer(health_pb2_grpc.HealthServicer):
    async def Check(self, request, context):
        logger.info("Проверка успешна")
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING
        )


class ActivitySender(pb2_grpc.ActivitiesServiceServicer):
    async def ReceiveActivityUpdates(self, request: Empty, context):
        """Асинхронно стримит активности."""
        queue = asyncio.Queue()

        pollers = (
            ModelPoller(FilmBookmarkModel, transform_film_bookmark),
            ModelPoller(FilmReviewModel, transform_film_review),
            ModelPoller(FilmScoreModel, transform_film_score),
        )

        tasks = [asyncio.create_task(poller.run(queue)) for poller in pollers]

        try:
            while True:
                activ = await queue.get()
                yield activ
        except asyncio.CancelledError as e:
            logger.info("ReceiveActivityUpdates cancelled")
            raise e
        finally:
            for t in tasks:
                t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            logger.info("All poll tasks stopped.")

    async def GetActivities(self, request, context):
        for user_id in request.user_ids:
            activs = await form_activities(user_id)
            for activ in activs:
                yield activ


async def serve():
    server = grpc.aio.server()
    pb2_grpc.add_ActivitiesServiceServicer_to_server(ActivitySender(), server)
    health_pb2_grpc.add_HealthServicer_to_server(HealthServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logger.info("Сервер запущен на порту 50051")
    await server.wait_for_termination()


async def main():
    await init_mongo()
    await init_casher()
    server_task = asyncio.create_task(serve())
    await server_task


if __name__ == "__main__":
    asyncio.run(main())
