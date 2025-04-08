from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from util.logging_config import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"HTTPException: {exc.detail} (status {exc.status_code})",
                   path=request.url.path,
                   request_id=request_id,
                   status_code=exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


async def validation_exception_handler(request: Request, exc):
     request_id = getattr(request.state, "request_id", "unknown")
     logger.warning(f"Validation error: {exc.errors()}",
                path=request.url.path,
                request_id=request_id,
                errors=exc.errors())
     return JSONResponse(
        status_code=422,
        content={"error": "Invalid request", "details": exc.errors()},
     )


async def generic_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Unexpected error: {str(exc)}",
                path=request.url.path,
                request_id=request_id,
                exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
