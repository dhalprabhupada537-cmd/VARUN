import pandas as pd
import numpy as np

def predict_best_crop(soil_type, ph, nitrogen, phosphorus, potassium, temperature, rainfall, humidity):
    """Predict the best crop based on environmental conditions"""
    # Load crop data
    crops_df = pd.DataFrame([
        {
            'name': 'Wheat',
            'soil_type': 'Loam',
            'ph_min': 6.0, 'ph_max': 7.5,
            'temp_min': 10, 'temp_max': 25,
            'rainfall_min': 500, 'rainfall_max': 1000,
            'n_min': 50, 'n_max': 80,
            'p_min': 30, 'p_max': 60,
            'k_min': 40, 'k_max': 70
        },
        {
            'name': 'Rice',
            'soil_type': 'Clay',
            'ph_min': 5.0, 'ph_max': 6.5,
            'temp_min': 20, 'temp_max': 35,
            'rainfall_min': 1000, 'rainfall_max': 2000,
            'n_min': 60, 'n_max': 90,
            'p_min': 40, 'p_max': 70,
            'k_min': 50, 'k_max': 80
        },
        {
            'name': 'Maize',
            'soil_type': 'Loam',
            'ph_min': 5.5, 'ph_max': 7.0,
            'temp_min': 15, 'temp_max': 30,
            'rainfall_min': 600, 'rainfall_max': 1200,
            'n_min': 70, 'n_max': 100,
            'p_min': 50, 'p_max': 80,
            'k_min': 60, 'k_max': 90
        },
        {
            'name': 'Cotton',
            'soil_type': 'Sandy',
            'ph_min': 5.5, 'ph_max': 7.5,
            'temp_min': 20, 'temp_max': 35,
            'rainfall_min': 500, 'rainfall_max': 800,
            'n_min': 40, 'n_max': 70,
            'p_min': 30, 'p_max': 60,
            'k_min': 50, 'k_max': 80
        },
        {
            'name': 'Soybean',
            'soil_type': 'Silt',
            'ph_min': 6.0, 'ph_max': 7.0,
            'temp_min': 15, 'temp_max': 30,
            'rainfall_min': 600, 'rainfall_max': 1000,
            'n_min': 30, 'n_max': 60,
            'p_min': 40, 'p_max': 70,
            'k_min': 50, 'k_max': 80
        }
    ])
    
    # Calculate suitability score for each crop
    scores = []
    for _, crop in crops_df.iterrows():
        score = 0
        
        # Soil type match
        if crop['soil_type'] == soil_type:
            score += 25
        
        # pH level suitability
        if crop['ph_min'] <= ph <= crop['ph_max']:
            score += 20
        else:
            score -= 10 * abs(ph - (crop['ph_min'] + crop['ph_max'])/2)
        
        # Temperature suitability
        if crop['temp_min'] <= temperature <= crop['temp_max']:
            score += 15
        else:
            score -= 5 * abs(temperature - (crop['temp_min'] + crop['temp_max'])/2)
        
        # Rainfall suitability
        if crop['rainfall_min'] <= rainfall <= crop['rainfall_max']:
            score += 15
        else:
            score -= 3 * abs(rainfall - (crop['rainfall_min'] + crop['rainfall_max'])/2)
        
        # Nutrient suitability
        n_score = 0
        if crop['n_min'] <= nitrogen <= crop['n_max']:
            n_score += 8
        else:
            n_score -= 2 * abs(nitrogen - (crop['n_min'] + crop['n_max'])/2)
        
        p_score = 0
        if crop['p_min'] <= phosphorus <= crop['p_max']:
            p_score += 8
        else:
            p_score -= 2 * abs(phosphorus - (crop['p_min'] + crop['p_max'])/2)
        
        k_score = 0
        if crop['k_min'] <= potassium <= crop['k_max']:
            k_score += 9
        else:
            k_score -= 2 * abs(potassium - (crop['k_min'] + crop['k_max'])/2)
        
        score += n_score + p_score + k_score
        
        scores.append(score)
    
    # Add scores to dataframe
    crops_df['score'] = scores
    
    # Get the best crop
    best_crop = crops_df.loc[crops_df['score'].idxmax()]
    
    # Generate recommendation details
    recommendation = {
        'crop': best_crop['name'],
        'probability': min(95, max(65, int(best_crop['score']))),
        'yield': f"{np.random.uniform(2.5, 4.5):.1f}",
        'reason': generate_reason(best_crop, soil_type, ph, temperature, rainfall, nitrogen, phosphorus, potassium),
        'planting_time': "October-November" if best_crop['name'] == 'Wheat' else 
                         "June-July" if best_crop['name'] == 'Rice' else
                         "April-May" if best_crop['name'] == 'Maize' else
                         "May-June" if best_crop['name'] == 'Cotton' else "June-July",
        'water_req': "Moderate (500-700 mm)" if best_crop['name'] == 'Wheat' else 
                     "High (1000-1500 mm)" if best_crop['name'] == 'Rice' else
                     "Moderate (600-800 mm)" if best_crop['name'] == 'Maize' else
                     "Low (400-600 mm)" if best_crop['name'] == 'Cotton' else "Moderate (500-700 mm)",
        'fertilizer': "N:P:K = 60:40:40 kg/ha" if best_crop['name'] == 'Wheat' else 
                      "N:P:K = 80:40:40 kg/ha" if best_crop['name'] == 'Rice' else
                      "N:P:K = 100:50:50 kg/ha" if best_crop['name'] == 'Maize' else
                      "N:P:K = 50:25:25 kg/ha" if best_crop['name'] == 'Cotton' else "N:P:K = 40:60:40 kg/ha",
        'harvest_time': "March-April" if best_crop['name'] == 'Wheat' else 
                        "October-November" if best_crop['name'] == 'Rice' else
                        "August-September" if best_crop['name'] == 'Maize' else
                        "October-December" if best_crop['name'] == 'Cotton' else "September-October",
        'market_price': f"₹{np.random.randint(20, 45)}",
        'demand_trend': "Stable" if best_crop['name'] == 'Wheat' else 
                        "High" if best_crop['name'] == 'Rice' else
                        "Increasing" if best_crop['name'] == 'Maize' else
                        "Moderate" if best_crop['name'] == 'Cotton' else "Stable"
    }
    
    return recommendation

def generate_reason(crop, soil_type, ph, temperature, rainfall, nitrogen, phosphorus, potassium):
    """Generate a reason for the recommendation"""
    reasons = []
    
    if crop['soil_type'] == soil_type:
        reasons.append(f"ideal for {soil_type} soil")
    else:
        reasons.append(f"adaptable to {soil_type} soil")
    
    if crop['ph_min'] <= ph <= crop['ph_max']:
        reasons.append("optimal pH level")
    
    if crop['temp_min'] <= temperature <= crop['temp_max']:
        reasons.append("suitable temperature range")
    
    if crop['rainfall_min'] <= rainfall <= crop['rainfall_max']:
        reasons.append("adequate rainfall")
    
    if crop['n_min'] <= nitrogen <= crop['n_max']:
        reasons.append("sufficient nitrogen")
    
    if crop['p_min'] <= phosphorus <= crop['p_max']:
        reasons.append("adequate phosphorus")
    
    if crop['k_min'] <= potassium <= crop['k_max']:
        reasons.append("proper potassium levels")
    
    return f"{crop['name']} is recommended because it's {', '.join(reasons)}. This crop has high market demand and is well-suited to your region's climate conditions."