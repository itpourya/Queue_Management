import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
from src.app.route import api_router, task_router
from fastapi import APIRouter, FastAPI

app_router: APIRouter = APIRouter()

app_router.include_router(router=api_router, prefix="/api/v1/auth")
app_router.include_router(router=task_router, prefix="/api/v1/tasks")

app = FastAPI()
app.include_router(app_router)
