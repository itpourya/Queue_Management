import os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
import sys, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../..")
from src.app.celery_tasks import encode_image_to_base64
from src.utils.validator import validate_file_extensions

api_router: APIRouter = APIRouter()
task_router: APIRouter = APIRouter()

UPLOAD_DIR: str = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@api_router.on_event("startup")
async def on_startup():
    await init_db()

@api_router.post("/signup")
async def signup():
    pass


@api_router.post("/signin")
async def signin():
    pass


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
