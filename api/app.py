from fastapi import FastAPI, Request
from util.logging_config import logger
from api.pets_api import router as pets_router
from api.store_api import router as store_router
from api.user_api import router as user_router

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(
        "Incoming request",
        method=request.method,
        url=str(request.url),
        headers=dict(request.headers),
    )
    response = await call_next(request)
    return response

# Connect routers
app.include_router(pets_router)
app.include_router(store_router)
app.include_router(user_router)