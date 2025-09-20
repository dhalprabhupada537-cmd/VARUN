import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import time
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="VARUN AI Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== EMBEDDED LANGUAGE DATA (No import needed) =====
LANGUAGES = {
    'en': {
        'name': 'English',
        'direction': 'ltr',
        'states': {
            'Punjab': 'Punjab',
            'Haryana': 'Haryana', 
            'Uttar Pradesh': 'Uttar Pradesh',
            'Maharashtra': 'Maharashtra',
            'Karnataka': 'Karnataka',
            'Tamil Nadu': 'Tamil Nadu',
            'Andhra Pradesh': 'Andhra Pradesh',
            'Gujarat': 'Gujarat',
            'Odisha': 'Odisha',
            'Jharkhand': 'Jharkhand',
            'West Bengal': 'West Bengal',
            'Bihar': 'Bihar'
        },
        'ui': {
            'app_name': 'VARUN AI',
            'tagline': 'Vikasit Adhunik Roopantaran ke liye Uttam Nirdesh',
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
            'dashboard': 'Dashboard',
            'crop_recommendation': 'Crop Recommendation',
            'soil_analysis': 'Soil Analysis',
            'weather_forecast': 'Weather Forecast',
            'farm_overview': 'Farm Overview',
            'soil_nutrient_levels': 'Soil Nutrient Levels',
            'recommended_crop': 'Recommended Crop',
            'expected_yield': 'Expected Yield',
            'success_probability': 'Success Probability',
            'why_this_crop': 'Why this crop?',
            'planting_guide': 'Planting Guide',
            'best_planting_time': 'Best Planting Time',
            'water_requirements': 'Water Requirements',
            'fertilizer_recommendations': 'Fertilizer Recommendations',
            'harvest_timeline': 'Harvest Timeline',
            'market_insights': 'Market Insights',
            'current_market_price': 'Current market price',
            'demand_trend': 'Demand trend',
            'click_to_analyze': 'Click the button to get crop recommendations',
            'ph_level': 'pH Level',
            'moisture': 'Moisture',
            'organic_matter': 'Organic Matter',
            'wind_speed': 'Wind Speed',
            'created_by': 'Created with love by',
            'team_name': 'Team AgroNova',
            'for_sih': 'for SIH 2025',
            'language': 'Language',
            'select_language': 'Select Language'
        },
        'crops': {
            'Wheat': 'Wheat',
            'Rice': 'Rice',
            'Maize': 'Maize',
            'Cotton': 'Cotton',
            'Soybean': 'Soybean',
            'Pulses': 'Pulses'
        }
    },
    'hi': {
        'name': 'हिंदी',
        'direction': 'ltr',
        'states': {
            'Punjab': 'पंजाब',
            'Haryana': 'हरियाणा',
            'Uttar Pradesh': 'उत्तर प्रदेश',
            'Maharashtra': 'महाराष्ट्र',
            'Karnataka': 'कर्नाटक',
            'Tamil Nadu': 'तमिलनाडु',
            'Andhra Pradesh': 'आंध्र प्रदेश',
            'Gujarat': 'गुजरात',
            'Odisha': 'ओडिशा',
            'Jharkhand': 'झारखंड',
            'West Bengal': 'पश्चिम बंगाल',
            'Bihar': 'बिहार'
        },
        'ui': {
            'app_name': 'VARUN AI',
            'tagline': 'विकसित आधुनिक रूपांतरण के लिए उत्तम निर्देश',
            'farmer_details': 'किसान विवरण',
            'full_name': 'पूरा नाम',
            'region': 'क्षेत्र',
            'farm_size': 'खेत का आकार (एकड़)',
            'soil_properties': 'मिट्टी के गुण',
            'soil_type': 'मिट्टी का प्रकार',
            'soil_ph': 'मिट्टी का pH',
            'soil_moisture': 'मिट्टी की नमी (%)',
            'nitrogen': 'नाइट्रोजन (kg/ha)',
            'phosphorus': 'फॉस्फोरस (kg/ha)',
            'potassium': 'पोटैशियम (kg/ha)',
            'environmental_factors': 'पर्यावरणीय कारक',
            'temperature': 'तापमान (°C)',
            'rainfall': 'वार्षिक वर्षा (mm)',
            'humidity': 'आर्द्रता (%)',
            'analyze_button': 'विश्लेषण करें और सिफारिश करें',
            'dashboard': 'डैशबोर्ड',
            'crop_recommendation': 'फसल सिफारिश',
            'soil_analysis': 'मिट्टी विश्लेषण',
            'weather_forecast': 'मौसम पूर्वानुमान',
            'farm_overview': 'खेत का अवलोकन',
            'soil_nutrient_levels': 'मिट्टी के पोषक तत्वों के स्तर',
            'recommended_crop': 'सिफारिश की गई फसल',
            'expected_yield': 'अनुमानित उपज',
            'success_probability': 'सफलता की संभावना',
            'why_this_crop': 'यह फसल क्यों?',
            'planting_guide': 'रोपण मार्गदर्शिका',
            'best_planting_time': 'सर्वोत्तम रोपण समय',
            'water_requirements': 'पानी की आवश्यकताएं',
            'fertilizer_recommendations': 'उर्वरक सिफारिशें',
            'harvest_timeline': 'फसल कटाई की समयसीमा',
            'market_insights': 'बाजार की जानकारी',
            'current_market_price': 'वर्तमान बाजार मूल्य',
            'demand_trend': 'मांग की प्रवृत्ति',
            'click_to_analyze': 'फसल सिफारिशें प्राप्त करने के लिए बटन पर क्लिक करें',
            'ph_level': 'pH स्तर',
            'moisture': 'नमी',
            'organic_matter': 'कार्बनिक पदार्थ',
            'wind_speed': 'हवा की गति',
            'created_by': 'प्यार से बनाया गया',
            'team_name': 'टीम एग्रोनोवा',
            'for_sih': 'एसआईएच 2025 के लिए',
            'language': 'भाषा',
            'select_language': 'भाषा चुनें'
        },
        'crops': {
            'Wheat': 'गेहूं',
            'Rice': 'चावल',
            'Maize': 'मक्का',
            'Cotton': 'कपास',
            'Soybean': 'सोयाबीन',
            'Pulses': 'दलहन'
        }
    },
    'or': {
        'name': 'ଓଡିଆ',
        'direction': 'ltr',
        'states': {
            'Punjab': 'ପଞ୍ଜାବ',
            'Haryana': 'ହରିୟାଣା',
            'Uttar Pradesh': 'ଉତ୍ତର ପ୍ରଦେଶ',
            'Maharashtra': 'ମହାରାଷ୍ଟ୍ର',
            'Karnataka': 'କର୍ଣାଟକ',
            'Tamil Nadu': 'ତାମିଲନାଡୁ',
            'Andhra Pradesh': 'ଆନ୍ଧ୍ର ପ୍ରଦେଶ',
            'Gujarat': 'ଗୁଜରାଟ',
            'Odisha': 'ଓଡିଶା',
            'Jharkhand': 'ଝାଡଖଣ୍ଡ',
            'West Bengal': 'ପଶ୍ଚିମ ବଙ୍ଗ',
            'Bihar': 'ବିହାର'
        },
        'ui': {
            'app_name': 'VARUN AI',
            'tagline': 'ବିକଶିତ ଆଧୁନିକ ରୂପାନ୍ତରଣ ପାଇଁ ଉତ୍ତମ �ନିର୍ଦେଶ',
            'farmer_details': 'କୃଷକର ବିବରଣୀ',
            'full_name': 'ପୂରା ନାମ',
            'region': 'ଅଞ୍ଚଳ',
            'farm_size': 'ଚାଷ ଜମିର ଆକାର (ଏକର)',
            'soil_properties': 'ମୃତ୍ତିକାର ଗୁଣ',
            'soil_type': 'ମୃତ୍ତିକାର ପ୍ରକାର',
            'soil_ph': 'ମୃତ୍ତିକାର pH',
            'soil_moisture': 'ମୃତ୍ତିକାର ଆର୍ଦ୍ରତା (%)',
            'nitrogen': 'ନାଇଟ୍ରୋଜେନ୍ (kg/ha)',
            'phosphorus': 'ଫସଫରସ୍ (kg/ha)',
            'potassium': 'ପଟାସିଅମ୍ (kg/ha)',
            'environmental_factors': 'ପରିବେଶଗତ କାରକ',
            'temperature': 'ତାପମାତ୍ରା (°C)',
            'rainfall': 'ବାର୍ଷିକ ବର୍ଷା (mm)',
            'humidity': 'ଆର୍ଦ୍ରତା (%)',
            'analyze_button': 'ବିଶ୍ଳେଷଣ କର ଏବଂ ପରାମର୍ଶ ଦିଅ',
            'dashboard': 'ଡ୍ୟାସବୋର୍ଡ',
            'crop_recommendation': 'ଫସଲ ପରାମର୍ଶ',
            'soil_analysis': 'ମୃତ୍ତିକା ବିଶ୍ଳେଷଣ',
            'weather_forecast': 'ପାଣିପାଗ ପୂର୍ବାନୁମାନ',
            'farm_overview': 'ଚାଷ ଜମିର ସମୀକ୍ଷା',
            'soil_nutrient_levels': 'ମୃତ୍ତିକାର ପୋଷକ ତତ୍ତ୍ୱର ସ୍ତର',
            'recommended_crop': 'ପରାମର୍ଶିତ ଫସଲ',
            'expected_yield': 'ଆଶାକୃତ ଉତ୍ପାଦନ',
            'success_probability': 'ସଫଳତାର ସମ୍ଭାବନା',
            'why_this_crop': 'ଏହି ଫସଲ କାହିଁକି?',
            'planting_guide': 'ରୋପଣ ମାର୍ଗଦର୍ଶିକା',
            'best_planting_time': 'ସର୍ବୋତ୍ତମ ରୋପଣ ସଞ୍ଚୟ',
            'water_requirements': 'ଜଳ ଆବଶ୍ୟକତା',
            'fertilizer_recommendations': 'ସାର ପରାମର୍ଶ',
            'harvest_timeline': 'ଫସଲ କଟାଇ ସମୟସୀମା',
            'market_insights': 'ବଜାରର ଅନ୍ତର୍ଦୃଷ୍ଟି',
            'current_market_price': 'ବର୍ତ୍ତମାନର ବଜାର ମୂଲ୍ୟ',
            'demand_trend': 'ଚାହିଦା ପ୍ରବୃତ୍ତି',
            'click_to_analyze': 'ଫସଲ ପରାମର୍ଶ ପାଇବା ପାଇଁ ବଟନ୍ ଦବାନ୍ତୁ',
            'ph_level': 'pH ସ୍ତର',
            'moisture': 'ଆର୍ଦ୍ରତା',
            'organic_matter': 'ଜୈବିକ ପଦାର୍ଥ',
            'wind_speed': 'ପବନର ଗତି',
            'created_by': 'ଭାଲୋବାସା କରି ତିଆରି କରାଯାଇଛି',
            'team_name': 'ଦଳ ଆଗ୍ରୋନୋଭା',
            'for_sih': 'SIH 2025 ପାଇଁ',
            'language': 'ଭାଷା',
            'select_language': 'ଭାଷା ଚୟନ କରନ୍ତୁ'
        },
        'crops': {
            'Wheat': 'ଗହମ',
            'Rice': 'ଚାଉଳ',
            'Maize': 'ମକା',
            'Cotton': 'କପାହ',
            'Soybean': 'ସୋୟାବିନ',
            'Pulses': 'ଡାଲି'
        }
    }
}

# State to language mapping
STATE_LANGUAGE_MAPPING = {
    'Odisha': 'or',
    'Jharkhand': 'hi',
    'Bihar': 'hi',
    'Punjab': 'hi',
    'Haryana': 'hi',
    'Uttar Pradesh': 'hi',
    'Default': 'en'
}

def get_language_for_state(state):
    """Get the default language for a given state"""
    return STATE_LANGUAGE_MAPPING.get(state, STATE_LANGUAGE_MAPPING['Default'])

def get_available_languages():
    """Return list of available languages"""
    return list(LANGUAGES.keys())

def get_state_name(state, lang):
    """Get translated state name"""
    return LANGUAGES[lang]['states'].get(state, state)

# ===== EMBEDDED CSS STYLING =====
def get_css():
    return """
    <style>
    :root {
        --primary-color: #2E8B57;
        --secondary-color: #3CB371;
        --accent-color: #4CAF50;
        --background-color: #FFFFFF;
        --card-background: #F8F9FA;
        --text-color: #333333;
        --border-color: #E0E0E0;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --hover-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #1E1E1E;
            --card-background: #2D2D2D;
            --text-color: #FFFFFF;
            --border-color: #404040;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            --hover-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
        }
    }

    .main-header {
        font-size: 3rem;
        color: var(--primary-color);
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .tagline {
        font-size: 1.1rem;
        color: var(--secondary-color);
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
        font-style: italic;
    }

    .sub-header {
        font-size: 1.6rem;
        color: var(--primary-color);
        border-bottom: 2px solid var(--secondary-color);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .card {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .card:hover {
        box-shadow: var(--hover-shadow);
        transform: translateY(-2px);
    }

    .recommendation-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid var(--accent-color);
        box-shadow: var(--shadow);
        margin: 1.5rem 0;
    }

    .weather-card {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }

    .soil-image {
        border-radius: 12px;
        width: 100%;
        height: 200px;
        object-fit: cover;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }

    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border-radius: 12px;
        box-shadow: var(--shadow);
    }

    .team-name {
        font-weight: bold;
        color: #FFD700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    .language-selector {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: var(--card-background);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-color) 0%, #8BC34A 100%);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }
    </style>
    """

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'last_state' not in st.session_state:
    st.session_state.last_state = ''

# Apply custom CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Helper function to get translated text
def t(key, lang=None):
    """Get translated text for the given key"""
    if lang is None:
        lang = st.session_state.language
    
    # Navigate through nested keys (e.g., 'ui.farmer_details')
    keys = key.split('.')
    value = LANGUAGES[lang]
    
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            # Fallback to English if translation not found
            if lang != 'en':
                return t(key, 'en')
            return key  # Return the key itself as last resort
    
    return value

# Generate soil images if they don't exist
def generate_soil_images():
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
            
            img.save(img_path)

# Generate logo if it doesn't exist
def generate_logo():
    if not os.path.exists("assets/logo.png"):
        img = Image.new('RGB', (400, 200), color=(46, 139, 87))
        draw = ImageDraw.Draw(img)
        
        # Draw VARUN text
        draw.text((120, 70), "VARUN", fill=(255, 255, 255))
        draw.text((130, 120), "ai", fill=(255, 215, 0))
        
        # Draw plant icon
        draw.ellipse([(30, 70), (90, 130)], fill=(255, 215, 0))
        img.save("assets/logo.png")

# Generate images
os.makedirs("assets", exist_ok=True)
generate_logo()
generate_soil_images()

# Language selector at top right
with st.container():
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        st.markdown('<div class="language-selector">', unsafe_allow_html=True)
        selected_language = st.selectbox(
            "🌐",
            options=get_available_languages(),
            format_func=lambda x: LANGUAGES[x]['name'],
            key='language_selector',
            index=get_available_languages().index(st.session_state.language),
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Update language when selector changes
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()

# App header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f'<h1 class="main-header">VARUN<span style="color: #FFD700;">ai</span></h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="tagline">{t("ui.tagline")}</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", width=280)
    st.markdown(f"## {t('ui.farmer_details')}")
    
    farmer_name = st.text_input(t('ui.full_name'))
    
    # Get state names in current language
    state_options = list(LANGUAGES['en']['states'].keys())
    state_display_names = [get_state_name(state, st.session_state.language) for state in state_options]
    
    selected_state_index = st.selectbox(
        t('ui.region'),
        range(len(state_options)),
        format_func=lambda i: state_display_names[i]
    )
    
    farm_location = state_options[selected_state_index]
    
    # Update language based on state selection
    if farm_location and farm_location != st.session_state.last_state:
        state_language = get_language_for_state(farm_location)
        if state_language != st.session_state.language:
            st.session_state.language = state_language
            st.session_state.last_state = farm_location
            st.rerun()
    
    farm_size = st.slider(t('ui.farm_size'), 1, 100, 10)
    
    st.markdown(f"## {t('ui.soil_properties')}")
    soil_type = st.selectbox(t('ui.soil_type'), ["Loam", "Clay", "Sandy", "Silt"])
    soil_ph = st.slider(t('ui.soil_ph'), 4.0, 9.0, 6.5)
    soil_moisture = st.slider(t('ui.soil_moisture'), 0, 100, 50)
    nitrogen = st.slider(t('ui.nitrogen'), 0, 200, 50)
    phosphorus = st.slider(t('ui.phosphorus'), 0, 200, 40)
    potassium = st.slider(t('ui.potassium'), 0, 200, 60)
    
    st.markdown(f"## {t('ui.environmental_factors')}")
    temperature = st.slider(t('ui.temperature'), 0, 45, 25)
    rainfall = st.slider(t('ui.rainfall'), 0, 2000, 800)
    humidity = st.slider(t('ui.humidity'), 0, 100, 60)
    
    analyze_button = st.button(t('ui.analyze_button'), type="primary", use_container_width=True)

# Crop recommendation model
def predict_best_crop(soil_type, ph, nitrogen, phosphorus, potassium, temperature, rainfall, humidity, region):
    # Regional crop preferences
    regional_preferences = {
        "Punjab": ["Wheat", "Rice", "Cotton", "Maize"],
        "Haryana": ["Wheat", "Rice", "Cotton", "Mustard"],
        "Uttar Pradesh": ["Wheat", "Rice", "Sugarcane", "Potato"],
        "Maharashtra": ["Cotton", "Soybean", "Pulses", "Sugarcane"],
        "Karnataka": ["Rice", "Cotton", "Pulses", "Coffee"],
        "Tamil Nadu": ["Rice", "Sugarcane", "Cotton", "Groundnut"],
        "Andhra Pradesh": ["Rice", "Cotton", "Chilli", "Groundnut"],
        "Gujarat": ["Cotton", "Groundnut", "Wheat", "Pulses"],
        "Odisha": ["Rice", "Pulses", "Oilseeds", "Millets"],
        "Jharkhand": ["Rice", "Pulses", "Oilseeds", "Maize"],
        "West Bengal": ["Rice", "Jute", "Tea", "Potato"],
        "Bihar": ["Rice", "Wheat", "Maize", "Pulses"]
    }
    
    # Crop data with optimal conditions
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
        }
    ]
    
    # Calculate scores
    scores = []
    for crop in crops:
        score = 0
        
        # Regional preference (higher weight)
        if crop['name'] in regional_preferences.get(region, []):
            score += 30
        
        # Soil type match
        if crop['soil_type'].lower() == soil_type.lower():
            score += 25
        
        # pH suitability
        if crop['ph_min'] <= ph <= crop['ph_max']:
            score += 15
        else:
            score -= 10 * abs(ph - (crop['ph_min'] + crop['ph_max'])/2)
        
        # Temperature suitability
        if crop['temp_min'] <= temperature <= crop['temp_max']:
            score += 10
        else:
            score -= 5 * abs(temperature - (crop['temp_min'] + crop['temp_max'])/2)
        
        # Rainfall suitability
        if crop['rainfall_min'] <= rainfall <= crop['rainfall_max']:
            score += 10
        else:
            score -= 3 * abs(rainfall - (crop['rainfall_min'] + crop['rainfall_max'])/2)
        
        # Nutrient suitability
        n_score = 8 if crop['n_min'] <= nitrogen <= crop['n_max'] else -2 * abs(nitrogen - (crop['n_min'] + crop['n_max'])/2)
        p_score = 8 if crop['p_min'] <= phosphorus <= crop['p_max'] else -2 * abs(phosphorus - (crop['p_min'] + crop['p_max'])/2)
        k_score = 9 if crop['k_min'] <= potassium <= crop['k_max'] else -2 * abs(potassium - (crop['k_min'] + crop['k_max'])/2)
        
        score += n_score + p_score + k_score
        scores.append(score)
    
    # Get best crop
    best_idx = np.argmax(scores)
    best_crop = crops[best_idx]
    
    # Generate recommendation
    planting_times = {
        'Wheat': t('crops.Wheat') + ' - October-November',
        'Rice': t('crops.Rice') + ' - June-July', 
        'Maize': t('crops.Maize') + ' - April-May',
        'Cotton': t('crops.Cotton') + ' - May-June',
        'Soybean': t('crops.Soybean') + ' - June-July',
        'Pulses': t('crops.Pulses') + ' - October-November'
    }
    
    return {
        'crop': t(f'crops.{best_crop["name"]}'),
        'probability': min(95, max(65, int(scores[best_idx]))),
        'yield': f"{np.random.uniform(2.0, 5.0):.1f}",
        'reason': f"{t(f'crops.{best_crop['name']}')} is ideal for {region}'s climate and your soil conditions ({soil_type} soil, pH {ph}).",
        'planting_time': planting_times.get(best_crop['name'], 'Varies by region'),
        'water_req': 'Moderate (600-800 mm)' if best_crop['name'] in ['Wheat', 'Maize'] else 
                     'High (1000-1500 mm)' if best_crop['name'] == 'Rice' else
                     'Low (400-600 mm)' if best_crop['name'] == 'Cotton' else 'Moderate (500-700 mm)',
        'fertilizer': 'N:P:K = 60:40:40 kg/ha' if best_crop['name'] == 'Wheat' else 
                      'N:P:K = 80:40:40 kg/ha' if best_crop['name'] == 'Rice' else
                      'N:P:K = 100:50:50 kg/ha' if best_crop['name'] == 'Maize' else
                      'N:P:K = 50:25:25 kg/ha' if best_crop['name'] == 'Cotton' else 'N:P:K = 40:60:40 kg/ha',
        'harvest_time': 'March-April' if best_crop['name'] == 'Wheat' else 
                        'October-November' if best_crop['name'] == 'Rice' else
                        'August-September' if best_crop['name'] == 'Maize' else
                        'October-December' if best_crop['name'] == 'Cotton' else 'September-October',
        'market_price': f"₹{np.random.randint(25, 55)}",
        'demand_trend': 'High' if best_crop['name'] in ['Rice', 'Wheat'] else 'Stable'
    }

# Main content
tab1, tab2, tab3, tab4 = st.tabs([
    t('ui.dashboard'), 
    t('ui.crop_recommendation'), 
    t('ui.soil_analysis'), 
    t('ui.weather_forecast')
])

with tab1:
    st.markdown(f'<h2 class="sub-header">{t("ui.farm_overview")}</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.markdown(f'<div class="card"><div class="metric-label">{t("ui.farm_size")}</div><div class="metric-value">{farm_size} acres</div></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="card"><div class="metric-label">{t("ui.soil_type")}</div><div class="metric-value">{soil_type}</div></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown(f'<div class="card"><div class="metric-label">{t("ui.region")}</div><div class="metric-value">{get_state_name(farm_location, st.session_state.language)}</div></div>', unsafe_allow_html=True)

with tab2:
    st.markdown(f'<h2 class="sub-header">{t("ui.crop_recommendation")}</h2>', unsafe_allow_html=True)
    
    if analyze_button:
        with st.spinner('Analyzing your farm data and generating recommendations...'):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            recommendation = predict_best_crop(soil_type, soil_ph, nitrogen, phosphorus, 
                                             potassium, temperature, rainfall, humidity, farm_location)
            
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown(f"### 🌱 {t('ui.recommended_crop')}: **{recommendation['crop']}**")
            st.markdown(f"**{t('ui.expected_yield')}:** {recommendation['yield']} tons/acre")
            st.markdown(f"**{t('ui.success_probability')}:** {recommendation['probability']}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f"#### {t('ui.why_this_crop')}")
            st.info(recommendation['reason'])
            
            st.markdown(f"#### {t('ui.planting_guide')}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{t('ui.best_planting_time')}**")
                st.write(recommendation['planting_time'])
                
                st.markdown(f"**{t('ui.water_requirements')}**")
                st.write(recommendation['water_req'])
            
            with col2:
                st.markdown(f"**{t('ui.fertilizer_recommendations')}**")
                st.write(recommendation['fertilizer'])
                
                st.markdown(f"**{t('ui.harvest_timeline')}**")
                st.write(recommendation['harvest_time'])
            
            st.markdown(f"#### {t('ui.market_insights')}")
            st.success(f"{t('ui.current_market_price')}: {recommendation['market_price']} per kg")
            st.write(f"{t('ui.demand_trend')}: {recommendation['demand_trend']}")
    
    else:
        st.info(t('ui.click_to_analyze'))

with tab3:
    st.markdown(f'<h2 class="sub-header">{t("ui.soil_analysis")}</h2>', unsafe_allow_html=True)
    
    # Load soil image with error handling
    try:
        soil_img = Image.open(f"assets/soil_types/{soil_type.lower()}.png")
        st.image(soil_img, caption=f"{soil_type} {t('ui.soil_type')}", use_container_width=True)
    except FileNotFoundError:
        st.warning("Soil image not found. Please run generate_images.py to create soil images.")
        # Create a simple colored placeholder
        soil_colors = {
            "clay": (180, 120, 80),
            "loam": (160, 100, 60),
            "sand": (220, 200, 160),
            "silt": (200, 180, 140)
        }
        color = soil_colors.get(soil_type.lower(), (200, 200, 200))
        placeholder = Image.new('RGB', (400, 300), color=color)
        draw = ImageDraw.Draw(placeholder)
        draw.text((150, 140), soil_type.upper(), fill=(255, 255, 255))
        st.image(placeholder, caption=f"{soil_type} {t('ui.soil_type')} (Placeholder)", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.markdown(f'<div class="weather-card"><div class="metric-label">{t("ui.ph_level")}</div><div class="metric-value">{soil_ph}</div></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><div class="metric-label">{t("ui.moisture")}</div><div class="metric-value">{soil_moisture}%</div></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown(f'<div class="weather-card"><div class="metric-label">{t("ui.organic_matter")}</div><div class="metric-value">3.2%</div></div>', unsafe_allow_html=True)

with tab4:
    st.markdown(f'<h2 class="sub-header">{t("ui.weather_forecast")}</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown(f'<div class="weather-card"><div class="metric-label">{t("ui.temperature")}</div><div class="metric-value">{temperature}°C</div></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><div class="metric-label">{t("ui.humidity")}</div><div class="metric-value">{humidity}%</div></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown(f'<div class="weather-card"><div class="metric-label">{t("ui.rainfall")}</div><div class="metric-value">{rainfall} mm</div></div>', unsafe_allow_html=True)
    with col4: 
        st.markdown(f'<div class="weather-card"><div class="metric-label">{t("ui.wind_speed")}</div><div class="metric-value">12 km/h</div></div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
    <p>{t('ui.created_by')} <span class="team-name">{t('ui.team_name')}</span> {t('ui.for_sih')}</p>
    <p>VARUN AI - {t('ui.tagline')}</p>
</div>
""", unsafe_allow_html=True)
