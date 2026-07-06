from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter()

search_results_store = {}

class SearchRequest(BaseModel):
    cv_id: str
    keywords: Optional[List[str]] = []
    location: Optional[str] = None

class JobOffer(BaseModel):
    id: str
    title: str
    company: str
    description: str
    score: float

class SearchResponse(BaseModel):
    search_id: str
    status: str

@router.post("", response_model=SearchResponse)
async def trigger_search(request: SearchRequest, background_tasks: BackgroundTasks):
    search_id = str(uuid.uuid4())
    search_results_store[search_id] = {"status": "pending", "results": []}
    
    background_tasks.add_task(run_search_task, search_id, request.cv_id, request.keywords, request.location)
    
    return {"search_id": search_id, "status": "pending"}

@router.get("/{search_id}/results", response_model=List[JobOffer])
async def get_search_results(search_id: str):
    if search_id not in search_results_store:
        raise HTTPException(status_code=404, detail="Search not found")
    
    data = search_results_store[search_id]
    if data["status"] == "pending":
        raise HTTPException(status_code=202, detail="Search is still processing")
        
    results = sorted(data["results"], key=lambda x: x["score"], reverse=True)
    return results

async def run_search_task(search_id: str, cv_id: str, keywords: List[str], location: str):
    from backend.services.cv_parser import parse_cv
    from backend.services.job_providers import search_jobs
    from backend.services.matching_engine import match_offers
    
    try:
        cv_profile = parse_cv(cv_id)
        all_keywords = list(set((keywords or []) + cv_profile.get("skills", [])))
        raw_offers = search_jobs(all_keywords, location)
        scored_offers = match_offers(cv_profile, raw_offers)
        
        search_results_store[search_id] = {
            "status": "completed",
            "results": scored_offers
        }
    except Exception as e:
        search_results_store[search_id] = {
            "status": "error",
            "error": str(e),
            "results": []
        }
