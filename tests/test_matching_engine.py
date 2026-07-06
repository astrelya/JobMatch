from src.matching_engine import ParsedCV, JobOffer, calculate_match_score

def test_calculate_match_score():
    cv = ParsedCV(
        skills=["Python", "React", "Docker"],
        titles=["Développeur Full Stack"],
        years_experience=4,
        raw_text="Développeur passionné avec 4 ans d'expérience."
    )
    
    offers = [
        JobOffer(
            id="1",
            title="Développeur Full Stack Python/React",
            company="TechCorp",
            description="Nous cherchons un développeur avec 3 ans d'expérience en Python et React. Docker est un plus."
        ),
        JobOffer(
            id="2",
            title="Data Scientist",
            company="DataInc",
            description="Expert en Machine Learning, R et Python. 5 ans d'expérience requis."
        )
    ]
    
    results = calculate_match_score(cv, offers)
    
    assert len(results) == 2
    assert results[0].offer_id == "1"
    assert results[0].score > results[1].score
    assert "Python" in results[0].justification
    assert "React" in results[0].justification
