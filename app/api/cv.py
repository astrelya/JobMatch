from fastapi import APIRouter, UploadFile, File, HTTPException
from app.tasks.cv_tasks import parse_cv_task
from celery.result import AsyncResult
import base64

router = APIRouter(prefix="/api/cv", tags=["cv"])

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    contents = await file.read()
    file_b64 = base64.b64encode(contents).decode('utf-8')
    
    task = parse_cv_task.delay(file_b64, file.filename)
    
    return {"id": task.id, "message": "CV parsing started"}

@router.get("/{cv_id}/status")
async def get_cv_status(cv_id: str):
    task = AsyncResult(cv_id)
    if task.state == 'PENDING':
        return {"id": cv_id, "status": "pending"}
    elif task.state != 'FAILURE':
        return {"id": cv_id, "status": "done"}
    else:
        return {"id": cv_id, "status": "error", "error": str(task.info)}

@router.get("/{cv_id}/profile")
async def get_cv_profile(cv_id: str):
    task = AsyncResult(cv_id)
    if task.state == 'SUCCESS':
        return task.result
    elif task.state == 'PENDING':
        raise HTTPException(status_code=404, detail="Parsing not finished yet")
    else:
        raise HTTPException(status_code=500, detail="Parsing failed")
