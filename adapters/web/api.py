from fastapi import APIRouter
from .routes import user_routes, auth_routes

api_router = APIRouter()
api_router = APIRouter(prefix="/v1")

api_router.include_router(user_routes.router)
api_router.include_router(auth_routes.router)
