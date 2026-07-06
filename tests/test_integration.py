from fastapi.testclient import TestClient
from backend.main import app
import time

client = TestClient(app)

def test_full_flow():
    response = client.post("/api/cv/upload", files={"file": ("cv.pdf", b"dummy content")})
    assert response.status_code == 200
    cv_id = response.json()["cv_id"]
    
    search_payload = {
        "cv_id": cv_id,
        "keywords": ["Python"],
        "location": "Paris"
    }
    response = client.post("/api/search", json=search_payload)
    assert response.status_code == 200
    search_id = response.json()["search_id"]
    
    time.sleep(0.5)
    
    response = client.get(f"/api/search/{search_id}/results")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["score"] >= results[-1]["score"]
    
    offer_id = results[0]["id"]
    response = client.get(f"/api/offers/{offer_id}")
    assert response.status_code == 200
    offer = response.json()
    assert offer["id"] == offer_id
