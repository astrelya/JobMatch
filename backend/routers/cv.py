from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_cv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    cv_id = str(uuid.uuid4())
    return {"cv_id": cv_id, "status": "parsing_started"}

@router.get("/{cv_id}/status")
async def get_cv_status(cv_id: str):
    return {"cv_id": cv_id, "status": "done"}

@router.get("/{cv_id}/profile")
async def get_cv_profile(cv_id: str):
    return {
        "skills": ["Python", "React"],
        "titles": ["Développeur Full Stack"],
        "years_experience": 3
    }
