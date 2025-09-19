import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import time
from datetime import datetime, timedelta
import os

# Import language utilities and style
from utils.languages import LANGUAGES, get_language_for_state, get_available_languages, get_state_name
from utils.style import get_css

# Page configuration
st.set_page_config(
    page_title="VARUN AI Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            st.markdown(f"### 🌱 {t('ui.recommended_crop')}: *{recommendation['crop']}*")
            st.markdown(f"{t('ui.expected_yield')}:** {recommendation['yield']} tons/acre")
            st.markdown(f"{t('ui.success_probability')}:** {recommendation['probability']}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f"#### {t('ui.why_this_crop')}")
            st.info(recommendation['reason'])
            
            st.markdown(f"#### {t('ui.planting_guide')}")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"{t('ui.best_planting_time')}")
                st.write(recommendation['planting_time'])
                
                st.markdown(f"{t('ui.water_requirements')}")
                st.write(recommendation['water_req'])
            
            with col2:
                st.markdown(f"{t('ui.fertilizer_recommendations')}")
                st.write(recommendation['fertilizer'])
                
                st.markdown(f"{t('ui.harvest_timeline')}")
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
