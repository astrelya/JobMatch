def match_offers(cv_profile: dict, offers: list) -> list:
    scored_offers = []
    for offer in offers:
        score = 50.0
        if "Python" in offer["description"]:
            score += 30.0
        if "React" in offer["description"]:
            score += 15.0
        
        scored_offers.append({
            "id": offer["id"],
            "title": offer["title"],
            "company": offer["company"],
            "description": offer["description"],
            "score": score
        })
    return scored_offers
