from fastapi import FastAPI
from backend.routers import search, offers, cv

app = FastAPI(title="JobMatch API")

app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(offers.router, prefix="/api/offers", tags=["Offers"])
app.include_router(cv.router, prefix="/api/cv", tags=["CV"])
