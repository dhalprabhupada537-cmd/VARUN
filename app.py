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

# ===== EMBEDDED LANGUAGE DATA =====
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
            'Bihar': 'Bihar',
            'Select': 'Select Region'
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
            'select_language': 'Select Language',
            'not_specified': 'Not specified',
            'regional_preference': 'Regional Preference',
            'soil_type_match': 'Soil Type Match',
            'ph_suitability': 'pH Suitability',
            'temperature_suitability': 'Temperature Suitability',
            'rainfall_suitability': 'Rainfall Suitability',
            'nutrient_suitability': 'Nutrient Suitability',
            'alternative_options': 'Alternative Options',
            'detailed_factor_analysis': 'Detailed Factor Analysis',
            'suitability_analysis': 'Suitability Analysis for',
            'analysis_loading': 'Analyzing your farm data and generating recommendations...'
        },
        'crops': {
            'Wheat': 'Wheat',
            'Rice': 'Rice',
            'Maize': 'Maize',
            'Cotton': 'Cotton',
            'Soybean': 'Soybean',
            'Pulses': 'Pulses',
            'Sugarcane': 'Sugarcane',
            'Groundnut': 'Groundnut'
        },
        'reasons': {
            'highly_suitable': 'Highly suitable for {} region',
            'not_typical': 'Not typically grown in {}',
            'ideal_soil': 'Ideal for {} soil',
            'not_optimal_soil': 'Not optimal for {} soil (prefers {})',
            'optimal_ph': 'Optimal pH range ({}-{})',
            'ph_low': 'pH slightly low (ideal: {}-{})',
            'ph_high': 'pH slightly high (ideal: {}-{})',
            'optimal_temp': 'Optimal temperature range ({}-{}°C)',
            'temp_low': 'Temperature slightly low (ideal: {}-{}°C)',
            'temp_high': 'Temperature slightly high (ideal: {}-{}°C)',
            'optimal_rain': 'Optimal rainfall ({}-{}mm)',
            'rain_low': 'Rainfall slightly low (ideal: {}-{}mm)',
            'rain_high': 'Rainfall slightly high (ideal: {}-{}mm)',
            'nitrogen_issue': 'Nitrogen level not optimal for {}',
            'phosphorus_issue': 'Phosphorus level not optimal for {}',
            'potassium_issue': 'Potassium level not optimal for {}'
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
            'Bihar': 'बिहार',
            'Select': 'क्षेत्र चुनें'
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
            'select_language': 'भाषा चुनें',
            'not_specified': 'निर्दिष्ट नहीं',
            'regional_preference': 'क्षेत्रीय प्राथमिकता',
            'soil_type_match': 'मिट्टी प्रकार मिलान',
            'ph_suitability': 'pH उपयुक्तता',
            'temperature_suitability': 'तापमान उपयुक्तता',
            'rainfall_suitability': 'वर्षा उपयुक्तता',
            'nutrient_suitability': 'पोषक तत्व उपयुक्तता',
            'alternative_options': 'वैकल्पिक विकल्प',
            'detailed_factor_analysis': 'विस्तृत कारक विश्लेषण',
            'suitability_analysis': 'के लिए उपयुक्तता विश्लेषण',
            'analysis_loading': 'आपके फार्म डेटा का विश्लेषण और सिफारिशें तैयार की जा रही हैं...'
        },
        'crops': {
            'Wheat': 'गेहूं',
            'Rice': 'चावल',
            'Maize': 'मक्का',
            'Cotton': 'कपास',
            'Soybean': 'सोयाबीन',
            'Pulses': 'दलहन',
            'Sugarcane': 'गन्ना',
            'Groundnut': 'मूंगफली'
        },
        'reasons': {
            'highly_suitable': '{} क्षेत्र के लिए अत्यधिक उपयुक्त',
            'not_typical': '{} में आमतौर पर नहीं उगाया जाता',
            'ideal_soil': '{} मिट्टी के लिए आदर्श',
            'not_optimal_soil': '{} मिट्टी के लिए इष्टतम नहीं (पसंद करता है {})',
            'optimal_ph': 'इष्टतम pH सीमा ({}-{})',
            'ph_low': 'pH थोड़ा कम (आदर्श: {}-{})',
            'ph_high': 'pH थोड़ा अधिक (आदर्श: {}-{})',
            'optimal_temp': 'इष्टतम तापमान सीमा ({}-{}°C)',
            'temp_low': 'तापमान थोड़ा कम (आदर्श: {}-{}°C)',
            'temp_high': 'तापमान थोड़ा अधिक (आदर्श: {}-{}°C)',
            'optimal_rain': 'इष्टतम वर्षा ({}-{}mm)',
            'rain_low': 'वर्षा थोड़ी कम (आदर्श: {}-{}mm)',
            'rain_high': 'वर्षा थोड़ी अधिक (आदर्श: {}-{}mm)',
            'nitrogen_issue': '{} के लिए नाइट्रोजन स्तर इष्टतम नहीं',
            'phosphorus_issue': '{} के लिए फॉस्फोरस स्तर इष्टतम नहीं',
            'potassium_issue': '{} के लिए पोटैशियम स्तर इष्टतम नहीं'
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
            'Bihar': 'ବିହାର',
            'Select': 'ଅଞ୍ଚଳ ଚୟନ କରନ୍ତୁ'
        },
        'ui': {
            'app_name': 'VARUN AI',
            'tagline': 'ବିକଶିତ ଆଧୁନିକ ରୂପାନ୍ତରଣ ପାଇଁ ଉତ୍ତମ ନିର୍ଦେଶ',
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
            'best_planting_time': 'ସର୍ବୋତ୍ତମ ରୋପଣ ସମୟ',
            'water_requirements': 'ଜଳ ଆବଶ୍ୟକତା',
            'fertilizer_recommendations': 'ସାର ପରାମର୍ଶ',
            'harvest_timeline': 'ଫସଲ କଟାଇ ସମୟସୀଞା',
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
            'select_language': 'ଭାଷା ଚୟନ କରନ୍ତୁ',
            'not_specified': 'ନିର୍ଦ୍ଦିଷ୍ଟ ନୁହେଁ',
            'regional_preference': 'କ୍ଷେତ୍ରୀୟ ପସନ୍ଦ',
            'soil_type_match': 'ମାଟି ପ୍ରକାର ମେଳ',
            'ph_suitability': 'pH ଉପଯୁକ୍ତତା',
            'temperature_suitability': 'ତାପମାତ୍ରା ଉପଯୁକ୍ତତା',
            'rainfall_suitability': 'ବର୍ଷା ଉପଯୁକ୍ତତା',
            'nutrient_suitability': 'ପୋଷକ ଉପଯୁକ୍ତତା',
            'alternative_options': 'ବିକଳ୍ପ ବିକଳ୍ପ',
            'detailed_factor_analysis': 'ବିସ୍ତୃତ କାରକ ବିଶ୍ଳେଷଣ',
            'suitability_analysis': 'ପାଇଁ ଉପଯୁକ୍ତତା ବିଶ୍ଳେଷଣ',
            'analysis_loading': 'ଆପଣଙ୍କ ଫାର୍ମ ତଥ୍ୟ ବିଶ୍ଳେଷଣ ଏବଂ ପରାମର୍ଶ ପ୍ରସ୍ତୁତ କରାଯାଉଛି...'
        },
        'crops': {
            'Wheat': 'ଗହମ',
            'Rice': 'ଚାଉଳ',
            'Maize': 'ମକା',
            'Cotton': 'କପାହ',
            'Soybean': 'ସୋୟାବିନ',
            'Pulses': 'ଡାଲି',
            'Sugarcane': 'ଆଖୁ',
            'Groundnut': 'ଚିନାବାଦାମ'
        },
        'reasons': {
            'highly_suitable': '{} ଅଞ୍ଚଳ ପାଇଁ ଅତ୍ୟଧିକ ଉପଯୁକ୍ତ',
            'not_typical': '{} ରେ ସାଧାରଣତଃ ଚାଷ କରାଯାଏ ନାହିଁ',
            'ideal_soil': '{} ମାଟି ପାଇଁ ଆଦର୍ଶ',
            'not_optimal_soil': '{} ମାଟି ପାଇଁ ଉତ୍କୃଷ୍ଟ ନୁହେଁ (ପସନ୍ଦ କରେ {})',
            'optimal_ph': 'ଉତ୍କୃଷ୍ଟ pH ସୀମା ({}-{})',
            'ph_low': 'pH ଟିକେ କମ୍ (ଆଦର୍ଶ: {}-{})',
            'ph_high': 'pH ଟିକେ ଅଧିକ (ଆଦର୍ଶ: {}-{})',
            'optimal_temp': 'ଉତ୍କୃଷ୍ଟ ତାପମାତ୍ରା ସୀମା ({}-{}°C)',
            'temp_low': 'ତାପମାତ୍ରା ଟିକେ କମ୍ (ଆଦର୍ଶ: {}-{}°C)',
            'temp_high': 'ତାପମାତ୍ରା ଟିକେ ଅଧିକ (ଆଦର୍ଶ: {}-{}°C)',
            'optimal_rain': 'ଉତ୍କୃଷ୍ଟ ବର୍ଷା ({}-{}mm)',
            'rain_low': 'ବର୍ଷା ଟିକେ କମ୍ (ଆଦର୍ଶ: {}-{}mm)',
            'rain_high': 'ବର୍ଷା ଟିକେ ଅଧିକ (ଆଦର୍ଶ: {}-{}mm)',
            'nitrogen_issue': '{} ପାଇଁ ନାଇଟ୍ରୋଜେନ୍ ସ୍ତର ଉତ୍କୃଷ୍ଟ ନୁହେଁ',
            'phosphorus_issue': '{} ପାଇଁ ଫସଫରସ୍ ସ୍ତର ଉତ୍କୃଷ୍ଟ ନୁହେଁ',
            'potassium_issue': '{} ପାଇଁ ପଟାସିଅମ୍ ସ୍ତର ଉତ୍କୃଷ୍ଟ ନୁହେଁ'
        }
    },
    'ta': {
        'name': 'தமிழ்',
        'direction': 'ltr',
        'states': {
            'Punjab': 'பஞ்சாப்',
            'Haryana': 'ஹரியானா',
            'Uttar Pradesh': 'உத்தரப் பிரதேசம்',
            'Maharashtra': 'மகாராஷ்டிரா',
            'Karnataka': 'கர்நாடகா',
            'Tamil Nadu': 'தமிழ்நாடு',
            'Andhra Pradesh': 'ஆந்திரப் பிரதேசம்',
            'Gujarat': 'குஜராத்',
            'Odisha': 'ஒடிசா',
            'Jharkhand': 'ஜார்கண்ட்',
            'West Bengal': 'மேற்கு வங்காளம்',
            'Bihar': 'பீகார்',
            'Select': 'பிராந்தியத்தைத் தேர்ந்தெடுக்கவும்'
        },
        'ui': {
            'app_name': 'VARUN AI',
            'tagline': 'மேம்பட்ட நவீன மாற்றத்திற்கான சிறந்த வழிகாட்டி',
            'farmer_details': 'விவசாயி விவரங்கள்',
            'full_name': 'முழு பெயர்',
            'region': 'பிராந்தியம்',
            'farm_size': 'விவசாய நில அளவு (ஏக்கர்)',
            'soil_properties': 'மண் பண்புகள்',
            'soil_type': 'மண் வகை',
            'soil_ph': 'மண் pH',
            'soil_moisture': 'மண் ஈரப்பதம் (%)',
            'nitrogen': 'நைட்ரஜன் (kg/ha)',
            'phosphorus': 'பாஸ்பரஸ் (kg/ha)',
            'potassium': 'பொட்டாசியம் (kg/ha)',
            'environmental_factors': 'சுற்றுச்சூழல் காரணிகள்',
            'temperature': 'வெப்பநிலை (°C)',
            'rainfall': 'ஆண்டு மழை (mm)',
            'humidity': 'ஈரப்பதம் (%)',
            'analyze_button': 'பகுப்பாய்வு செய்து பரிந்துரைக்கவும்',
            'dashboard': 'டாஷ்போர்டு',
            'crop_recommendation': 'பயிர் பரிந்துரை',
            'soil_analysis': 'மண் பகுப்பாய்வு',
            'weather_forecast': 'வானிலை முன்னறிவிப்பு',
            'farm_overview': 'விவசாய நிலை மேலோட்டம்',
            'soil_nutrient_levels': 'மண் ஊட்டச்சத்து அளவுகள்',
            'recommended_crop': 'பரிந்துரைக்கப்பட்ட பயிர்',
            'expected_yield': 'எதிர்பார்க்கப்படும் விளைச்சல்',
            'success_probability': 'வெற்றி நிகழ்தகவு',
            'why_this_crop': 'இந்த பயிர் ஏன்?',
            'planting_guide': 'நடவு வழிகாட்டி',
            'best_planting_time': 'சிறந்த நடவு நேரம்',
            'water_requirements': 'நீர் தேவைகள்',
            'fertilizer_recommendations': 'உர பரிந்துரைகள்',
            'harvest_timeline': 'அறுவடை காலக்கெடு',
            'market_insights': 'சந்தை நுண்ணறிவுகள்',
            'current_market_price': 'தற்போதைய சந்தை விலை',
            'demand_trend': 'தேவைப் போக்கு',
            'click_to_analyze': 'பயிர் பரிந்துரைகளைப் பெற பொத்தானைக் கிளிக் செய்யவும்',
            'ph_level': 'pH அளவு',
            'moisture': 'ஈரப்பதம்',
            'organic_matter': 'கரிமப் பொருள்',
            'wind_speed': 'காற்றின் வேகம்',
            'created_by': 'அன்போடு உருவாக்கப்பட்டது',
            'team_name': 'டீம் அக்ரோநோவா',
            'for_sih': 'SIH 2025க்காக',
            'language': 'மொழி',
            'select_language': 'மொழியைத் தேர்ந்தெடுக்கவும்',
            'not_specified': 'குறிப்பிடப்படவில்லை',
            'regional_preference': 'பிராந்திய விருப்பம்',
            'soil_type_match': 'மண் வகை பொருத்தம்',
            'ph_suitability': 'pH பொருத்தம்',
            'temperature_suitability': 'வெப்பநிலை பொருத்தம்',
            'rainfall_suitability': 'மழை பொருத்தம்',
            'nutrient_suitability': 'ஊட்டச்சத்து பொருத்தம்',
            'alternative_options': 'மாற்று விருப்பங்கள்',
            'detailed_factor_analysis': 'விரிவான காரணி பகுப்பாய்வு',
            'suitability_analysis': 'க்கான பொருத்தம் பகுப்பாய்வு',
            'analysis_loading': 'உங்கள் பண்ணை தரவை பகுப்பாய்வு செய்து பரிந்துரைகளை உருவாக்குகிறோம்...'
        },
        'crops': {
            'Wheat': 'கோதுமை',
            'Rice': 'நெல்',
            'Maize': 'சோளம்',
            'Cotton': 'பருத்தி',
            'Soybean': 'சோயா',
            'Pulses': 'பருப்பு வகைகள்',
            'Sugarcane': 'கரும்பு',
            'Groundnut': 'நிலக்கடலை'
        },
        'reasons': {
            'highly_suitable': '{} பிராந்தியத்திற்கு மிகவும் பொருத்தமானது',
            'not_typical': '{} இல் பொதுவாக பயிரிடப்படுவதில்லை',
            'ideal_soil': '{} மண்ணுக்கு ஏற்றது',
            'not_optimal_soil': '{} மண்ணுக்கு உகந்ததல்ல (விரும்புகிறது {})',
            'optimal_ph': 'உகந்த pH வரம்பு ({}-{})',
            'ph_low': 'pH சற்று குறைவு (உகந்த: {}-{})',
            'ph_high': 'pH சற்று அதிகம் (உகந்த: {}-{})',
            'optimal_temp': 'உகந்த வெப்பநிலை வரம்பு ({}-{}°C)',
            'temp_low': 'வெப்பநிலை சற்று குறைவு (உகந்த: {}-{}°C)',
            'temp_high': 'வெப்பநிலை சற்று அதிகம் (உகந்த: {}-{}°C)',
            'optimal_rain': 'உகந்த மழை ({}-{}mm)',
            'rain_low': 'மழை சற்று குறைவு (உகந்த: {}-{}mm)',
            'rain_high': 'மழை சற்று அதிகம் (உகந்த: {}-{}mm)',
            'nitrogen_issue': '{} க்கு நைட்ரஜன் அளவு உகந்ததல்ல',
            'phosphorus_issue': '{} க்கு பாஸ்பரஸ் அளவு உகந்ததல்ல',
            'potassium_issue': '{} க்கு பொட்டாசியம் அளவு உகந்ததல்ல'
        }
    },
    'bn': {
        'name': 'বাংলা',
        'direction': 'ltr',
        'states': {
            'Punjab': 'পঞ্জাব',
            'Haryana': 'হরিয়ানা',
            'Uttar Pradesh': 'উত্তর প্রদেশ',
            'Maharashtra': 'মহারাষ্ট্র',
            'Karnataka': 'কর্ণাটক',
            'Tamil Nadu': 'তামিলনাড়ু',
            'Andhra Pradesh': 'অন্ধ্র প্রদেশ',
            'Gujarat': 'গুজরাট',
            'Odisha': 'ওড়িশা',
            'Jharkhand': 'ঝাড়খণ্ড',
            'West Bengal': 'পশ্চিমবঙ্গ',
            'Bihar': 'বিহার',
            'Select': 'অঞ্চল নির্বাচন করুন'
        },
        'ui': {
            'app_name': 'VARUN AI',
            'tagline': 'উন্নত আধুনিক রূপান্তরের জন্য সেরা নির্দেশিকা',
            'farmer_details': 'কৃষকের বিবরণ',
            'full_name': 'পুরো নাম',
            'region': 'অঞ্চল',
            'farm_size': 'খামারের আকার (একর)',
            'soil_properties': 'মাটির বৈশিষ্ট্য',
            'soil_type': 'মাটির ধরন',
            'soil_ph': 'মাটির pH',
            'soil_moisture': 'মাটির আর্দ্রতা (%)',
            'nitrogen': 'নাইট্রোজেন (kg/ha)',
            'phosphorus': 'ফসফরাস (kg/ha)',
            'potassium': 'পটাসিয়াম (kg/ha)',
            'environmental_factors': 'পরিবেশগত কারণ',
            'temperature': 'তাপমাত্রা (°C)',
            'rainfall': 'বার্ষিক বৃষ্টিপাত (mm)',
            'humidity': 'আর্দ্রতা (%)',
            'analyze_button': 'বিশ্লেষণ করুন এবং সুপারিশ করুন',
            'dashboard': 'ড্যাশবোর্ড',
            'crop_recommendation': 'ফসল সুপারিশ',
            'soil_analysis': 'মাটির বিশ্লেষণ',
            'weather_forecast': 'আবহাওয়ার পূর্বাভাস',
            'farm_overview': 'খামারের ওভারভিউ',
            'soil_nutrient_levels': 'মাটির পুষ্টির মাত্রা',
            'recommended_crop': 'সুপারিশকৃত ফসল',
            'expected_yield': 'প্রত্যাশিত ফলন',
            'success_probability': 'সাফল্যের সম্ভাবনা',
            'why_this_crop': 'এই ফসল কেন?',
            'planting_guide': 'রোপণ গাইড',
            'best_planting_time': 'সেরা রোপণের সময়',
            'water_requirements': 'পানির প্রয়োজনীয়তা',
            'fertilizer_recommendations': 'সার সুপারিশ',
            'harvest_timeline': 'ফসল কাটার সময়সীমা',
            'market_insights': 'বাজার অন্তর্দৃষ্টি',
            'current_market_price': 'বর্তমান বাজার মূল্য',
            'demand_trend': 'চাহিদার প্রবণতা',
            'click_to_analyze': 'ফসলের সুপারিশ পেতে বাটন ক্লিক করুন',
            'ph_level': 'pH মাত্রা',
            'moisture': 'আর্দ্রতা',
            'organic_matter': 'জৈব পদার্থ',
            'wind_speed': 'বাতাসের গতি',
            'created_by': 'ভালোবাসা সহ তৈরি',
            'team_name': 'টিম এগ্রোনোভা',
            'for_sih': 'SIH 2025 এর জন্য',
            'language': 'ভাষা',
            'select_language': 'ভাষা নির্বাচন করুন',
            'not_specified': 'নির্দিষ্ট করা হয়নি',
            'regional_preference': 'আঞ্চলিক পছন্দ',
            'soil_type_match': 'মাটির ধরন মিল',
            'ph_suitability': 'pH উপযুক্ততা',
            'temperature_suitability': 'তাপমাত্রা উপযুক্ততা',
            'rainfall_suitability': 'বৃষ্টিপাত উপযুক্ততা',
            'nutrient_suitability': 'পুষ্টি উপযুক্ততা',
            'alternative_options': 'বিকল্প বিকল্প',
            'detailed_factor_analysis': 'বিস্তারিত ফ্যাক্টর বিশ্লেষণ',
            'suitability_analysis': 'এর জন্য উপযুক্ততা বিশ্লেষণ',
            'analysis_loading': 'আপনার খামারের ডেটা বিশ্লেষণ এবং সুপারিশ তৈরি করা হচ্ছে...'
        },
        'crops': {
            'Wheat': 'গম',
            'Rice': 'ধান',
            'Maize': 'ভুট্টা',
            'Cotton': 'তুলা',
            'Soybean': 'সয়াবিন',
            'Pulses': 'ডাল',
            'Sugarcane': 'আখ',
            'Groundnut': 'চিনাবাদাম'
        },
        'reasons': {
            'highly_suitable': '{} অঞ্চলের জন্য অত্যন্ত উপযুক্ত',
            'not_typical': '{} এ সাধারণত চাষ করা হয় না',
            'ideal_soil': '{} মাটির জন্য আদর্শ',
            'not_optimal_soil': '{} মাটির জন্য সর্বোত্তম নয় (পছন্দ করে {})',
            'optimal_ph': 'সর্বোত্তম pH পরিসীমা ({}-{})',
            'ph_low': 'pH কিছুটা কম (আদর্শ: {}-{})',
            'ph_high': 'pH কিছুটা বেশি (আদর্শ: {}-{})',
            'optimal_temp': 'সর্বোত্তম তাপমাত্রা পরিসীমা ({}-{}°C)',
            'temp_low': 'তাপমাত্রা কিছুটা কম (আদর্শ: {}-{}°C)',
            'temp_high': 'তাপমাত্রা কিছুটা বেশি (আদর্শ: {}-{}°C)',
            'optimal_rain': 'সর্বোত্তম বৃষ্টিপাত ({}-{}mm)',
            'rain_low': 'বৃষ্টিপাত কিছুটা কম (আদর্শ: {}-{}mm)',
            'rain_high': 'বৃষ্টিপাত কিছুটা বেশি (আদর্শ: {}-{}mm)',
            'nitrogen_issue': '{} এর জন্য নাইট্রোজেন স্তর সর্বোত্তম নয়',
            'phosphorus_issue': '{} এর জন্য ফসফরাস স্তর সর্বোত্তম নয়',
            'potassium_issue': '{} এর জন্য পটাসিয়াম স্তর সর্বোত্তম নয়'
        }
    },
    'mr': {
        'name': 'मराठी',
        'direction': 'ltr',
        'states': {
            'Punjab': 'पंजाब',
            'Haryana': 'हरियाणा',
            'Uttar Pradesh': 'उत्तर प्रदेश',
            'Maharashtra': 'महाराष्ट्र',
            'Karnataka': 'कर्नाटक',
            'Tamil Nadu': 'तमिळनाडू',
            'Andhra Pradesh': 'आंध्र प्रदेश',
            'Gujarat': 'गुजरात',
            'Odisha': 'ओडिशा',
            'Jharkhand': 'झारखंड',
            'West Bengal': 'पश्चिम बंगाल',
            'Bihar': 'बिहार',
            'Select': 'प्रदेश निवडा'
        },
        'ui': {
            'app_name': 'VARUN AI',
            'tagline': 'विकसित आधुनिक रूपांतरणासाठी उत्तम मार्गदर्शन',
            'farmer_details': 'शेतकरी तपशील',
            'full_name': 'पूर्ण नाव',
            'region': 'प्रदेश',
            'farm_size': 'शेताचा आकार (एकर)',
            'soil_properties': 'मातीचे गुणधर्म',
            'soil_type': 'मातीचा प्रकार',
            'soil_ph': 'मातीचा pH',
            'soil_moisture': 'मातीची आर्द्रता (%)',
            'nitrogen': 'नायट्रोजन (kg/ha)',
            'phosphorus': 'फॉस्फरस (kg/ha)',
            'potassium': 'पोटॅशियम (kg/ha)',
            'environmental_factors': 'पर्यावरणीय घटक',
            'temperature': 'तापमान (°C)',
            'rainfall': 'वार्षिक पाऊस (mm)',
            'humidity': 'आर्द्रता (%)',
            'analyze_button': 'विश्लेषण करा आणि शिफारस करा',
            'dashboard': 'डॅशबोर्ड',
            'crop_recommendation': 'पीक शिफारस',
            'soil_analysis': 'माती विश्लेषण',
            'weather_forecast': 'हवामान अंदाज',
            'farm_overview': 'शेताचा आढावा',
            'soil_nutrient_levels': 'मातीतील पोषक द्रव्य पातळी',
            'recommended_crop': 'शिफारस केलेली पीक',
            'expected_yield': 'अपेक्षित उत्पादन',
            'success_probability': 'यशाची शक्यता',
            'why_this_crop': 'हे पीक का?',
            'planting_guide': 'लागवड मार्गदर्शक',
            'best_planting_time': 'उत्तम लागवडीची वेळ',
            'water_requirements': 'पाण्याची आवश्यकता',
            'fertilizer_recommendations': 'खत शिफारसी',
            'harvest_timeline': 'कापणी वेळरेषा',
            'market_insights': 'बाजारातील अंतर्दृष्टी',
            'current_market_price': 'सध्याचा बाजारभाव',
            'demand_trend': 'मागणीची प्रवृत्ती',
            'click_to_analyze': 'पीक शिफारसी मिळविण्यासाठी बटण क्लिक करा',
            'ph_level': 'pH पातळी',
            'moisture': 'आर्द्रता',
            'organic_matter': 'सेंद्रिय पदार्थ',
            'wind_speed': 'वाऱ्याची गती',
            'created_by': 'प्रेमाने तयार केले',
            'team_name': 'टीम अॅग्रोनोव्हा',
            'for_sih': 'SIH 2025 साठी',
            'language': 'भाषा',
            'select_language': 'भाषा निवडा',
            'not_specified': 'निर्दिष्ट नाही',
            'regional_preference': 'प्रादेशिक प्राधान्य',
            'soil_type_match': 'माती प्रकार जुळणी',
            'ph_suitability': 'pH योग्यता',
            'temperature_suitability': 'तापमान योग्यता',
            'rainfall_suitability': 'पाऊस योग्यता',
            'nutrient_suitability': 'पोषक योग्यता',
            'alternative_options': 'पर्यायी पर्याय',
            'detailed_factor_analysis': 'तपशीलवार घटक विश्लेषण',
            'suitability_analysis': 'साठी योग्यता विश्लेषण',
            'analysis_loading': 'आपला शेत डेटा विश्लेषण आणि शिफारसी तयार केल्या जात आहेत...'
        },
        'crops': {
            'Wheat': 'गहू',
            'Rice': 'तांदूळ',
            'Maize': 'मका',
            'Cotton': 'कापूस',
            'Soybean': 'सोयाबीन',
            'Pulses': 'डाळ',
            'Sugarcane': 'ऊस',
            'Groundnut': 'भुईमूग'
        },
        'reasons': {
            'highly_suitable': '{} प्रदेशासाठी अत्यंत योग्य',
            'not_typical': '{} मध्ये सामान्यतः लावली जात नाही',
            'ideal_soil': '{} मातीसाठी आदर्श',
            'not_optimal_soil': '{} मातीसाठी इष्टतम नाही (प्राधान्य {})',
            'optimal_ph': 'इष्टतम pH श्रेणी ({}-{})',
            'ph_low': 'pH किंचित कमी (आदर्श: {}-{})',
            'ph_high': 'pH किंचित जास्त (आदर्श: {}-{})',
            'optimal_temp': 'इष्टतम तापमान श्रेणी ({}-{}°C)',
            'temp_low': 'तापमान किंचित कमी (आदर्श: {}-{}°C)',
            'temp_high': 'तापमान किंचित जास्त (आदर्श: {}-{}°C)',
            'optimal_rain': 'इष्टतम पाऊस ({}-{}mm)',
            'rain_low': 'पाऊस किंचित कमी (आदर्श: {}-{}mm)',
            'rain_high': 'पाऊस किंचित जास्त (आदर्श: {}-{}mm)',
            'nitrogen_issue': '{} साठी नायट्रोजन पातळी इष्टतम नाही',
            'phosphorus_issue': '{} साठी फॉस्फरस पातळी इष्टतम नाही',
            'potassium_issue': '{} साठी पोटॅशियम पातळी इष्टतम नाही'
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
    'West Bengal': 'bn',
    'Maharashtra': 'mr',
    'Tamil Nadu': 'ta',
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

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'last_state' not in st.session_state:
    st.session_state.last_state = ''

# ===== ENHANCED CSS STYLING =====
st.markdown("""
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
        font-size: 3.5rem;
        color: var(--primary-color);
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .tagline {
        font-size: 1.2rem;
        color: var(--secondary-color);
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
        font-style: italic;
    }

    .sub-header {
        font-size: 1.8rem;
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

    .analysis-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border: 1px solid var(--border-color);
    }

    .factor-score {
        font-size: 0.9rem;
        color: var(--primary-color);
        font-weight: bold;
        margin: 0.3rem 0;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .card {
            padding: 1rem;
        }
        
        .language-selector {
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.3rem 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

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
            draw.text((120, 70), "VARUN", fill=(255, 255, 255))
            draw.text((130, 120), "ai", fill=(255, 215, 0))
            
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
    try:
        st.image("assets/logo.png", width=280)
    except:
        st.warning("Logo image not found")
    
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
    
    # Get soil types in current language
    soil_options = ["Select", "Loam", "Clay", "Sandy", "Silt"]
    soil_display_names = [t('ui.select') if opt == "Select" else opt for opt in soil_options]
    
    selected_soil_index = st.selectbox(
        t('ui.soil_type'),
        range(len(soil_options)),
        format_func=lambda i: soil_display_names[i]
    )
    
    soil_type = soil_options[selected_soil_index]
    
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
            analysis['reasons'].append(t('reasons.highly_suitable').format(region))
        elif region != "Select":
            analysis['reasons'].append(t('reasons.not_typical').format(region))
        
        # Soil type match
        if soil_type != "Select" and crop['soil_type'].lower() == soil_type.lower():
            analysis['score'] += 25
            analysis['details']['soil_type'] = 25
            analysis['reasons'].append(t('reasons.ideal_soil').format(soil_type))
        elif soil_type != "Select":
            analysis['reasons'].append(t('reasons.not_optimal_soil').format(soil_type, crop['soil_type']))
        
        # pH suitability
        if crop['ph_min'] <= ph <= crop['ph_max']:
            ph_score = 15
            analysis['reasons'].append(t('reasons.optimal_ph').format(crop['ph_min'], crop['ph_max']))
        else:
            # Calculate penalty based on deviation from optimal range
            if ph < crop['ph_min']:
                deviation = crop['ph_min'] - ph
                ph_score = max(0, 15 - (deviation * 5))
                analysis['reasons'].append(t('reasons.ph_low').format(crop['ph_min'], crop['ph_max']))
            else:
                deviation = ph - crop['ph_max']
                ph_score = max(0, 15 - (deviation * 5))
                analysis['reasons'].append(t('reasons.ph_high').format(crop['ph_min'], crop['ph_max']))
        
        analysis['score'] += ph_score
        analysis['details']['ph_suitability'] = ph_score
        
        # Temperature suitability
        if crop['temp_min'] <= temperature <= crop['temp_max']:
            temp_score = 10
            analysis['reasons'].append(t('reasons.optimal_temp').format(crop['temp_min'], crop['temp_max']))
        else:
            # Calculate penalty based on deviation from optimal range
            if temperature < crop['temp_min']:
                deviation = crop['temp_min'] - temperature
                temp_score = max(0, 10 - (deviation * 0.5))
                analysis['reasons'].append(t('reasons.temp_low').format(crop['temp_min'], crop['temp_max']))
            else:
                deviation = temperature - crop['temp_max']
                temp_score = max(0, 10 - (deviation * 0.5))
                analysis['reasons'].append(t('reasons.temp_high').format(crop['temp_min'], crop['temp_max']))
        
        analysis['score'] += temp_score
        analysis['details']['temperature_suitability'] = temp_score
        
        # Rainfall suitability
        if crop['rainfall_min'] <= rainfall <= crop['rainfall_max']:
            rain_score = 10
            analysis['reasons'].append(t('reasons.optimal_rain').format(crop['rainfall_min'], crop['rainfall_max']))
        else:
            # Calculate penalty based on deviation from optimal range
            if rainfall < crop['rainfall_min']:
                deviation = crop['rainfall_min'] - rainfall
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
            st.markdown(f"### 🌱 Top Recommendation: {top_recommendation['crop']}")
            st.markdown(f"Expected Yield: {top_recommendation['yield']} tons/acre")
            st.markdown(f"Success Probability: {top_recommendation['probability']}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display suitability chart
            st.plotly_chart(create_suitability_chart(top_recommendation['details'], top_recommendation['crop']), 
                           use_container_width=True)
            
            # Display detailed factor analysis
            display_factor_analysis(top_recommendation['details'])
            
            # Display reasons
            st.markdown("#### Why this crop?")
            for reason in top_recommendation['reasons']:
                st.info(f"• {reason}")
            
            # Display crop details
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Best Planting Time")
                st.write(top_recommendation['planting_time'])
                st.markdown("Water Requirements")
                st.write(top_recommendation['water_req'])
            with col2:
                st.markdown("Fertilizer Recommendations")
                st.write(top_recommendation['fertilizer'])
                st.markdown("Harvest Timeline")
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
    <p>Created with ❤ by <span class="team-name">Team AgroNova</span> for SIH 2025</p>
    <p>VARUN AI - Vikasit Adhunik Roopantaran ke liye Uttam Nirdesh</p>
</div>
""", unsafe_allow_html=True)
