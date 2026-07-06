import re
from typing import List, Optional
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobOffer(BaseModel):
    id: str
    title: str
    company: str
    description: str
    location: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None

class ParsedCV(BaseModel):
    skills: List[str]
    titles: List[str]
    years_experience: Optional[int] = None
    languages: List[str] = []
    raw_text: str = ""

class MatchResult(BaseModel):
    offer_id: str
    score: float
    justification: str

def extract_years_experience(text: str) -> Optional[int]:
    """Extract required years of experience from text."""
    match = re.search(r'(\d+)\s*(?:ans?|années?)\s*(?:d\'|d )?exp', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    if re.search(r'\b(senior|expert)\b', text, re.IGNORECASE):
        return 5
    if re.search(r'\b(junior|débutant)\b', text, re.IGNORECASE):
        return 1
    return None

def calculate_match_score(cv: ParsedCV, offers: List[JobOffer]) -> List[MatchResult]:
    """
    Calculate relevance score between a structured CV and a list of job offers.
    Uses TF-IDF + Cosine Similarity and keyword boosting.
    """
    if not offers:
        return []

    # Prepare CV text
    cv_text = " ".join(cv.titles) + " " + " ".join(cv.skills) + " " + cv.raw_text
    
    # Prepare offers text
    offers_text = [f"{offer.title} {offer.description}" for offer in offers]
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([cv_text] + offers_text)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    except ValueError:
        # Fallback if vocabulary is empty
        cosine_sim = [0.0] * len(offers)

    results = []
    for idx, offer in enumerate(offers):
        base_score = cosine_sim[idx] * 50  # Base score out of 50
        
        # Boosts
        boost_score = 0
        matched_keywords = []
        
        # Skill overlap
        offer_text_lower = (offer.title + " " + offer.description).lower()
        for skill in cv.skills:
            if skill.lower() in offer_text_lower:
                boost_score += 5
                matched_keywords.append(skill)
                
        # Title overlap
        for title in cv.titles:
            if title.lower() in offer.title.lower():
                boost_score += 10
                matched_keywords.append(title)
                
        # Experience filter/boost
        offer_exp = extract_years_experience(offer.description)
        if cv.years_experience is not None and offer_exp is not None:
            if cv.years_experience >= offer_exp:
                boost_score += 10
                matched_keywords.append(f">= {offer_exp} ans exp")
            else:
                boost_score -= 10 # Penalty if not enough experience
                
        # Cap boost score
        boost_score = min(boost_score, 50)
        
        final_score = max(0.0, min(100.0, base_score + boost_score))
        
        justification = f"Matché sur : {', '.join(set(matched_keywords))}" if matched_keywords else "Aucun mot-clé spécifique matché"
        
        results.append(MatchResult(
            offer_id=offer.id,
            score=round(final_score, 2),
            justification=justification
        ))
        
    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    return results
