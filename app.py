import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
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

# Custom CSS with VARUN branding
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2E8B57;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
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
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px 0 rgba(0,0,0,0.2);
        margin: 15px 0;
        background-color: #FFFFFF;
        border-left: 5px solid #4CAF50;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
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
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        background-color: #2E8B57;
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
</style>
""", unsafe_allow_html=True)

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
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            draw.text((120, 120), soil_type.upper(), fill=(255, 255, 255), font=font)
            img.save(img_path)

# Generate logo if it doesn't exist
def generate_logo():
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
        img.save("assets/logo.png")

# Generate images
os.makedirs("assets", exist_ok=True)
generate_logo()
generate_soil_images()

# App header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="main-header">VARUN<span style="color: #FFD700;">ai</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Vikasit Adhunik Roopantaran ke liye Uttam Nirdesh</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", width=280)
    st.markdown("## Farmer Details")
    
    farmer_name = st.text_input("Full Name")
    farm_location = st.selectbox("Region", ["Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", 
                                           "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Gujarat",
                                           "Odisha", "Jharkhand", "West Bengal", "Bihar"])
    farm_size = st.slider("Farm Size (acres)", 1, 100, 10)
    
    st.markdown("## Soil Properties")
    soil_type = st.selectbox("Soil Type", ["Loam", "Clay", "Sandy", "Silt"])
    soil_ph = st.slider("Soil pH", 4.0, 9.0, 6.5)
    soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 50)
    nitrogen = st.slider("Nitrogen (kg/ha)", 0, 200, 50)
    phosphorus = st.slider("Phosphorus (kg/ha)", 0, 200, 40)
    potassium = st.slider("Potassium (kg/ha)", 0, 200, 60)
    
    st.markdown("## Environmental Factors")
    temperature = st.slider("Temperature (°C)", 0, 45, 25)
    rainfall = st.slider("Annual Rainfall (mm)", 0, 2000, 800)
    humidity = st.slider("Humidity (%)", 0, 100, 60)
    
    analyze_button = st.button("Analyze & Recommend", type="primary")

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
        'Wheat': 'October-November',
        'Rice': 'June-July', 
        'Maize': 'April-May',
        'Cotton': 'May-June',
        'Soybean': 'June-July',
        'Pulses': 'October-November'
    }
    
    return {
        'crop': best_crop['name'],
        'probability': min(95, max(65, int(scores[best_idx]))),
        'yield': f"{np.random.uniform(2.0, 5.0):.1f}",
        'reason': f"{best_crop['name']} is ideal for {region}'s climate and your soil conditions ({soil_type} soil, pH {ph}).",
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
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Crop Recommendation", "Soil Analysis", "Weather Forecast"])

with tab1:
    st.markdown('<h2 class="sub-header">Farm Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="card"><h3>Farm Size</h3><p style="font-size: 24px; color: #2E8B57;">' + str(farm_size) + ' acres</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="card"><h3>Soil Type</h3><p style="font-size: 24px; color: #2E8B57;">' + soil_type + '</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="card"><h3>Region</h3><p style="font-size: 24px; color: #2E8B57;">' + farm_location + '</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 class="sub-header">Crop Recommendation</h2>', unsafe_allow_html=True)
    
    if analyze_button:
        with st.spinner('Analyzing your farm data and generating recommendations...'):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            recommendation = predict_best_crop(soil_type, soil_ph, nitrogen, phosphorus, 
                                             potassium, temperature, rainfall, humidity, farm_location)
            
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown(f"### 🌱 Recommended Crop: **{recommendation['crop']}**")
            st.markdown(f"**Expected Yield:** {recommendation['yield']} tons/acre")
            st.markdown(f"**Success Probability:** {recommendation['probability']}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("#### Why this crop?")
            st.info(recommendation['reason'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Best Planting Time**")
                st.write(recommendation['planting_time'])
                st.markdown("**Water Requirements**")
                st.write(recommendation['water_req'])
            with col2:
                st.markdown("**Fertilizer Recommendations**")
                st.write(recommendation['fertilizer'])
                st.markdown("**Harvest Timeline**")
                st.write(recommendation['harvest_time'])
            
            st.markdown("#### Market Insights")
            st.success(f"Current market price: {recommendation['market_price']} per kg")
            st.write(f"Demand trend: {recommendation['demand_trend']}")
    
    else:
        st.info("Click the 'Analyze & Recommend' button in the sidebar to get crop recommendations")

with tab3:
    st.markdown('<h2 class="sub-header">Soil Analysis</h2>', unsafe_allow_html=True)
    
    soil_img = Image.open(f"assets/soil_types/{soil_type.lower()}.png")
    st.image(soil_img, caption=f"{soil_type} Soil", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="weather-card"><h4>pH Level</h4><p style="font-size: 20px;">' + str(soil_ph) + '</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="weather-card"><h4>Moisture</h4><p style="font-size: 20px;">' + str(soil_moisture) + '%</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="weather-card"><h4>Organic Matter</h4><p style="font-size: 20px;">3.2%</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<h2 class="sub-header">Weather Forecast</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="weather-card"><h4>Temperature</h4><p style="font-size: 20px;">' + str(temperature) + '°C</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="weather-card"><h4>Humidity</h4><p style="font-size: 20px;">' + str(humidity) + '%</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="weather-card"><h4>Rainfall</h4><p style="font-size: 20px;">' + str(rainfall) + ' mm</p></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="weather-card"><h4>Wind Speed</h4><p style="font-size: 20px;">12 km/h</p></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Created with ❤️ by <span class="team-name">Team AgroNova</span> for SIH 2025</p>
    <p>VARUN AI - Vikasit Adhunik Roopantaran ke liye Uttam Nirdesh</p>
</div>
""", unsafe_allow_html=True)