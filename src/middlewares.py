import logging

from fastapi import Request
from fastapi.responses import Response

logger = logging.getLogger(__name__)


async def log_stuff(request: Request, call_next):
    response: Response = await call_next(request)
    logger.info("%s %s %s", response.status_code, request.method, request.url)
    return response
