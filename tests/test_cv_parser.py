import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.cv_parser import extract_structured_data
import io
import docx
from reportlab.pdfgen import canvas

client = TestClient(app)

def create_dummy_pdf(text):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    can.drawString(10, 100, text)
    can.save()
    packet.seek(0)
    return packet.read()

def create_dummy_docx(text):
    doc = docx.Document()
    doc.add_paragraph(text)
    packet = io.BytesIO()
    doc.save(packet)
    packet.seek(0)
    return packet.read()

def test_extract_structured_data():
    text = "Je suis un développeur full stack avec 4 ans d'expérience. Je maîtrise Python, React et Docker. Je parle français et anglais."
    data = extract_structured_data(text)
    
    assert "python" in data["skills"]
    assert "react" in data["skills"]
    assert "docker" in data["skills"]
    assert "développeur full stack" in data["titles"]
    assert data["years_experience"] == 4
    assert "français" in data["languages"]
    assert "anglais" in data["languages"]

def test_upload_cv_pdf():
    pdf_bytes = create_dummy_pdf("Développeur full stack Python React 4 ans d'expérience")
    response = client.post(
        "/api/cv/upload",
        files={"file": ("test.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_upload_cv_docx():
    docx_bytes = create_dummy_docx("Développeur full stack Python React 4 ans d'expérience")
    response = client.post(
        "/api/cv/upload",
        files={"file": ("test.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_cv_status_and_profile(monkeypatch):
    class MockTask:
        id = "test-task-id"
    
    def mock_delay(*args, **kwargs):
        return MockTask()
        
    monkeypatch.setattr("app.api.cv.parse_cv_task.delay", mock_delay)
    
    pdf_bytes = create_dummy_pdf("Développeur full stack Python React 4 ans d'expérience")
    response = client.post(
        "/api/cv/upload",
        files={"file": ("test.pdf", pdf_bytes, "application/pdf")}
    )
    task_id = response.json()["id"]
    
    class MockAsyncResult:
        def __init__(self, id):
            self.id = id
            self.state = "SUCCESS"
            self.result = {
                "skills": ["python", "react"],
                "titles": ["développeur full stack"],
                "years_experience": 4,
                "languages": [],
                "raw_text": "Développeur full stack Python React 4 ans d'expérience"
            }
            
    monkeypatch.setattr("app.api.cv.AsyncResult", MockAsyncResult)
    
    status_response = client.get(f"/api/cv/{task_id}/status")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "done"
    
    profile_response = client.get(f"/api/cv/{task_id}/profile")
    assert profile_response.status_code == 200
    assert "python" in profile_response.json()["skills"]
