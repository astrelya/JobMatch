from fastapi import FastAPI
from app.api.cv import router as cv_router

app = FastAPI(title="JobMatch API")

app.include_router(cv_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to JobMatch API"}
