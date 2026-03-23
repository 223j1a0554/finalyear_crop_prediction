# 🌱 GLOBAL RULES
soil_rules = {
    "rice": ["clay", "alluvial"],
    "maize": ["red", "loamy"],
    "chickpea": ["loamy"],
    "kidneybeans": ["loamy", "red"],
    "pigeonpeas": ["red", "loamy"],
    "mothbeans": ["sandy", "loamy"],
    "mungbean": ["loamy", "red"],
    "blackgram": ["black", "loamy"],
    "lentil": ["loamy"],
    "pomegranate": ["loamy"],
    "banana": ["loamy", "alluvial"],
    "mango": ["loamy"],
    "grapes": ["loamy"],
    "watermelon": ["sandy", "loamy"],
    "muskmelon": ["sandy", "loamy"],
    "apple": ["loamy"],
    "orange": ["loamy"],
    "papaya": ["loamy"],
    "coconut": ["alluvial"],
    "cotton": ["black"],
    "jute": ["alluvial"],
    "coffee": ["loamy"]
}

season_rules = {
    "rice": ["kharif"],
    "maize": ["kharif", "summer"],
    "chickpea": ["rabi"],
    "kidneybeans": ["kharif"],
    "pigeonpeas": ["kharif"],
    "mothbeans": ["summer"],
    "mungbean": ["summer"],
    "blackgram": ["kharif"],
    "lentil": ["rabi"],
    "pomegranate": ["summer"],
    "banana": ["all"],
    "mango": ["summer"],
    "grapes": ["rabi"],
    "watermelon": ["summer"],
    "muskmelon": ["summer"],
    "apple": ["rabi"],
    "orange": ["rabi"],
    "papaya": ["all"],
    "coconut": ["all"],
    "cotton": ["kharif"],
    "jute": ["kharif"],
    "coffee": ["rabi"]
}

def predict_crop_suitability(crop, season, soil, water_status):
    crop = crop.lower()
    soil = soil.lower()
    season = season.lower()
    score = 0

    if crop in soil_rules and soil in soil_rules[crop]:
        score += 2

    if crop in season_rules and (
        season in season_rules[crop] or "all" in season_rules[crop]
    ):
        score += 2

    # water_status should be an integer (1, 2, or 3)
    if water_status >= 3:
        score += 2
    elif water_status == 2:
        score += 1

    if score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"
    
def get_suitable_crops(season, soil, water_status):
    season = season.lower()
    soil = soil.lower()
    suitable = []

    for crop in soil_rules.keys():
        soil_ok = soil in soil_rules[crop]
        season_ok = (
            season in season_rules[crop] or
            "all" in season_rules[crop]
        )
        
        # Only suggest if water is at least Moderate (2)
        if soil_ok and season_ok and water_status >= 2:
            suitable.append(crop)

    return suitable[:3]