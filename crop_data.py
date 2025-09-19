import numpy as np

# Regional crop preferences with weights
REGIONAL_PREFERENCES = {
    "Punjab": {"Wheat": 0.9, "Rice": 0.8, "Cotton": 0.7, "Maize": 0.6, "Sugarcane": 0.5},
    "Haryana": {"Wheat": 0.9, "Rice": 0.8, "Cotton": 0.7, "Mustard": 0.6, "Bajra": 0.5},
    "Uttar Pradesh": {"Wheat": 0.9, "Rice": 0.8, "Sugarcane": 0.8, "Potato": 0.7, "Pulses": 0.6},
    "Maharashtra": {"Cotton": 0.9, "Soybean": 0.8, "Pulses": 0.7, "Sugarcane": 0.7, "Groundnut": 0.6},
    "Karnataka": {"Rice": 0.8, "Cotton": 0.7, "Pulses": 0.7, "Coffee": 0.8, "Sugarcane": 0.6},
    "Tamil Nadu": {"Rice": 0.9, "Sugarcane": 0.8, "Cotton": 0.7, "Groundnut": 0.7, "Coconut": 0.8},
    "Andhra Pradesh": {"Rice": 0.9, "Cotton": 0.8, "Chilli": 0.7, "Groundnut": 0.7, "Tobacco": 0.6},
    "Gujarat": {"Cotton": 0.9, "Groundnut": 0.8, "Wheat": 0.7, "Pulses": 0.6, "Castor": 0.5},
    "Odisha": {"Rice": 0.9, "Pulses": 0.7, "Oilseeds": 0.6, "Millets": 0.6, "Jute": 0.5},
    "Jharkhand": {"Rice": 0.9, "Pulses": 0.7, "Oilseeds": 0.6, "Maize": 0.6, "Wheat": 0.5},
    "West Bengal": {"Rice": 0.9, "Jute": 0.8, "Tea": 0.7, "Potato": 0.6, "Wheat": 0.5},
    "Bihar": {"Rice": 0.9, "Wheat": 0.8, "Maize": 0.7, "Pulses": 0.6, "Sugarcane": 0.5}
}

# Crop data with optimal conditions
CROPS = [
    {
        'name': 'Wheat', 
        'soil_types': ['Loam', 'Clay Loam'], 
        'ph_min': 6.0, 'ph_max': 7.5,
        'temp_min': 10, 'temp_max': 25, 
        'rainfall_min': 500, 'rainfall_max': 1000,
        'n_min': 50, 'n_max': 80, 
        'p_min': 30, 'p_max': 60, 
        'k_min': 40, 'k_max': 70,
        'humidity_min': 40, 'humidity_max': 80
    },
    {
        'name': 'Rice', 
        'soil_types': ['Clay', 'Clay Loam'], 
        'ph_min': 5.0, 'ph_max': 6.5,
        'temp_min': 20, 'temp_max': 35, 
        'rainfall_min': 1000, 'rainfall_max': 2000,
        'n_min': 60, 'n_max': 90, 
        'p_min': 40, 'p_max': 70, 
        'k_min': 50, 'k_max': 80,
        'humidity_min': 60, 'humidity_max': 100
    },
    {
        'name': 'Maize', 
        'soil_types': ['Loam', 'Sandy Loam'], 
        'ph_min': 5.5, 'ph_max': 7.0,
        'temp_min': 15, 'temp_max': 30, 
        'rainfall_min': 600, 'rainfall_max': 1200,
        'n_min': 70, 'n_max': 100, 
        'p_min': 50, 'p_max': 80, 
        'k_min': 60, 'k_max': 90,
        'humidity_min': 50, 'humidity_max': 80
    },
    {
        'name': 'Cotton', 
        'soil_types': ['Sandy', 'Sandy Loam'], 
        'ph_min': 5.5, 'ph_max': 7.5,
        'temp_min': 20, 'temp_max': 35, 
        'rainfall_min': 500, 'rainfall_max': 800,
        'n_min': 40, 'n_max': 70, 
        'p_min': 30, 'p_max': 60, 
        'k_min': 50, 'k_max': 80,
        'humidity_min': 40, 'humidity_max': 70
    },
    {
        'name': 'Soybean', 
        'soil_types': ['Silt', 'Silt Loam'], 
        'ph_min': 6.0, 'ph_max': 7.0,
        'temp_min': 15, 'temp_max': 30, 
        'rainfall_min': 600, 'rainfall_max': 1000,
        'n_min': 30, 'n_max': 60, 
        'p_min': 40, 'p_max': 70, 
        'k_min': 50, 'k_max': 80,
        'humidity_min': 50, 'humidity_max': 85
    },
    {
        'name': 'Pulses', 
        'soil_types': ['Loam', 'Sandy Loam'], 
        'ph_min': 6.0, 'ph_max': 7.5,
        'temp_min': 15, 'temp_max': 30, 
        'rainfall_min': 500, 'rainfall_max': 800,
        'n_min': 20, 'n_max': 50, 
        'p_min': 30, 'p_max': 60, 
        'k_min': 40, 'k_max': 70,
        'humidity_min': 40, 'humidity_max': 70
    },
    {
        'name': 'Sugarcane', 
        'soil_types': ['Loam', 'Clay Loam'], 
        'ph_min': 6.0, 'ph_max': 7.5,
        'temp_min': 20, 'temp_max': 35, 
        'rainfall_min': 1000, 'rainfall_max': 1500,
        'n_min': 100, 'n_max': 150, 
        'p_min': 50, 'p_max': 80, 
        'k_min': 80, 'k_max': 120,
        'humidity_min': 60, 'humidity_max': 85
    },
    {
        'name': 'Groundnut', 
        'soil_types': ['Sandy', 'Sandy Loam'], 
        'ph_min': 5.5, 'ph_max': 7.0,
        'temp_min': 20, 'temp_max': 35, 
        'rainfall_min': 500, 'rainfall_max': 1000,
        'n_min': 20, 'n_max': 40, 
        'p_min': 30, 'p_max': 50, 
        'k_min': 40, 'k_max': 60,
        'humidity_min': 50, 'humidity_max': 80
    }
]

# Additional crop information
PLANTING_TIMES = {
    'Wheat': 'October-November',
    'Rice': 'June-July', 
    'Maize': 'April-May',
    'Cotton': 'May-June',
    'Soybean': 'June-July',
    'Pulses': 'October-November',
    'Sugarcane': 'February-March',
    'Groundnut': 'June-July'
}

WATER_REQUIREMENTS = {
    'Wheat': 'Moderate (600-800 mm)',
    'Rice': 'High (1000-1500 mm)',
    'Maize': 'Moderate (600-800 mm)',
    'Cotton': 'Low (400-600 mm)',
    'Soybean': 'Moderate (500-700 mm)',
    'Pulses': 'Low to Moderate (400-600 mm)',
    'Sugarcane': 'High (1200-1800 mm)',
    'Groundnut': 'Moderate (500-800 mm)'
}

FERTILIZER_RECOMMENDATIONS = {
    'Wheat': 'N:P:K = 60:40:40 kg/ha',
    'Rice': 'N:P:K = 80:40:40 kg/ha',
    'Maize': 'N:P:K = 100:50:50 kg/ha',
    'Cotton': 'N:P:K = 50:25:25 kg/ha',
    'Soybean': 'N:P:K = 40:60:40 kg/ha',
    'Pulses': 'N:P:K = 20:50:40 kg/ha',
    'Sugarcane': 'N:P:K = 150:60:100 kg/ha',
    'Groundnut': 'N:P:K = 20:50:40 kg/ha'
}

HARVEST_TIMES = {
    'Wheat': 'March-April',
    'Rice': 'October-November',
    'Maize': 'August-September',
    'Cotton': 'October-December',
    'Soybean': 'September-October',
    'Pulses': 'February-March',
    'Sugarcane': 'February-March',
    'Groundnut': 'September-October'
}

def calculate_suitability_score(crop, soil_type, ph, nitrogen, phosphorus, potassium, 
                              temperature, rainfall, humidity, region):
    """
    Calculate suitability score for a crop based on various parameters
    """
    score = 0
    reasons = []
    
    # Regional preference (weight: 25%)
    regional_weight = 0.25
    regional_score = REGIONAL_PREFERENCES.get(region, {}).get(crop['name'], 0.5)
    score += regional_score * 100 * regional_weight
    reasons.append(f"Regional suitability: {regional_score*100:.1f}%")
    
    # Soil type match (weight: 20%)
    soil_weight = 0.20
    if soil_type and soil_type in crop['soil_types']:
        soil_score = 1.0
    else:
        soil_score = 0.3  # Some crops can grow in other soils with reduced yield
    score += soil_score * 100 * soil_weight
    reasons.append(f"Soil type compatibility: {soil_score*100:.1f}%")
    
    # pH suitability (weight: 15%)
    ph_weight = 0.15
    if crop['ph_min'] <= ph <= crop['ph_max']:
        ph_score = 1.0
    else:
        # Calculate how far from optimal range
        ph_mid = (crop['ph_min'] + crop['ph_max']) / 2
        ph_distance = min(abs(ph - crop['ph_min']), abs(ph - crop['ph_max']))
        ph_score = max(0, 1 - (ph_distance / 3))  # Reduced to 0 if 3 units away
    score += ph_score * 100 * ph_weight
    reasons.append(f"pH suitability: {ph_score*100:.1f}%")
    
    # Temperature suitability (weight: 15%)
    temp_weight = 0.15
    if crop['temp_min'] <= temperature <= crop['temp_max']:
        temp_score = 1.0
    else:
        # Calculate how far from optimal range
        temp_mid = (crop['temp_min'] + crop['temp_max']) / 2
        temp_distance = min(abs(temperature - crop['temp_min']), abs(temperature - crop['temp_max']))
        temp_score = max(0, 1 - (temp_distance / 15))  # Reduced to 0 if 15°C away
    score += temp_score * 100 * temp_weight
    reasons.append(f"Temperature suitability: {temp_score*100:.1f}%")
    
    # Rainfall suitability (weight: 10%)
    rain_weight = 0.10
    if crop['rainfall_min'] <= rainfall <= crop['rainfall_max']:
        rain_score = 1.0
    else:
        # Calculate how far from optimal range
        rain_mid = (crop['rainfall_min'] + crop['rainfall_max']) / 2
        rain_distance = min(abs(rainfall - crop['rainfall_min']), abs(rainfall - crop['rainfall_max']))
        rain_score = max(0, 1 - (rain_distance / 500))  # Reduced to 0 if 500mm away
    score += rain_score * 100 * rain_weight
    reasons.append(f"Rainfall suitability: {rain_score*100:.1f}%")
    
    # Humidity suitability (weight: 5%)
    humidity_weight = 0.05
    if crop['humidity_min'] <= humidity <= crop['humidity_max']:
        humidity_score = 1.0
    else:
        # Calculate how far from optimal range
        humidity_mid = (crop['humidity_min'] + crop['humidity_max']) / 2
        humidity_distance = min(abs(humidity - crop['humidity_min']), abs(humidity - crop['humidity_max']))
        humidity_score = max(0, 1 - (humidity_distance / 30))  # Reduced to 0 if 30% away
    score += humidity_score * 100 * humidity_weight
    reasons.append(f"Humidity suitability: {humidity_score*100:.1f}%")
    
    # Nutrient suitability (weight: 10%)
    nutrient_weight = 0.10
    n_score = 1.0 if crop['n_min'] <= nitrogen <= crop['n_max'] else max(0, 1 - abs(nitrogen - (crop['n_min'] + crop['n_max'])/2) / 50)
    p_score = 1.0 if crop['p_min'] <= phosphorus <= crop['p_max'] else max(0, 1 - abs(phosphorus - (crop['p_min'] + crop['p_max'])/2) / 40)
    k_score = 1.0 if crop['k_min'] <= potassium <= crop['k_max'] else max(0, 1 - abs(potassium - (crop['k_min'] + crop['k_max'])/2) / 40)
    
    nutrient_score = (n_score + p_score + k_score) / 3
    score += nutrient_score * 100 * nutrient_weight
    reasons.append(f"Nutrient suitability: {nutrient_score*100:.1f}%")
    
    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    return score, reasons

def predict_best_crops(soil_type, ph, nitrogen, phosphorus, potassium, 
                      temperature, rainfall, humidity, region, top_n=3):
    """
    Predict the best crops based on input parameters
    """
    results = []
    
    for crop in CROPS:
        score, reasons = calculate_suitability_score(
            crop, soil_type, ph, nitrogen, phosphorus, potassium,
            temperature, rainfall, humidity, region
        )
        
        # Generate detailed analysis
        analysis = generate_detailed_analysis(crop, soil_type, ph, nitrogen, phosphorus, potassium,
                                            temperature, rainfall, humidity, region)
        
        results.append({
            'crop': crop['name'],
            'score': score,
            'reasons': reasons,
            'analysis': analysis,
            'yield': f"{np.random.uniform(2.0, 5.0):.1f}",
            'planting_time': PLANTING_TIMES.get(crop['name'], 'Varies by region'),
            'water_req': WATER_REQUIREMENTS.get(crop['name'], 'Moderate'),
            'fertilizer': FERTILIZER_RECOMMENDATIONS.get(crop['name'], 'N:P:K = 50:50:50 kg/ha'),
            'harvest_time': HARVEST_TIMES.get(crop['name'], 'Varies by region'),
            'market_price': f"₹{np.random.randint(25, 55)}",
            'demand_trend': 'High' if crop['name'] in ['Rice', 'Wheat'] else 'Moderate' if crop['name'] in ['Maize', 'Cotton'] else 'Stable'
        })
    
    # Sort by score and return top N results
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_n]

def generate_detailed_analysis(crop, soil_type, ph, nitrogen, phosphorus, potassium,
                             temperature, rainfall, humidity, region):
    """
    Generate detailed analysis for a crop
    """
    analysis = []
    
    # Regional analysis
    regional_pref = REGIONAL_PREFERENCES.get(region, {}).get(crop['name'], 0)
    if regional_pref >= 0.7:
        analysis.append(f"{crop['name']} is highly preferred in {region} region.")
    elif regional_pref >= 0.4:
        analysis.append(f"{crop['name']} is moderately suitable for {region} region.")
    else:
        analysis.append(f"{crop['name']} is not typically grown in {region} but may still be viable.")
    
    # Soil analysis
    if soil_type and soil_type in crop['soil_types']:
        analysis.append(f"Ideal soil type: {soil_type} is perfect for {crop['name']}.")
    elif soil_type:
        analysis.append(f"Soil type: {soil_type} is not ideal but {crop['name']} can adapt.")
    else:
        analysis.append(f"{crop['name']} grows best in {', '.join(crop['soil_types'])} soils.")
    
    # pH analysis
    if crop['ph_min'] <= ph <= crop['ph_max']:
        analysis.append(f"Soil pH ({ph}) is ideal for {crop['name']}.")
    else:
        analysis.append(f"Soil pH ({ph}) is outside the optimal range ({crop['ph_min']}-{crop['ph_max']}) for {crop['name']}.")
    
    # Temperature analysis
    if crop['temp_min'] <= temperature <= crop['temp_max']:
        analysis.append(f"Temperature ({temperature}°C) is ideal for {crop['name']}.")
    else:
        analysis.append(f"Temperature ({temperature}°C) is outside the optimal range ({crop['temp_min']}-{crop['temp_max']}°C) for {crop['name']}.")
    
    # Rainfall analysis
    if crop['rainfall_min'] <= rainfall <= crop['rainfall_max']:
        analysis.append(f"Rainfall ({rainfall}mm) is sufficient for {crop['name']}.")
    else:
        analysis.append(f"Rainfall ({rainfall}mm) is outside the optimal range ({crop['rainfall_min']}-{crop['rainfall_max']}mm) for {crop['name']}.")
    
    # Nutrient analysis
    nutrient_status = []
    if crop['n_min'] <= nitrogen <= crop['n_max']:
        nutrient_status.append("Nitrogen levels are optimal")
    elif nitrogen < crop['n_min']:
        nutrient_status.append(f"Add {crop['n_min'] - nitrogen} kg/ha Nitrogen")
    else:
        nutrient_status.append("Reduce Nitrogen application")
    
    if crop['p_min'] <= phosphorus <= crop['p_max']:
        nutrient_status.append("Phosphorus levels are optimal")
    elif phosphorus < crop['p_min']:
        nutrient_status.append(f"Add {crop['p_min'] - phosphorus} kg/ha Phosphorus")
    else:
        nutrient_status.append("Reduce Phosphorus application")
    
    if crop['k_min'] <= potassium <= crop['k_max']:
        nutrient_status.append("Potassium levels are optimal")
    elif potassium < crop['k_min']:
        nutrient_status.append(f"Add {crop['k_min'] - potassium} kg/ha Potassium")
    else:
        nutrient_status.append("Reduce Potassium application")
    
    analysis.append("Nutrient status: " + ", ".join(nutrient_status) + ".")
    
    return analysis
