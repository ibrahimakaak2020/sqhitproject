from fastapi import APIRouter

from api import route_login  #new


api_router = APIRouter()

api_router.include_router(route_login.router,prefix="/login",tags=["login"])   #new
