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
    .analysis-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
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
            img.save("assets/logo.png")
    except Exception as e:
        st.error(f"Error generating logo: {e}")

# Generate images
try:
    os.makedirs("assets", exist_ok=True)
    generate_logo()
    generate_soil_images()
except Exception as e:
    st.error(f"Error creating assets directory: {e}")

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
    farm_location = st.selectbox("Region (Optional)", ["Select", "Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", 
                                           "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Gujarat",
                                           "Odisha", "Jharkhand", "West Bengal", "Bihar"])
    farm_size = st.slider("Farm Size (acres)", 1, 100, 10)
    
    st.markdown("## Soil Properties")
    soil_type = st.selectbox("Soil Type (Optional)", ["Select", "Loam", "Clay", "Sandy", "Silt"])
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
            'fertilizer': 'N:P:K = 60:40:40 kg/ha' if crop_name == 'Wheat' else 
                          'N:P:K = 80:40:40 kg/ha' if crop_name == 'Rice' else
                          'N:P:K = 100:50:50 kg/ha' if crop_name == 'Maize' else
                          'N:P:K = 50:25:25 kg/ha' if crop_name == 'Cotton' else 
                          'N:P:K = 40:60:40 kg/ha' if crop_name == 'Soybean' else
                          'N:P:K = 150:60:100 kg/ha' if crop_name == 'Sugarcane' else
                          'N:P:K = 20:50:40 kg/ha',
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
                            'Stable'
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

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Crop Recommendation", "Soil Analysis", "Weather Forecast"])

with tab1:
    st.markdown('<h2 class="sub-header">Farm Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="card"><h3>Farm Size</h3><p style="font-size: 24px; color: #2E8B57;">' + str(farm_size) + ' acres</p></div>', unsafe_allow_html=True)
    with col2: 
        soil_display = soil_type if soil_type != "Select" else "Not specified"
        st.markdown('<div class="card"><h3>Soil Type</h3><p style="font-size: 24px; color: #2E8B57;">' + soil_display + '</p></div>', unsafe_allow_html=True)
    with col3: 
        region_display = farm_location if farm_location != "Select" else "Not specified"
        st.markdown('<div class="card"><h3>Region</h3><p style="font-size: 24px; color: #2E8B57;">' + region_display + '</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 class="sub-header">Crop Recommendation</h2>', unsafe_allow_html=True)
    
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
            st.markdown(f"### 🌱 Top Recommendation: **{top_recommendation['crop']}**")
            st.markdown(f"**Expected Yield:** {top_recommendation['yield']} tons/acre")
            st.markdown(f"**Success Probability:** {top_recommendation['probability']}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display suitability chart
            st.plotly_chart(create_suitability_chart(top_recommendation['details'], top_recommendation['crop']), 
                           use_container_width=True)
            
            # Display reasons
            st.markdown("#### Why this crop?")
            for reason in top_recommendation['reasons']:
                st.info(f"• {reason}")
            
            # Display crop details
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Best Planting Time**")
                st.write(top_recommendation['planting_time'])
                st.markdown("**Water Requirements**")
                st.write(top_recommendation['water_req'])
            with col2:
                st.markdown("**Fertilizer Recommendations**")
                st.write(top_recommendation['fertilizer'])
                st.markdown("**Harvest Timeline**")
                st.write(top_recommendation['harvest_time'])
            
            # Display market insights
            st.markdown("#### Market Insights")
            st.success(f"Current market price: {top_recommendation['market_price']} per kg")
            st.write(f"Demand trend: {top_recommendation['demand_trend']}")
            
            # Show alternative options
            if len(recommendations) > 1:
                st.markdown("#### Alternative Options")
                cols = st.columns(len(recommendations) - 1)
                for idx, rec in enumerate(recommendations[1:]):
                    with cols[idx]:
                        st.markdown(f'<div class="analysis-card"><h4>{rec["crop"]}</h4><p>Score: {rec["score"]:.1f}</p><p>Probability: {rec["probability"]}%</p></div>', 
                                  unsafe_allow_html=True)
    
    else:
        st.info("Click the 'Analyze & Recommend' button in the sidebar to get crop recommendations")

with tab3:
    st.markdown('<h2 class="sub-header">Soil Analysis</h2>', unsafe_allow_html=True)
    
    if soil_type != "Select":
        try:
            soil_img = Image.open(f"assets/soil_types/{soil_type.lower()}.png")
            st.image(soil_img, caption=f"{soil_type} Soil", use_container_width=True)
        except:
            st.warning("Soil image not available")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown('<div class="weather-card"><h4>pH Level</h4><p style="font-size: 20px;">' + str(soil_ph) + '</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown('<div class="weather-card"><h4>Moisture</h4><p style="font-size: 20px;">' + str(soil_moisture) + '%</p></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown('<div class="weather-card"><h4>Nitrogen</h4><p style="font-size: 20px;">' + str(nitrogen) + ' kg/ha</p></div>', unsafe_allow_html=True)
    with col4: 
        st.markdown('<div class="weather-card"><h4>Organic Matter</h4><p style="font-size: 20px;">3.2%</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: 
        st.markdown('<div class="weather-card"><h4>Phosphorus</h4><p style="font-size: 20px;">' + str(phosphorus) + ' kg/ha</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown('<div class="weather-card"><h4>Potassium</h4><p style="font-size: 20px;">' + str(potassium) + ' kg/ha</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<h2 class="sub-header">Weather Forecast</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown('<div class="weather-card"><h4>Temperature</h4><p style="font-size: 20px;">' + str(temperature) + '°C</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown('<div class="weather-card"><h4>Humidity</h4><p style="font-size: 20px;">' + str(humidity) + '%</p></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown('<div class="weather-card"><h4>Rainfall</h4><p style="font-size: 20px;">' + str(rainfall) + ' mm</p></div>', unsafe_allow_html=True)
    with col4: 
        st.markdown('<div class="weather-card"><h4>Wind Speed</h4><p style="font-size: 20px;">12 km/h</p></div>', unsafe_allow_html=True)
    
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

# Footer
st.markdown("""
<div class="footer">
    <p>Created with ❤️ by <span class="team-name">Team AgroNova</span> for SIH 2025</p>
    <p>VARUN AI - Vikasit Adhunik Roopantaran ke liye Uttam Nirdesh</p>
</div>
""", unsafe_allow_html=True)
