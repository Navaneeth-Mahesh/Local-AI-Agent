import time
import logging

from fastapi import Request


logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info(
        "%s %s %.2f ms",
        request.method,
        request.url.path,
        duration * 1000,
    )

    return response