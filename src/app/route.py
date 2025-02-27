import os, shutil
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Body, Depends
import sys, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../..")
from src.app.celery_tasks import encode_image_to_base64
from src.utils.validator import validate_file_extensions
from src.schema.pydantic_models import RegisterFields, LoginFields
from typing import Annotated
from src.database.db import get_db, init_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.pydantic_models import RegisterFields
from src.service.user_service import UserService

api_router: APIRouter = APIRouter()
task_router: APIRouter = APIRouter()

UPLOAD_DIR: str = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@api_router.on_event("startup")
async def on_startup():
    await init_db()

@api_router.post("/signup")
async def signup(session: Annotated[AsyncSession, Depends(get_db)], data: RegisterFields = Body()):
    service = UserService(session=session)
    status = await service.create_user_service(data)

    if not status:
        raise HTTPException(
            status_code=400,
            detail={
                "detail": "error in signup",
                "errors": {
                        "field": "email or username in not valid"
                    }
            }
        )
    
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": {
                "username": data.username,
                "email": data.email
            }
        }
    )


@api_router.post("/signin")
async def signin(session: Annotated[AsyncSession, Depends(get_db)], data: LoginFields = Body()):
    service = UserService(session=session)
    check = await service.login_user_service(data)

    if not check[0]:
        raise HTTPException(
            status_code=400,
            detail={
                "detail": "error in signup",
                "errors": {
                        "field": "email or username in not correct"
                    }
            }
        )
    
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": {
                "token": check[1].access_token,
                "type": check[1].token_type
            }
        }
    )


@task_router.post("/upload")
async def send_task(image_file: UploadFile = File(...)):
    valid: bool = validate_file_extensions(image_file.filename)
    if not valid:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Please upload .jpg file"
        )

    try:
        image_file.filename = f"{uuid.uuid4()}.png"
        file_path: str = os.path.join(UPLOAD_DIR, image_file.filename)

        with open(file_path, "wb") as img:
            shutil.copyfileobj(image_file.file, img)

        task = encode_image_to_base64.delay(file_path)

        return {
            "task_id": task.id,
            "status": "Image uploaded"
        }
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error in create task"
        )


@task_router.get("/get")
async def get_task():
    pass
