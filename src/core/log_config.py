import json
import logging.config
import pathlib
import uuid

from core.config import settings
from core.context import ctx_request_id


def setup_logging() -> None:
    suf: str = settings.ENV.lower()
    config_file = (
        pathlib.Path(__file__).resolve().parent / f"log_{suf}_config.json"
    )

    with open(config_file) as f_in:
        config = json.load(f_in)
        config["formatters"]["default"][
            "()"
        ] = "uvicorn.logging.DefaultFormatter"
        config["formatters"]["access"][
            "()"
        ] = "uvicorn.logging.AccessFormatter"
        try:
            logging.config.dictConfig(config)
        except ValueError as ex:
            logging.error("Error setting up logging: %s", ex)

    factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = factory(*args, **kwargs)
        record.request_id = ctx_request_id.get(uuid.uuid4())
        return record

    logging.setLogRecordFactory(record_factory)
