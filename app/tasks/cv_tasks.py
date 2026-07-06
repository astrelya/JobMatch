from app.tasks.celery_app import celery_app
from app.services.cv_parser import parse_cv
import base64

@celery_app.task(bind=True)
def parse_cv_task(self, file_b64: str, filename: str):
    file_bytes = base64.b64decode(file_b64)
    parsed_data = parse_cv(file_bytes, filename)
    return parsed_data
