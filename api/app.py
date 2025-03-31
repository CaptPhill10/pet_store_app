from fastapi import FastAPI
from api.pets_api import router as pets_router
from api.store_api import router as store_router
from api.user_api import router as user_router

app = FastAPI()
app.include_router(pets_router)
app.include_router(store_router)
app.include_router(user_router)
