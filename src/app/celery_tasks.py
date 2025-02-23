import base64
import os
from celery import Celery
from typing import Tuple

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="db+sqlite:///../../db.sqlite3",
)

app.conf.update(task_track_started=True)


@app.task
def encode_image_to_base64(image_path: str) -> Tuple[str, str]:
    with open(image_path, "rb") as img:
        encoded_str: str = base64.b64encode(img.read()).decode("utf-8")
        return os.path.basename(image_path), encoded_str
