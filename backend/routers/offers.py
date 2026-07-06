from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class JobOfferDetail(BaseModel):
    id: str
    title: str
    company: str
    description: str
    location: str
    url: str

OFFERS_DB = {
    "offer_1": {
        "id": "offer_1",
        "title": "Développeur Full Stack",
        "company": "TechCorp",
        "description": "Nous cherchons un dev Python/React.",
        "location": "Paris",
        "url": "https://example.com/offer_1"
    },
    "offer_2": {
        "id": "offer_2",
        "title": "Data Scientist",
        "company": "DataInc",
        "description": "Machine learning et Python.",
        "location": "Lyon",
        "url": "https://example.com/offer_2"
    }
}

@router.get("/{offer_id}", response_model=JobOfferDetail)
async def get_offer(offer_id: str):
    if offer_id not in OFFERS_DB:
        raise HTTPException(status_code=404, detail="Offer not found")
    return OFFERS_DB[offer_id]
