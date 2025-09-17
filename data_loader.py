import pandas as pd
import numpy as np

def load_crop_data():
    """Load crop data with optimal growing conditions"""
    crops = [
        {
            'name': 'Wheat',
            'soil_type': 'Loam',
            'ph_min': 6.0,
            'ph_max': 7.5,
            'temp_min': 10,
            'temp_max': 25,
            'rainfall_min': 500,
            'rainfall_max': 1000,
            'n_min': 50,
            'n_max': 80,
            'p_min': 30,
            'p_max': 60,
            'k_min': 40,
            'k_max': 70
        },
        {
            'name': 'Rice',
            'soil_type': 'Clay',
            'ph_min': 5.0,
            'ph_max': 6.5,
            'temp_min': 20,
            'temp_max': 35,
            'rainfall_min': 1000,
            'rainfall_max': 2000,
            'n_min': 60,
            'n_max': 90,
            'p_min': 40,
            'p_max': 70,
            'k_min': 50,
            'k_max': 80
        },
        {
            'name': 'Maize',
            'soil_type': 'Loam',
            'ph_min': 5.5,
            'ph_max': 7.0,
            'temp_min': 15,
            'temp_max': 30,
            'rainfall_min': 600,
            'rainfall_max': 1200,
            'n_min': 70,
            'n_max': 100,
            'p_min': 50,
            'p_max': 80,
            'k_min': 60,
            'k_max': 90
        },
        {
            'name': 'Cotton',
            'soil_type': 'Sandy',
            'ph_min': 5.5,
            'ph_max': 7.5,
            'temp_min': 20,
            'temp_max': 35,
            'rainfall_min': 500,
            'rainfall_max': 800,
            'n_min': 40,
            'n_max': 70,
            'p_min': 30,
            'p_max': 60,
            'k_min': 50,
            'k_max': 80
        },
        {
            'name': 'Soybean',
            'soil_type': 'Silt',
            'ph_min': 6.0,
            'ph_max': 7.0,
            'temp_min': 15,
            'temp_max': 30,
            'rainfall_min': 600,
            'rainfall_max': 1000,
            'n_min': 30,
            'n_max': 60,
            'p_min': 40,
            'p_max': 70,
            'k_min': 50,
            'k_max': 80
        }
    ]
    return pd.DataFrame(crops)

def load_soil_data():
    """Load soil type characteristics"""
    soil_types = {
        'Loam': {
            'description': 'Well-balanced soil with good drainage and nutrient retention',
            'suitable_crops': ['Wheat', 'Maize', 'Vegetables', 'Fruits'],
            'water_retention': 'Medium',
            'nutrient_retention': 'High'
        },
        'Clay': {
            'description': 'Heavy soil with poor drainage but high nutrient content',
            'suitable_crops': ['Rice', 'Cabbage', 'Lettuce', 'Broccoli'],
            'water_retention': 'High',
            'nutrient_retention': 'High'
        },
        'Sandy': {
            'description': 'Light soil with excellent drainage but low nutrient retention',
            'suitable_crops': ['Cotton', 'Potatoes', 'Carrots', 'Peanuts'],
            'water_retention': 'Low',
            'nutrient_retention': 'Low'
        },
        'Silt': {
            'description': 'Smooth soil with moderate drainage and good fertility',
            'suitable_crops': ['Soybean', 'Wheat', 'Barley', 'Oats'],
            'water_retention': 'Medium',
            'nutrient_retention': 'Medium'
        }
    }
    return soil_types

def get_weather_forecast(location):
    """Get mock weather forecast data"""
    # In a real application, this would fetch data from a weather API
    return {
        'location': location,
        'temperature': 25,
        'humidity': 60,
        'rainfall': 800,
        'forecast': 'Partly cloudy with a chance of rain'
    }