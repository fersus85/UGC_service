import logging
import os

import sentry_sdk
import fastapi
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from core.config import settings
from core.log_config import setup_logging
from exceptions.exception import exception_handlers
from lifespan import lifespan
from middlewares import log_stuff

load_dotenv()


setup_logging()
logger = logging.getLogger(__name__)


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
)


app = fastapi.FastAPI(
    title=settings.PROJECT_NAME,
    description="UGC-2 service",
    version="1.0.0",
    lifespan=lifespan,
    exception_handlers=exception_handlers,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=fastapi.responses.ORJSONResponse,
)


app.middleware("http")(log_stuff)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
