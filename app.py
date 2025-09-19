import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time
from datetime import datetime, timedelta
import os

# Import custom modules
from crop_data import predict_best_crops
from image_generator import generate_soil_images, generate_logo

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
    .suitability-bar {
        height: 20px;
        background: linear-gradient(90deg, #ff4b4b 0%, #ffa500 50%, #4CAF50 100%);
        border-radius: 10px;
        margin: 5px 0;
    }
    .analysis-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate images
try:
    os.makedirs("assets", exist_ok=True)
    logo_success = generate_logo()
    soil_success = generate_soil_images()
except Exception as e:
    st.error(f"Error creating assets: {e}")

# App header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="main-header">VARUN<span style="color: #FFD700;">ai</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Vikasit Adhunik Roopantaran ke liye Uttam Nirdesh</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    try:
        st.image("assets/logo.png", width=280)
    except:
        st.warning("Logo image not found")
    
    st.markdown("## Farmer Details")
    
    farmer_name = st.text_input("Full Name")
    farm_location = st.selectbox("Region (Optional)", ["Select Region", "Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", 
                                           "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Gujarat",
                                           "Odisha", "Jharkhand", "West Bengal", "Bihar"])
    farm_size = st.slider("Farm Size (acres)", 1, 100, 10)
    
    st.markdown("## Soil Properties")
    soil_type = st.selectbox("Soil Type (Optional)", ["Select Soil Type", "Loam", "Clay", "Sandy", "Silt", "Clay Loam", "Sandy Loam", "Silt Loam"])
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

# Function to display suitability bars
def display_suitability_bars(reasons):
    """
    Display suitability factors as visual bars
    """
    for reason in reasons:
        # Extract percentage from the reason text
        if ":" in reason and "%" in reason:
            label, value_text = reason.split(":", 1)
            value = float(value_text.replace("%", "").strip())
            
            st.markdown(f"{label}")
            st.markdown(f'<div class="suitability-bar" style="width: {value}%;"></div>', unsafe_allow_html=True)
            st.markdown(f"{value:.1f}%")
            st.write("")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Crop Recommendation", "Soil Analysis", "Weather Forecast"])

with tab1:
    st.markdown('<h2 class="sub-header">Farm Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.markdown(f'<div class="card"><h3>Farm Size</h3><p style="font-size: 24px; color: #2E8B57;">{farm_size} acres</p></div>', unsafe_allow_html=True)
    with col2: 
        soil_display = soil_type if soil_type != "Select Soil Type" else "Not specified"
        st.markdown(f'<div class="card"><h3>Soil Type</h3><p style="font-size: 24px; color: #2E8B57;">{soil_display}</p></div>', unsafe_allow_html=True)
    with col3: 
        region_display = farm_location if farm_location != "Select Region" else "Not specified"
        st.markdown(f'<div class="card"><h3>Region</h3><p style="font-size: 24px; color: #2E8B57;">{region_display}</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 class="sub-header">Crop Recommendation</h2>', unsafe_allow_html=True)
    
    if analyze_button:
        with st.spinner('Analyzing your farm data and generating recommendations...'):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            # Handle optional parameters
            region = farm_location if farm_location != "Select Region" else None
            soil = soil_type if soil_type != "Select Soil Type" else None
            
            recommendations = predict_best_crops(
                soil, soil_ph, nitrogen, phosphorus, potassium, 
                temperature, rainfall, humidity, region
            )
            
            # Display top recommendation
            if recommendations:
                top_recommendation = recommendations[0]
                
                st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
                st.markdown(f"### 🌱 Recommended Crop: *{top_recommendation['crop']}*")
                st.markdown(f"*Suitability Score:* {top_recommendation['score']:.1f}%")
                st.markdown(f"*Expected Yield:* {top_recommendation['yield']} tons/acre")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display suitability factors
                st.markdown("#### Suitability Analysis")
                display_suitability_bars(top_recommendation['reasons'])
                
                # Display detailed analysis
                st.markdown("#### Detailed Analysis")
                for analysis_point in top_recommendation['analysis']:
                    st.markdown(f'<div class="analysis-box">{analysis_point}</div>', unsafe_allow_html=True)
                
                # Display crop details
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("*Best Planting Time*")
                    st.write(top_recommendation['planting_time'])
                    st.markdown("*Water Requirements*")
                    st.write(top_recommendation['water_req'])
                with col2:
                    st.markdown("*Fertilizer Recommendations*")
                    st.write(top_recommendation['fertilizer'])
                    st.markdown("*Harvest Timeline*")
                    st.write(top_recommendation['harvest_time'])
                
                # Display market insights
                st.markdown("#### Market Insights")
                st.success(f"Current market price: {top_recommendation['market_price']} per kg")
                st.write(f"Demand trend: {top_recommendation['demand_trend']}")
                
                # Show alternative options
                if len(recommendations) > 1:
                    st.markdown("#### Alternative Options")
                    for i, rec in enumerate(recommendations[1:], 1):
                        st.markdown(f"{i}. {rec['crop']}** (Suitability: {rec['score']:.1f}%)")
            else:
                st.error("No suitable crops found for your conditions. Please adjust your parameters.")
    
    else:
        st.info("Click the 'Analyze & Recommend' button in the sidebar to get crop recommendations")

with tab3:
    st.markdown('<h2 class="sub-header">Soil Analysis</h2>', unsafe_allow_html=True)
    
    if soil_type != "Select Soil Type":
        try:
            soil_img = Image.open(f"assets/soil_types/{soil_type.lower().replace('
