# type: ignore
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

import grpc_server.generated.activities_pb2 as pb2
from models.mongo_models import (
    FilmScoreModel,
    FilmBookmarkModel,
    FilmReviewModel
)


def dt_to_pb_timestamp(dt: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def transform_film_score(doc: FilmScoreModel) -> pb2.Activity:
    return pb2.Activity(
        id=str(doc.id),
        user_id=str(doc.user_id),
        activity_type=pb2.ACTIVITY_TYPE_RATING,
        created_at=dt_to_pb_timestamp(doc.created_at),
        rating=pb2.Rating(
            film_id=str(doc.film_id),
            rating=doc.film_score,
        ),
    )


def transform_film_bookmark(doc: FilmBookmarkModel) -> pb2.Activity:
    return pb2.Activity(
        id=str(doc.id),
        user_id=str(doc.user_id),
        activity_type=pb2.ACTIVITY_TYPE_BOOKMARK,
        created_at=dt_to_pb_timestamp(doc.created_at),
        bookmark=pb2.Bookmark(
            film_id=str(doc.film_id),
        ),
    )


def transform_film_review(doc: FilmReviewModel) -> pb2.Activity:
    return pb2.Activity(
        id=str(doc.id),
        user_id=str(doc.user_id),
        activity_type=pb2.ACTIVITY_TYPE_REVIEW,
        created_at=dt_to_pb_timestamp(doc.created_at),
        review=pb2.Review(
            film_id=str(doc.film_id),
            review_text=doc.review_text,
        ),
    )
