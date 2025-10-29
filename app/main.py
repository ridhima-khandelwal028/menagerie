import logging.config
import time
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.utils.logger_config import LOGGING
from app.routes import pets, events

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("apis")

app = FastAPI(title="Pet Menagerie API")

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = None
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time:.3f}s"
        )
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.exception(f"Error processing request {request.method} {request.url.path}: {str(e)}")
        raise e


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error at {request.url.path}: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

app.include_router(pets.router)
app.include_router(events.router)
