import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime, timedelta
import os
import random

# Page configuration
st.set_page_config(
    page_title="VARUN AI Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language selection
def set_language():
    # Store language in session state
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    
    # Language options
    languages = {
        'English': 'EN',
        'Hindi': 'HI',
        'Odia': 'OD',
        'Telugu': 'TE',
        'Bengali': 'BN'
    }
    
    return languages

# Language translations
def get_translations():
    translations = {
        'EN': {
            'title': 'VARUN AI Crop Recommendation',
            'tagline': 'Advanced Modern Transformation for Optimal Guidance',
            'farmer_details': 'Farmer Details',
            'full_name': 'Full Name',
            'region': 'Region',
            'farm_size': 'Farm Size (acres)',
            'soil_properties': 'Soil Properties',
            'soil_type': 'Soil Type',
            'soil_ph': 'Soil pH',
            'soil_moisture': 'Soil Moisture (%)',
            'nitrogen': 'Nitrogen (kg/ha)',
            'phosphorus': 'Phosphorus (kg/ha)',
            'potassium': 'Potassium (kg/ha)',
            'environmental_factors': 'Environmental Factors',
            'temperature': 'Temperature (°C)',
            'rainfall': 'Annual Rainfall (mm)',
            'humidity': 'Humidity (%)',
            'analyze_button': 'Analyze & Recommend',
            'farm_overview': 'Farm Overview',
            'crop_recommendation': 'Crop Recommendation',
            'soil_analysis': 'Soil Analysis',
            'weather_forecast': 'Weather Forecast',
            'top_recommendation': 'Top Recommendation',
            'expected_yield': 'Expected Yield',
            'success_probability': 'Success Probability',
            'why_this_crop': 'Why this crop?',
            'best_planting_time': 'Best Planting Time',
            'water_requirements': 'Water Requirements',
            'fertilizer_recommendations': 'Fertilizer Recommendations',
            'harvest_timeline': 'Harvest Timeline',
            'market_insights': 'Market Insights',
            'current_market_price': 'Current market price',
            'demand_trend': 'Demand trend',
            'alternative_options': 'Alternative Options',
            'fertilizer_guide': 'Fertilizer Guide',
            'crop_diseases': 'Crop Diseases & Prevention',
            'common_diseases': 'Common Diseases',
            'prevention_methods': 'Prevention Methods',
            'created_by': 'Created with ❤ by',
            'team_name': 'Team AgroNova',
            'for_sih': 'for SIH 2025',
            'generate_data': 'Generate Sample Data',
            'regions': ['Select', 'Punjab', 'Haryana', 'Uttar Pradesh', 'Maharashtra', 
                       'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Gujarat',
                       'Odisha', 'Jharkhand', 'West Bengal', 'Bihar'],
            'soil_types': ['Select', 'Loam', 'Clay', 'Sandy', 'Silt'],
            'generate_weather': 'Generate Weather Data',
            'generate_soil': 'Generate Soil Data'
        },
        'HI': {
            'title': 'वरुण एआई फसल सिफारिश',
            'tagline': 'इष्टतम मार्गदर्शन के लिए उन्नत आधुनिक परिवर्तन',
            'farmer_details': 'किसान का विवरण',
            'full_name': 'पूरा नाम',
            'region': 'क्षेत्र',
            'farm_size': 'खेत का आकार (एकड़)',
            'soil_properties': 'मिट्टी के गुण',
            'soil_type': 'मिट्टी का प्रकार',
            'soil_ph': 'मिट्टी का पीएच',
            'soil_moisture': 'मिट्टी की नमी (%)',
            'nitrogen': 'नाइट्रोजन (किग्रा/हेक्टेयर)',
            'phosphorus': 'फॉस्फोरस (किग्रा/हेक्टेयर)',
            'potassium': 'पोटेशियम (किग्रा/हेक्टेयर)',
            'environmental_factors': 'पर्यावरणीय कारक',
            'temperature': 'तापमान (°C)',
            'rainfall': 'वार्षिक वर्षा (मिमी)',
            'humidity': 'आर्द्रता (%)',
            'analyze_button': 'विश्लेषण और सिफारिश करें',
            'farm_overview': 'खेत का अवलोकन',
            'crop_recommendation': 'फसल सिफारिश',
            'soil_analysis': 'मिट्टी विश्लेषण',
            'weather_forecast': 'मौसम पूर्वानुमान',
            'top_recommendation': 'शीर्ष सिफारिश',
            'expected_yield': 'अनुमानित उपज',
            'success_probability': 'सफलता की संभावना',
            'why_this_crop': 'यह फसल क्यों?',
            'best_planting_time': 'बुवाई का सबसे अच्छा समय',
            'water_requirements': 'पानी की आवश्यकता',
            'fertilizer_recommendations': 'उर्वरक सिफारिशें',
            'harvest_timeline': 'कटाई का समय',
            'market_insights': 'बाजार की जानकारी',
            'current_market_price': 'वर्तमान बाजार मूल्य',
            'demand_trend': 'मांग का रुझान',
            'alternative_options': 'वैकल्पिक विकल्प',
            'fertilizer_guide': 'उर्वरक गाइड',
            'crop_diseases': 'फसल रोग और रोकथाम',
            'common_diseases': 'सामान्य रोग',
            'prevention_methods': 'रोकथाम के तरीके',
            'created_by': '❤ से बनाया गया',
            'team_name': 'टीम एग्रोनोवा',
            'for_sih': 'एसआईएच 2025 के लिए',
            'generate_data': 'नमूना डेटा जनरेट करें',
            'regions': ['चुनें', 'पंजाब', 'हरियाणा', 'उत्तर प्रदेश', 'महाराष्ट्र',
                       'कर्नाटक', 'तमिलनाडु', 'आंध्र प्रदेश', 'गुजरात',
                       'ओडिशा', 'झारखंड', 'पश्चिम बंगाल', 'बिहार'],
            'soil_types': ['चुनें', 'दोमट', 'चिकनी', 'बलुई', 'गाद'],
            'generate_weather': 'मौसम डेटा जनरेट करें',
            'generate_soil': 'मिट्टी डेटा जनरेट करें'
        },
        # Other languages would follow the same pattern
        # For brevity, I've included only Hindi as an example
        # You would add similar translations for OD, TE, and BN
    }
    return translations

# Custom CSS with enhanced VARUN branding
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2E8B57;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .tagline {
        font-size: 1.2rem;
        color: #3CB371;
        text-align: center;
        margin-top: 0;
        font-style: italic;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2E8B57;
        border-bottom: 2px solid #3CB371;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px 0 rgba(0,0,0,0.1);
        margin: 15px 0;
        background-color: #FFFFFF;
        border-left: 5px solid #4CAF50;
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px 0 rgba(0,0,0,0.15);
    }
    .recommendation-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    .soil-image {
        border-radius: 12px;
        width: 100%;
        height: 180px;
        object-fit: cover;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .weather-card {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        border-radius: 10px;
    }
    .team-name {
        font-weight: bold;
        color: #FFD700;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
    }
    .analysis-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        height: 140px;
    }
    .factor-score {
        font-size: 14px;
        color: #2E8B57;
        font-weight: bold;
    }
    .disease-card {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .fertilizer-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .language-selector {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f0f8f0 0%, #e0f0e0 100%);
    }
</style>
""", unsafe_allow_html=True)

# Generate soil images if they don't exist
def generate_soil_images():
    try:
        soil_colors = {
            "clay": (180, 120, 80),
            "loam": (160, 100, 60),
            "sand": (220, 200, 160),
            "silt": (200, 180, 140)
        }
        
        os.makedirs("assets/soil_types", exist_ok=True)
        
        for soil_type, color in soil_colors.items():
            img_path = f"assets/soil_types/{soil_type}.png"
            if not os.path.exists(img_path):
                img = Image.new('RGB', (400, 300), color=color)
                draw = ImageDraw.Draw(img)
                
                # Add texture
                for _ in range(800):
                    x = np.random.randint(0, 400)
                    y = np.random.randint(0, 300)
                    size = np.random.randint(2, 8)
                    draw.ellipse([(x, y), (x+size, y+size)], 
                               fill=tuple(max(0, c-30) for c in color))
                
                # Add text
                try:
                    font = ImageFont.truetype("arial.ttf", 40)
                except:
                    font = ImageFont.load_default()
                
                draw.text((120, 120), soil_type.upper(), fill=(255, 255, 255), font=font)
                img.save(img_path)
    except Exception as e:
        st.error(f"Error generating soil images: {e}")

# Generate logo if it doesn't exist
def generate_logo():
    try:
        if not os.path.exists("assets/logo.png"):
            img = Image.new('RGB', (400, 200), color=(46, 139, 87))
            draw = ImageDraw.Draw(img)
            
            # Draw VARUN text
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            draw.text((120, 70), "VARUN", fill=(255, 255, 255), font=font)
            draw.text((130, 120), "ai", fill=(255, 215, 0), font=font)
            
            # Draw plant icon
            draw.ellipse([(30, 70), (90, 130)], fill=(255, 215, 0))  # Sun
            
            # Draw a small plant
            draw.rectangle([(180, 130), (190, 150)], fill=(139, 69, 19))  # Stem
            draw.polygon([(175, 130), (185, 100), (195, 130)], fill=(34, 139, 34))  # Leaves
            
            img.save("assets/logo.png")
    except Exception as e:
        st.error(f"Error generating logo: {e}")

# Generate images
try:
    os.makedirs("assets", exist_ok=True)
    os.makedirs("assets/soil_types", exist_ok=True)
    generate_logo()
    generate_soil_images()
except Exception as e:
    st.error(f"Error creating assets directory: {e}")

# Initialize language
languages = set_language()
translations = get_translations()

# Language selector in sidebar
with st.sidebar:
    st.selectbox("🌐 Language", options=list(languages.keys()), key='language_select')

# Update current language
current_lang_code = languages[st.session_state.language_select]
current_lang = translations[current_lang_code]

# App header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f'<h1 class="main-header">VARUN<span style="color: #FFD700;">ai</span></h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="tagline">{current_lang["tagline"]}</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    try:
        st.image("assets/logo.png", width=280)
    except:
        st.warning("Logo image not found")
    
    st.markdown(f"## {current_lang['farmer_details']}")
    
    farmer_name = st.text_input(current_lang["full_name"], "Rajesh Kumar")
    farm_location = st.selectbox(current_lang["region"], current_lang["regions"], index=1)
    farm_size = st.slider(current_lang["farm_size"], 1, 100, 10)
    
    st.markdown(f"## {current_lang['soil_properties']}")
    
    # Generate soil data button
    if st.button(current_lang["generate_soil"]):
        st.session_state.soil_type = random.choice(current_lang["soil_types"][1:])
        st.session_state.soil_ph = round(random.uniform(5.5, 7.5), 1)
        st.session_state.soil_moisture = random.randint(40, 80)
        st.session_state.nitrogen = random.randint(30, 100)
        st.session_state.phosphorus = random.randint(20, 80)
        st.session_state.potassium = random.randint(30, 90)
    
    # Initialize soil data in session state
    if 'soil_type' not in st.session_state:
        st.session_state.soil_type = current_lang["soil_types"][1]  # Default to Loam
    
    soil_type = st.selectbox(current_lang["soil_type"], current_lang["soil_types"], 
                           index=current_lang["soil_types"].index(st.session_state.soil_type) 
                           if st.session_state.soil_type in current_lang["soil_types"] else 1)
    
    if 'soil_ph' not in st.session_state:
        st.session_state.soil_ph = 6.5
    
    soil_ph = st.slider(current_lang["soil_ph"], 4.0, 9.0, st.session_state.soil_ph)
    
    if 'soil_moisture' not in st.session_state:
        st.session_state.soil_moisture = 50
    
    soil_moisture = st.slider(current_lang["soil_moisture"], 0, 100, st.session_state.soil_moisture)
    
    if 'nitrogen' not in st.session_state:
        st.session_state.nitrogen = 50
    
    nitrogen = st.slider(current_lang["nitrogen"], 0, 200, st.session_state.nitrogen)
    
    if 'phosphorus' not in st.session_state:
        st.session_state.phosphorus = 40
    
    phosphorus = st.slider(current_lang["phosphorus"], 0, 200, st.session_state.phosphorus)
    
    if 'potassium' not in st.session_state:
        st.session_state.potassium = 60
    
    potassium = st.slider(current_lang["potassium"], 0, 200, st.session_state.potassium)
    
    st.markdown(f"## {current_lang['environmental_factors']}")
    
    # Generate weather data button
    if st.button(current_lang["generate_weather"]):
        st.session_state.temperature = random.randint(15, 35)
        st.session_state.rainfall = random.randint(500, 1500)
        st.session_state.humidity = random.randint(40, 90)
    
    # Initialize weather data in session state
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 25
    
    temperature = st.slider(current_lang["temperature"], 0, 45, st.session_state.temperature)
    
    if 'rainfall' not in st.session_state:
        st.session_state.rainfall = 800
    
    rainfall = st.slider(current_lang["rainfall"], 0, 2000, st.session_state.rainfall)
    
    if 'humidity' not in st.session_state:
        st.session_state.humidity = 60
    
    humidity = st.slider(current_lang["humidity"], 0, 100, st.session_state.humidity)
    
    analyze_button = st.button(current_lang["analyze_button"], type="primary")

# Enhanced crop recommendation model with detailed analysis
def predict_best_crop(soil_type, ph, nitrogen, phosphorus, potassium, temperature, rainfall, humidity, region):
    # Regional crop preferences
    regional_preferences = {
        "Punjab": ["Wheat", "Rice", "Cotton", "Maize", "Sugarcane"],
        "Haryana": ["Wheat", "Rice", "Cotton", "Mustard", "Bajra"],
        "Uttar Pradesh": ["Wheat", "Rice", "Sugarcane", "Potato", "Pulses"],
        "Maharashtra": ["Cotton", "Soybean", "Pulses", "Sugarcane", "Groundnut"],
        "Karnataka": ["Rice", "Cotton", "Pulses", "Coffee", "Sugarcane"],
        "Tamil Nadu": ["Rice", "Sugarcane", "Cotton", "Groundnut", "Coconut"],
        "Andhra Pradesh": ["Rice", "Cotton", "Chilli", "Groundnut", "Tobacco"],
        "Gujarat": ["Cotton", "Groundnut", "Wheat", "Pulses", "Castor"],
        "Odisha": ["Rice", "Pulses", "Oilseeds", "Millets", "Jute"],
        "Jharkhand": ["Rice", "Pulses", "Oilseeds", "Maize", "Wheat"],
        "West Bengal": ["Rice", "Jute", "Tea", "Potato", "Wheat"],
        "Bihar": ["Rice", "Wheat", "Maize", "Pulses", "Sugarcane"]
    }
    
    # Expanded crop data with optimal conditions
    crops = [
        {
            'name': 'Wheat', 'soil_type': 'Loam', 'ph_min': 6.0, 'ph_max': 7.5,
            'temp_min': 10, 'temp_max': 25, 'rainfall_min': 500, 'rainfall_max': 1000,
            'n_min': 50, 'n_max': 80, 'p_min': 30, 'p_max': 60, 'k_min': 40, 'k_max': 70
        },
        {
            'name': 'Rice', 'soil_type': 'Clay', 'ph_min': 5.0, 'ph_max': 6.5,
            'temp_min': 20, 'temp_max': 35, 'rainfall_min': 1000, 'rainfall_max': 2000,
            'n_min': 60, 'n_max': 90, 'p_min': 40, 'p_max': 70, 'k_min': 50, 'k_max': 80
        },
        {
            'name': 'Maize', 'soil_type': 'Loam', 'ph_min': 5.5, 'ph_max': 7.0,
            'temp_min': 15, 'temp_max': 30, 'rainfall_min': 600, 'rainfall_max': 1200,
            'n_min': 70, 'n_max': 100, 'p_min': 50, 'p_max': 80, 'k_min': 60, 'k_max': 90
        },
        {
            'name': 'Cotton', 'soil_type': 'Sandy', 'ph_min': 5.5, 'ph_max': 7.5,
            'temp_min': 20, 'temp_max': 35, 'rainfall_min': 500, 'rainfall_max': 800,
            'n_min': 40, 'n_max': 70, 'p_min': 30, 'p_max': 60, 'k_min': 50, 'k_max': 80
        },
        {
            'name': 'Soybean', 'soil_type': 'Silt', 'ph_min': 6.0, 'ph_max': 7.0,
            'temp_min': 15, 'temp_max': 30, 'rainfall_min': 600, 'rainfall_max': 1000,
            'n_min': 30, 'n_max': 60, 'p_min': 40, 'p_max': 70, 'k_min': 50, 'k_max': 80
        },
        {
            'name': 'Pulses', 'soil_type': 'Loam', 'ph_min': 6.0, 'ph_max': 7.5,
            'temp_min': 15, 'temp_max': 30, 'rainfall_min': 500, 'rainfall_max': 800,
            'n_min': 20, 'n_max': 50, 'p_min': 30, 'p_max': 60, 'k_min': 40, 'k_max': 70
        },
        {
            'name': 'Sugarcane', 'soil_type': 'Loam', 'ph_min': 6.0, 'ph_max': 7.5,
            'temp_min': 20, 'temp_max': 35, 'rainfall_min': 1000, 'rainfall_max': 1500,
            'n_min': 100, 'n_max': 150, 'p_min': 50, 'p_max': 80, 'k_min': 80, 'k_max': 120
        },
        {
            'name': 'Groundnut', 'soil_type': 'Sandy', 'ph_min': 5.5, 'ph_max': 7.0,
            'temp_min': 20, 'temp_max': 35, 'rainfall_min': 500, 'rainfall_max': 1000,
            'n_min': 20, 'n_max': 40, 'p_min': 30, 'p_max': 50, 'k_min': 40, 'k_max': 60
        }
    ]
    
    # Calculate scores and detailed analysis
    crop_analyses = []
    for crop in crops:
        analysis = {
            'name': crop['name'],
            'score': 0,
            'details': {
                'regional_preference': 0,
                'soil_type': 0,
                'ph_suitability': 0,
                'temperature_suitability': 0,
                'rainfall_suitability': 0,
                'nutrient_suitability': 0
            },
            'reasons': []
        }
        
        # Regional preference (higher weight)
        if region != "Select" and crop['name'] in regional_preferences.get(region, []):
            analysis['score'] += 30
            analysis['details']['regional_preference'] = 30
            analysis['reasons'].append(f"Highly suitable for {region} region")
        elif region != "Select":
            analysis['reasons'].append(f"Not typically grown in {region}")
        
        # Soil type match
        if soil_type != "Select" and crop['soil_type'].lower() == soil_type.lower():
            analysis['score'] += 25
            analysis['details']['soil_type'] = 25
            analysis['reasons'].append(f"Ideal for {soil_type} soil")
        elif soil_type != "Select":
            analysis['reasons'].append(f"Not optimal for {soil_type} soil (prefers {crop['soil_type']})")
        
        # pH suitability
        if crop['ph_min'] <= ph <= crop['ph_max']:
            ph_score = 15
            analysis['reasons'].append(f"Optimal pH range ({crop['ph_min']}-{crop['ph_max']})")
        else:
            # Calculate penalty based on deviation from optimal range
            if ph < crop['ph_min']:
                deviation = crop['ph_min'] - ph
                ph_score = max(0, 15 - (deviation * 5))
                analysis['reasons'].append(f"pH slightly low (ideal: {crop['ph_min']}-{crop['ph_max']})")
            else:
                deviation = ph - crop['ph_max']
                ph_score = max(0, 15 - (deviation * 5))
                analysis['reasons'].append(f"pH slightly high (ideal: {crop['ph_min']}-{crop['ph_max']})")
        
        analysis['score'] += ph_score
        analysis['details']['ph_suitability'] = ph_score
        
        # Temperature suitability
        if crop['temp_min'] <= temperature <= crop['temp_max']:
            temp_score = 10
            analysis['reasons'].append(f"Optimal temperature range ({crop['temp_min']}-{crop['temp_max']}°C)")
        else:
            # Calculate penalty based on deviation from optimal range
            if temperature < crop['temp_min']:
                deviation = crop['temp_min'] - temperature
                temp_score = max(0, 10 - (deviation * 0.5))
                analysis['reasons'].append(f"Temperature slightly low (ideal: {crop['temp_min']}-{crop['temp_max']}°C)")
            else:
                deviation = temperature - crop['temp_max']
                temp_score = max(0, 10 - (deviation * 0.5))
                analysis['reasons'].append(f"Temperature slightly high (ideal: {crop['temp_min']}-{crop['temp_max']}°C)")
        
        analysis['score'] += temp_score
        analysis['details']['temperature_suitability'] = temp_score
        
        # Rainfall suitability
        if crop['rainfall_min'] <= rainfall <= crop['rainfall_max']:
            rain_score = 10
            analysis['reasons'].append(f"Optimal rainfall ({crop['rainfall_min']}-{crop['rainfall_max']}mm)")
        else:
            # Calculate penalty based on deviation from optimal range
            if rainfall < crop['rainfall_min']:
                deviation = crop['rainfall_min'] - rainfall
                rain_score = max(0, 10 - (deviation * 0.02))
                analysis['reasons'].append(f"Rainfall slightly low (ideal: {crop['rainfall_min']}-{crop['rainfall_max']}mm)")
            else:
                deviation = rainfall - crop['rainfall_max']
                rain_score = max(0, 10 - (deviation * 0.01))
                analysis['reasons'].append(f"Rainfall slightly high (ideal: {crop['rainfall_min']}-{crop['rainfall_max']}mm)")
        
        analysis['score'] += rain_score
        analysis['details']['rainfall_suitability'] = rain_score
        
        # Nutrient suitability
        n_score = 8 if crop['n_min'] <= nitrogen <= crop['n_max'] else max(0, 8 - abs(nitrogen - (crop['n_min'] + crop['n_max'])/2) * 0.2)
        p_score = 8 if crop['p_min'] <= phosphorus <= crop['p_max'] else max(0, 8 - abs(phosphorus - (crop['p_min'] + crop['p_max'])/2) * 0.2)
        k_score = 9 if crop['k_min'] <= potassium <= crop['k_max'] else max(0, 9 - abs(potassium - (crop['k_min'] + crop['k_max'])/2) * 0.2)
        
        nutrient_score = n_score + p_score + k_score
        analysis['score'] += nutrient_score
        analysis['details']['nutrient_suitability'] = nutrient_score
        
        if n_score < 5:
            analysis['reasons'].append(f"Nitrogen level not optimal for {crop['name']}")
        if p_score < 5:
            analysis['reasons'].append(f"Phosphorus level not optimal for {crop['name']}")
        if k_score < 5:
            analysis['reasons'].append(f"Potassium level not optimal for {crop['name']}")
        
        crop_analyses.append(analysis)
    
    # Sort by score
    crop_analyses.sort(key=lambda x: x['score'], reverse=True)
    
    # Generate detailed recommendations for top 3 crops
    recommendations = []
    planting_times = {
        'Wheat': 'October-November',
        'Rice': 'June-July', 
        'Maize': 'April-May',
        'Cotton': 'May-June',
        'Soybean': 'June-July',
        'Pulses': 'October-November',
        'Sugarcane': 'February-March',
        'Groundnut': 'June-July'
    }
    
    # Crop diseases and prevention
    crop_diseases = {
        'Wheat': {
            'common': ['Rust', 'Smut', 'Powdery Mildew'],
            'prevention': ['Use resistant varieties', 'Crop rotation', 'Fungicide application']
        },
        'Rice': {
            'common': ['Blight', 'Tungro Virus', 'Sheath Blight'],
            'prevention': ['Proper water management', 'Use certified seeds', 'Balanced fertilization']
        },
        'Maize': {
            'common': ['Leaf Blight', 'Stalk Rot', 'Ear Rot'],
            'prevention': ['Crop rotation', 'Timely harvesting', 'Use resistant hybrids']
        },
        'Cotton': {
            'common': ['Boll Rot', 'Leaf Curl Virus', 'Wilt'],
            'prevention': ['Intercropping', 'Use neem-based pesticides', 'Proper drainage']
        },
        'Soybean': {
            'common': ['Rust', 'Pod Blight', 'Mosaic Virus'],
            'prevention': ['Seed treatment', 'Weed control', 'Balanced fertilization']
        },
        'Pulses': {
            'common': ['Wilt', 'Root Rot', 'Powdery Mildew'],
            'prevention': ['Soil solarization', 'Use healthy seeds', 'Proper spacing']
        },
        'Sugarcane': {
            'common': ['Red Rot', 'Smut', 'Ratoon Stunting'],
            'prevention': ['Use disease-free setts', 'Hot water treatment', 'Crop rotation']
        },
        'Groundnut': {
            'common': ['Leaf Spot', 'Rust', 'Collar Rot'],
            'prevention': ['Crop rotation', 'Well-drained soil', 'Seed treatment']
        }
    }
    
    # Fertilizer recommendations based on soil nutrients
    fertilizer_recommendations = {
        'Wheat': f"N:P:K = {max(40, min(80, nitrogen))}:{max(30, min(60, phosphorus))}:{max(40, min(70, potassium))} kg/ha",
        'Rice': f"N:P:K = {max(60, min(90, nitrogen))}:{max(40, min(70, phosphorus))}:{max(50, min(80, potassium))} kg/ha",
        'Maize': f"N:P:K = {max(70, min(100, nitrogen))}:{max(50, min(80, phosphorus))}:{max(60, min(90, potassium))} kg/ha",
        'Cotton': f"N:P:K = {max(40, min(70, nitrogen))}:{max(30, min(60, phosphorus))}:{max(50, min(80, potassium))} kg/ha",
        'Soybean': f"N:P:K = {max(30, min(60, nitrogen))}:{max(40, min(70, phosphorus))}:{max(50, min(80, potassium))} kg/ha",
        'Pulses': f"N:P:K = {max(20, min(50, nitrogen))}:{max(30, min(60, phosphorus))}:{max(40, min(70, potassium))} kg/ha",
        'Sugarcane': f"N:P:K = {max(100, min(150, nitrogen))}:{max(50, min(80, phosphorus))}:{max(80, min(120, potassium))} kg/ha",
        'Groundnut': f"N:P:K = {max(20, min(40, nitrogen))}:{max(30, min(50, phosphorus))}:{max(40, min(60, potassium))} kg/ha"
    }
    
    for i, analysis in enumerate(crop_analyses[:3]):
        crop_name = analysis['name']
        recommendations.append({
            'rank': i+1,
            'crop': crop_name,
            'score': analysis['score'],
            'probability': min(95, max(65, int(analysis['score']))),
            'yield': f"{np.random.uniform(2.0, 5.0):.1f}",
            'reasons': analysis['reasons'],
            'details': analysis['details'],
            'planting_time': planting_times.get(crop_name, 'Varies by region'),
            'water_req': 'Moderate (600-800 mm)' if crop_name in ['Wheat', 'Maize'] else 
                         'High (1000-1500 mm)' if crop_name == 'Rice' else
                         'Low (400-600 mm)' if crop_name == 'Cotton' else 
                         'Moderate (500-700 mm)' if crop_name in ['Soybean', 'Pulses'] else
                         'High (1200-1800 mm)' if crop_name == 'Sugarcane' else
                         'Moderate (500-800 mm)',
            'fertilizer': fertilizer_recommendations.get(crop_name, 'N:P:K = 60:40:40 kg/ha'),
            'harvest_time': 'March-April' if crop_name == 'Wheat' else 
                            'October-November' if crop_name == 'Rice' else
                            'August-September' if crop_name == 'Maize' else
                            'October-December' if crop_name == 'Cotton' else 
                            'September-October' if crop_name == 'Soybean' else
                            'February-March' if crop_name == 'Sugarcane' else
                            'September-October',
            'market_price': f"₹{np.random.randint(25, 55)}",
            'demand_trend': 'High' if crop_name in ['Rice', 'Wheat'] else 
                            'Moderate' if crop_name in ['Maize', 'Cotton'] else
                            'Stable',
            'diseases': crop_diseases.get(crop_name, {'common': [], 'prevention': []})
        })
    
    return recommendations

# Function to create suitability visualization
def create_suitability_chart(details, crop_name):
    categories = ['Regional\nPreference', 'Soil Type\nMatch', 'pH\nSuitability', 
                 'Temperature\nSuitability', 'Rainfall\nSuitability', 'Nutrient\nSuitability']
    values = [details['regional_preference'], details['soil_type'], details['ph_suitability'],
             details['temperature_suitability'], details['rainfall_suitability'], details['nutrient_suitability']]
    max_values = [30, 25, 15, 10, 10, 25]  # Maximum possible scores for each category
    
    fig = go.Figure()
    
    # Add actual values
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Actual Suitability',
        line_color='#4CAF50'
    ))
    
    # Add maximum possible values (for reference)
    fig.add_trace(go.Scatterpolar(
        r=max_values,
        theta=categories,
        fill='toself',
        name='Maximum Possible',
        line_color='#FF9800',
        opacity=0.2
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 30]  # Set range based on maximum value
            )),
        showlegend=True,
        title=f"Suitability Analysis for {crop_name}"
    )
    
    return fig

# Function to display detailed factor analysis
def display_factor_analysis(details):
    st.markdown("#### Detailed Factor Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"Regional Preference")
        st.markdown(f'<p class="factor-score">{details["regional_preference"]}/30</p>', unsafe_allow_html=True)
        st.progress(details["regional_preference"]/30)
        
        st.markdown(f"Soil Type Match")
        st.markdown(f'<p class="factor-score">{details["soil_type"]}/25</p>', unsafe_allow_html=True)
        st.progress(details["soil_type"]/25)
    
    with col2:
        st.markdown(f"pH Suitability")
        st.markdown(f'<p class="factor-score">{details["ph_suitability"]}/15</p>', unsafe_allow_html=True)
        st.progress(details["ph_suitability"]/15)
        
        st.markdown(f"Temperature Suitability")
        st.markdown(f'<p class="factor-score">{details["temperature_suitability"]}/10</p>', unsafe_allow_html=True)
        st.progress(details["temperature_suitability"]/10)
    
    with col3:
        st.markdown(f"Rainfall Suitability")
        st.markdown(f'<p class="factor-score">{details["rainfall_suitability"]}/10</p>', unsafe_allow_html=True)
        st.progress(details["rainfall_suitability"]/10)
        
        st.markdown(f"Nutrient Suitability")
        st.markdown(f'<p class="factor-score">{details["nutrient_suitability"]}/25</p>', unsafe_allow_html=True)
        st.progress(details["nutrient_suitability"]/25)

# Function to display crop diseases and prevention
def display_crop_diseases(diseases_info):
    st.markdown("#### Common Diseases & Prevention")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Common Diseases")
        for disease in diseases_info['common']:
            st.markdown(f"• {disease}")
    
    with col2:
        st.markdown("##### Prevention Methods")
        for method in diseases_info['prevention']:
            st.markdown(f"• {method}")

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Crop Recommendation", "Soil Analysis", "Weather Forecast", "Fertilizer Guide"])

with tab1:
    st.markdown(f'<h2 class="sub-header">{current_lang["farm_overview"]}</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.markdown(f'<div class="card"><h3>{current_lang["farm_size"]}</h3><p style="font-size: 24px; color: #2E8B57;">{farm_size} acres</p></div>', unsafe_allow_html=True)
    with col2: 
        soil_display = soil_type if soil_type != "Select" else "Not specified"
        st.markdown(f'<div class="card"><h3>{current_lang["soil_type"]}</h3><p style="font-size: 24px; color: #2E8B57;">{soil_display}</p></div>', unsafe_allow_html=True)
    with col3: 
        region_display = farm_location if farm_location != "Select" else "Not specified"
        st.markdown(f'<div class="card"><h3>{current_lang["region"]}</h3><p style="font-size: 24px; color: #2E8B57;">{region_display}</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown(f'<h2 class="sub-header">{current_lang["crop_recommendation"]}</h2>', unsafe_allow_html=True)
    
    if analyze_button:
        with st.spinner('Analyzing your farm data and generating recommendations...'):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            recommendations = predict_best_crop(soil_type, soil_ph, nitrogen, phosphorus, 
                                              potassium, temperature, rainfall, humidity, farm_location)
            
            # Display top recommendation
            top_recommendation = recommendations[0]
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown(f"### 🌱 {current_lang['top_recommendation']}: {top_recommendation['crop']}")
            st.markdown(f"{current_lang['expected_yield']}: {top_recommendation['yield']} tons/acre")
            st.markdown(f"{current_lang['success_probability']}: {top_recommendation['probability']}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display suitability chart
            st.plotly_chart(create_suitability_chart(top_recommendation['details'], top_recommendation['crop']), 
                           use_container_width=True)
            
            # Display detailed factor analysis
            display_factor_analysis(top_recommendation['details'])
            
            # Display reasons
            st.markdown(f"#### {current_lang['why_this_crop']}")
            for reason in top_recommendation['reasons']:
                st.info(f"• {reason}")
            
            # Display crop details
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(current_lang["best_planting_time"])
                st.write(top_recommendation['planting_time'])
                st.markdown(current_lang["water_requirements"])
                st.write(top_recommendation['water_req'])
            with col2:
                st.markdown(current_lang["fertilizer_recommendations"])
                st.write(top_recommendation['fertilizer'])
                st.markdown(current_lang["harvest_timeline"])
                st.write(top_recommendation['harvest_time'])
            
            # Display market insights
            st.markdown(f"#### {current_lang['market_insights']}")
            st.success(f"{current_lang['current_market_price']}: {top_recommendation['market_price']} per kg")
            st.write(f"{current_lang['demand_trend']}: {top_recommendation['demand_trend']}")
            
            # Display crop diseases and prevention
            display_crop_diseases(top_recommendation['diseases'])
            
            # Show alternative options
            if len(recommendations) > 1:
                st.markdown(f"#### {current_lang['alternative_options']}")
                cols = st.columns(len(recommendations) - 1)
                for idx, rec in enumerate(recommendations[1:]):
                    with cols[idx]:
                        st.markdown(f'<div class="analysis-card"><h4>{rec["crop"]}</h4><p>Score: {rec["score"]:.1f}</p><p>Probability: {rec["probability"]}%</p></div>', 
                                  unsafe_allow_html=True)
    
    else:
        st.info(f"Click the '{current_lang['analyze_button']}' button in the sidebar to get crop recommendations")

with tab3:
    st.markdown(f'<h2 class="sub-header">{current_lang["soil_analysis"]}</h2>', unsafe_allow_html=True)
    
    if soil_type != "Select":
        try:
            soil_img = Image.open(f"assets/soil_types/{soil_type.lower()}.png")
            st.image(soil_img, caption=f"{soil_type} Soil", use_container_width=True)
        except:
            st.warning("Soil image not available")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["soil_ph"]}</h4><p style="font-size: 20px;">{soil_ph}</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["soil_moisture"]}</h4><p style="font-size: 20px;">{soil_moisture}%</p></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["nitrogen"]}</h4><p style="font-size: 20px;">{nitrogen} kg/ha</p></div>', unsafe_allow_html=True)
    with col4: 
        st.markdown(f'<div class="weather-card"><h4>Organic Matter</h4><p style="font-size: 20px;">3.2%</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["phosphorus"]}</h4><p style="font-size: 20px;">{phosphorus} kg/ha</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["potassium"]}</h4><p style="font-size: 20px;">{potassium} kg/ha</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown(f'<h2 class="sub-header">{current_lang["weather_forecast"]}</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["temperature"]}</h4><p style="font-size: 20px;">{temperature}°C</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["humidity"]}</h4><p style="font-size: 20px;">{humidity}%</p></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown(f'<div class="weather-card"><h4>{current_lang["rainfall"]}</h4><p style="font-size: 20px;">{rainfall} mm</p></div>', unsafe_allow_html=True)
    with col4: 
        st.markdown(f'<div class="weather-card"><h4>Wind Speed</h4><p style="font-size: 20px;">12 km/h</p></div>', unsafe_allow_html=True)
    
    # Generate forecast data
    dates = [datetime.now() + timedelta(days=i) for i in range(7)]
    temp_forecast = [temperature + np.random.uniform(-3, 3) for _ in range(7)]
    rain_forecast = [max(0, rainfall/365 + np.random.uniform(-2, 5)) for _ in range(7)]
    
    # Create forecast chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=temp_forecast, mode='lines+markers', name='Temperature (°C)', line=dict(color='red')))
    fig.add_trace(go.Bar(x=dates, y=rain_forecast, name='Rainfall (mm)', yaxis='y2', marker_color='blue'))
    
    fig.update_layout(
        title='7-Day Weather Forecast',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Temperature (°C)', side='left', showgrid=False),
        yaxis2=dict(title='Rainfall (mm)', side='right', overlaying='y', showgrid=False),
        legend=dict(x=0, y=1.1, orientation='h')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.markdown(f'<h2 class="sub-header">{current_lang["fertilizer_guide"]}</h2>', unsafe_allow_html=True)
    
    # Display fertilizer recommendations based on soil nutrients
    st.markdown("### Recommended Fertilizer Application")
    
    # Calculate fertilizer needs based on soil nutrients
    n_deficiency = max(0, 60 - nitrogen)
    p_deficiency = max(0, 40 - phosphorus)
    k_deficiency = max(0, 50 - potassium)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="fertilizer-card"><h4>Nitrogen (N)</h4><p style="font-size: 18px;">Deficiency: {n_deficiency} kg/ha</p><p>Recommended: Urea or Ammonium Sulfate</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="fertilizer-card"><h4>Phosphorus (P)</h4><p style="font-size: 18px;">Deficiency: {p_deficiency} kg/ha</p><p>Recommended: DAP or SSP</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="fertilizer-card"><h4>Potassium (K)</h4><p style="font-size: 18px;">Deficiency: {k_deficiency} kg/ha</p><p>Recommended: MOP or SOP</p></div>', unsafe_allow_html=True)
    
    # General fertilizer guidance
    st.markdown("### General Fertilizer Application Tips")
    st.info("""
    - Test soil every 2-3 years to adjust fertilizer recommendations
    - Apply fertilizers in split doses for better nutrient utilization
    - Incorporate organic matter to improve soil health
    - Consider slow-release fertilizers for longer nutrient availability
    - Always follow recommended application rates to avoid environmental damage
    """)

# Footer
st.markdown(f"""
<div class="footer">
    <p>{current_lang['created_by']} <span class="team-name">{current_lang['team_name']}</span> {current_lang['for_sih']}</p>
    <p>VARUN AI - Vikasit Adhunik Roopantaran ke liye Uttam Nirdesh</p>
</div>
""", unsafe_allow_html=True)










