import logging

from mongo.connection_info import mongo_dsl
from mongo.create_structure import initialize_mongo_schema
from mongo.test_insert import insert_data as mongo_insert_data
from mongo.test_queries import test_queries as mongo_test_queries
from postgres.connection_info import pg_dsl
from postgres.create_structure import initialize_db
from postgres.test_insert import insert_data as pg_insert_data
from postgres.test_queries import test_queries as pg_test_queries
from helpers.data_generation import generate_data, IDType

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


if '__main__' == __name__:
    # проверка mongo
    logging.info("----- Блок Mongo -----")
    initialize_mongo_schema(mongo_dsl)

    generated_data = generate_data(IDType.ObjectId)
    mongo_insert_data(
        data=generated_data,
        dsl=mongo_dsl
    )

    mongo_test_queries(mongo_dsl)

    # проверка postgres
    logging.info("----- Блок Postgres -----")
    initialize_db(pg_dsl)

    generated_data = generate_data(IDType.UUID)
    pg_insert_data(generated_data, pg_dsl)

    pg_test_queries(pg_dsl)
