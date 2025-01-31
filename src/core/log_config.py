import json
import logging.config
import pathlib

from core.config import settings


def setup_logging() -> None:
    suf: str = settings.ENV.lower()
    config_file = (
        pathlib.Path(__file__).resolve().parent / f"log_{suf}_config.json"
    )

    with open(config_file) as f_in:
        config = json.load(f_in)
        try:
            logging.config.dictConfig(config)
        except ValueError as ex:
            logging.error("Error setting up logging: %s", ex)
