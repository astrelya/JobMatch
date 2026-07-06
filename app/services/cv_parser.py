import io
import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import docx
import spacy

try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    import spacy.blank
    nlp = spacy.blank("fr")

SKILLS_DB = {"python", "react", "docker", "fastapi", "sql", "java", "c++", "machine learning", "nlp"}
LANGUAGES_DB = {"français", "anglais", "espagnol", "allemand"}
TITLES_DB = {"développeur full stack", "ingénieur logiciel", "data scientist", "devops"}

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    if not text.strip():
        images = convert_from_bytes(file_bytes)
        for img in images:
            text += pytesseract.image_to_string(img, lang='fra+eng') + "\n"
            
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def parse_cv(file_bytes: bytes, filename: str) -> dict:
    if filename.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith('.docx'):
        raw_text = extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format")

    return extract_structured_data(raw_text)

def extract_structured_data(text: str) -> dict:
    text_lower = text.lower()
    doc = nlp(text)
    
    skills = []
    for token in doc:
        if token.text.lower() in SKILLS_DB and token.text.lower() not in skills:
            skills.append(token.text.lower())
            
    for skill in SKILLS_DB:
        if " " in skill and skill in text_lower and skill not in skills:
            skills.append(skill)
            
    titles = []
    for title in TITLES_DB:
        if title in text_lower:
            titles.append(title)
            
    languages = []
    for lang in LANGUAGES_DB:
        if lang in text_lower:
            languages.append(lang)
            
    years_experience = 0
    exp_match = re.search(r'(\d+)\s*(ans|années)\s*(d\'|d )?expérience', text_lower)
    if exp_match:
        years_experience = int(exp_match.group(1))
        
    return {
        "skills": list(set(skills)),
        "titles": list(set(titles)),
        "years_experience": years_experience,
        "languages": list(set(languages)),
        "raw_text": text.strip()
    }
