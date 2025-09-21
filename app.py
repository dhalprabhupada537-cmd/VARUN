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

# Language data - All integrated in one file
LANGUAGES = {
    'en': {
        'name': 'English',
        'ui': {
            'tagline': 'Modern Transformation for Optimal Guidance',
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
            'click_to_analyze': 'Click the Analyze & Recommend button to get crop recommendations',
            'ph_level': 'pH Level',
            'moisture': 'Moisture',
            'organic_matter': 'Organic Matter',
            'wind_speed': 'Wind Speed',
            'created_by': 'Created with ❤️ by',
            'team_name': 'Team AgroNova',
            'for_sih': 'for SIH 2025'
        },
        'states': {
            "Punjab": "Punjab",
            "Haryana": "Haryana",
            "Uttar Pradesh": "Uttar Pradesh",
            "Maharashtra": "Maharashtra",
            "Karnataka": "Karnataka",
            "Tamil Nadu": "Tamil Nadu",
            "Andhra Pradesh": "Andhra Pradesh",
            "Gujarat": "Gujarat",
            "Odisha": "Odisha",
            "Jharkhand": "Jharkhand",
            "West Bengal": "West Bengal",
            "Bihar": "Bihar"
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
        'ui': {
            'tagline': 'आधुनिक रूपांतरण के लिए उत्तम निर्देश',
            'farmer_details': 'किसान का विवरण',
            'full_name': 'पूरा नाम',
            'region': 'क्षेत्र',
            'farm_size': 'खेत का आकार (एकड़)',
            'soil_properties': 'मिट्टी के गुण',
            'soil_type': 'मिट्टी का प्रकार',
            'soil_ph': 'मिट्टी का पीएच',
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
            'recommended_crop': 'सुझाई गई फसल',
            'expected_yield': 'अनुमानित उपज',
            'success_probability': 'सफलता की संभावना',
            'why_this_crop': 'यह फसल क्यों?',
            'planting_guide': 'रोपण मार्गदर्शिका',
            'best_planting_time': 'सर्वोत्तम रोपण समय',
            'water_requirements': 'पानी की आवश्यकता',
            'fertilizer_recommendations': 'उर्वरक सिफारिशें',
            'harvest_timeline': 'फसल कटाई का समय',
            'market_insights': 'बाजार की जानकारी',
            'current_market_price': 'वर्तमान बाजार मूल्य',
            'demand_trend': 'मांग की प्रवृत्ति',
            'click_to_analyze': 'फसल सिफारिशें प्राप्त करने के लिए विश्लेषण बटन पर क्लिक करें',
            'ph_level': 'पीएच स्तर',
            'moisture': 'नमी',
            'organic_matter': 'कार्बनिक पदार्थ',
            'wind_speed': 'हवा की गति',
            'created_by': '❤️ से बनाया गया',
            'team_name': 'टीम एग्रोनोवा',
            'for_sih': 'एसआईएच 2025 के लिए'
        },
        'states': {
            "Punjab": "पंजाब",
            "Haryana": "हरियाणा",
            "Uttar Pradesh": "उत्तर प्रदेश",
            "Maharashtra": "महाराष्ट्र",
            "Karnataka": "कर्नाटक",
            "Tamil Nadu": "तमिल नाडु",
            "Andhra Pradesh": "आंध्र प्रदेश",
            "Gujarat": "गुजरात",
            "Odisha": "ओडिशा",
            "Jharkhand": "झारखंड",
            "West Bengal": "पश्चिम बंगाल",
            "Bihar": "बिहार"
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
    'te': {
        'name': 'తెలుగు',
        'ui': {
            'tagline': 'ఆధునిక రూపాంతరం కోసం ఉత్తమ మార్గదర్శకత్వం',
            'farmer_details': 'రైతు వివరాలు',
            'full_name': 'పూర్తి పేరు',
            'region': 'ప్రాంతం',
            'farm_size': 'వ్యవసాయ భూమి పరిమాణం (ఎకరాలు)',
            'soil_properties': 'నేల లక్షణాలు',
            'soil_type': 'నేల రకం',
            'soil_ph': 'నేల pH',
            'soil_moisture': 'నేల తేమ (%)',
            'nitrogen': 'నత్రజని (kg/ha)',
            'phosphorus': 'భాస్వరం (kg/ha)',
            'potassium': 'పొటాషియం (kg/ha)',
            'environmental_factors': 'పర్యావరణ కారకాలు',
            'temperature': 'ఉష్ణోగ్రత (°C)',
            'rainfall': 'వార్షిక వర్షపాతం (mm)',
            'humidity': 'ఆర్ద్రత (%)',
            'analyze_button': 'విశ్లేషించు మరియు సిఫార్సు చేయండి',
            'dashboard': 'డాష్బోర్డ్',
            'crop_recommendation': 'పంట సిఫార్సు',
            'soil_analysis': 'నేల విశ్లేషణ',
            'weather_forecast': 'వాతావరణ సూచన',
            'farm_overview': 'వ్యవసాయ భూమి అవలోకనం',
            'recommended_crop': 'సిఫార్సు చేయబడిన పంట',
            'expected_yield': 'అంచనా దిగుబడి',
            'success_probability': 'విజయ సంభావ్యత',
            'why_this_crop': 'ఈ పంట ఎందుకు?',
            'planting_guide': 'నాటడం గైడ్',
            'best_planting_time': 'ఉత్తమ నాటే సమయం',
            'water_requirements': 'నీటి అవసరాలు',
            'fertilizer_recommendations': 'ఎరువు సిఫార్సులు',
            'harvest_timeline': 'పంట కోత సమయం',
            'market_insights': 'మార్కెట్ అంతర్దృష్టులు',
            'current_market_price': 'ప్రస్తుత మార్కెట్ ధర',
            'demand_trend': 'డిమాండ్ ట్రెండ్',
            'click_to_analyze': 'పంట సిఫార్సులను పొందడానికి విశ్లేషించు బటన్ పై క్లిక్ చేయండి',
            'ph_level': 'pH స్థాయి',
            'moisture': 'తేమ',
            'organic_matter': 'సేంద్రీయ పదార్థం',
            'wind_speed': 'గాలి వేగం',
            'created_by': '❤️ తో సృష్టించబడింది',
            'team_name': 'టీమ్ అగ్రోనోవా',
            'for_sih': 'SIH 2025 కోసం'
        },
        'states': {
            "Punjab": "పంజాబ్",
            "Haryana": "హర్యానా",
            "Uttar Pradesh": "ఉత్తర ప్రదేశ్",
            "Maharashtra": "మహారాష్ట్ర",
            "Karnataka": "కర్ణాటక",
            "Tamil Nadu": "తమిళనాడు",
            "Andhra Pradesh": "ఆంధ్రప్రదేశ్",
            "Gujarat": "గుజరాత్",
            "Odisha": "ఒడిశా",
            "Jharkhand": "ఝార్ఖండ్",
            "West Bengal": "పశ్చిమ బెంగాల్",
            "Bihar": "బీహార్"
        },
        'crops': {
            'Wheat': 'గోధుమ',
            'Rice': 'వరి',
            'Maize': 'మొక్కజొన్న',
            'Cotton': 'పత్తి',
            'Soybean': 'సోయా',
            'Pulses': 'పప్పులు'
        }
    },
    'bn': {
        'name': 'বাংলা',
        'ui': {
            'tagline': 'আধুনিক রূপান্তরের জন্য সর্বোত্তম নির্দেশনা',
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
            'recommended_crop': 'সুপারিশকৃত ফসল',
            'expected_yield': 'আনুমানিক ফলন',
            'success_probability': 'সাফল্যের সম্ভাবনা',
            'why_this_crop': 'এই ফসল কেন?',
            'planting_guide': 'রোপণ গাইড',
            'best_planting_time': 'সেরা রোপণের সময়',
            'water_requirements': 'পানির প্রয়োজনীয়তা',
            'fertilizer_recommendations': 'সারের সুপারিশ',
            'harvest_timeline': 'ফসল কাটার সময়সূচী',
            'market_insights': 'বাজার অন্তর্দৃষ্টি',
            'current_market_price': 'বর্তমান বাজার মূল্য',
            'demand_trend': 'চাহিদার প্রবণতা',
            'click_to_analyze': 'ফসলের সুপারিশ পেতে বিশ্লেষণ বাটনে ক্লিক করুন',
            'ph_level': 'pH মাত্রা',
            'moisture': 'আর্দ্রতা',
            'organic_matter': 'জৈব পদার্থ',
            'wind_speed': 'বাতাসের গতি',
            'created_by': '❤️ দিয়ে তৈরি',
            'team_name': 'টিম এগ্রোনোভা',
            'for_sih': 'SIH 2025 এর জন্য'
        },
        'states': {
            "Punjab": "পাঞ্জাব",
            "Haryana": "হরিয়ানা",
            "Uttar Pradesh": "উত্তর প্রদেশ",
            "Maharashtra": "মহারাষ্ট্র",
            "Karnataka": "কর্ণাটক",
            "Tamil Nadu": "তামিলনাড়ু",
            "Andhra Pradesh": "অন্ধ্রপ্রদেশ",
            "Gujarat": "গুজরাট",
            "Odisha": "ওড়িশা",
            "Jharkhand": "ঝাড়খণ্ড",
            "West Bengal": "পশ্চিমবঙ্গ",
            "Bihar": "বিহার"
        },
        'crops': {
            'Wheat': 'গম',
            'Rice': 'ধান',
            'Maize': 'ভুট্টা',
            'Cotton': 'তুলা',
            'Soybean': 'সয়াবিন',
            'Pulses': 'ডাল'
        }
    },
    'or': {
        'name': 'ଓଡିଆ',
        'ui': {
            'tagline': 'ଆଧୁନିକ ରୂପାନ୍ତରଣ ପାଇଁ ଉତ୍ତମ ନିର୍ଦେଶନା',
            'farmer_details': 'କୃଷକର ବିବରଣୀ',
            'full_name': 'ପୂରା ନାମ',
            'region': 'ଅଞ୍ଚଳ',
            'farm_size': 'ଚାଷ ଜମିର ଆକାର (ଏକର)',
            'soil_properties': 'ମୃତ୍ତିକାର ଗୁଣ',
            'soil_type': 'ମୃତ୍ତିକାର ପ୍ରକାର',
            'soil_ph': 'ମୃତ୍ତିକା pH',
            'soil_moisture': 'ମୃତ୍ତିକାର ଆର୍ଦ୍ରତା (%)',
            'nitrogen': 'ନାଇଟ୍ରୋଜେନ (kg/ha)',
            'phosphorus': 'ଫସଫରସ (kg/ha)',
            'potassium': 'ପୋଟାସିଅମ (kg/ha)',
            'environmental_factors': 'ପରିବେଶଗତ କାରକ',
            'temperature': 'ତାପମାତ୍ରା (°C)',
            'rainfall': 'ବାର୍ଷିକ ବର୍ଷା (mm)',
            'humidity': 'ଆର୍ଦ୍ରତା (%)',
            'analyze_button': 'ବିଶ୍ଳେଷଣ କରନ୍ତୁ ଏବଂ ସୁପାରିଶ କରନ୍ତୁ',
            'dashboard': 'ଡ୍ୟାସବୋର୍ଡ',
            'crop_recommendation': 'ଫସଲ ସୁପାରିଶ',
            'soil_analysis': 'ମୃତ୍ତିକା ବିଶ୍ଳେଷଣ',
            'weather_forecast': 'ପାଗ ପୂର୍ବାନୁମାନ',
            'farm_overview': 'ଚାଷ ଜମି ସମୀକ୍ଷା',
            'recommended_crop': 'ସୁପାରିଶକୃତ ଫସଲ',
            'expected_yield': 'ଅନୁମାନିତ ଫସଲ',
            'success_probability': 'ସଫଳତାର ସମ୍ଭାବନା',
            'why_this_crop': 'ଏହି ଫସଲ କାହିଁକି?',
            'planting_guide': 'ରୋପଣ ଗାଇଡ୍',
            'best_planting_time': 'ସର୍ବୋତ୍ତମ ରୋପଣ ସମୟ',
            'water_requirements': 'ଜଳ ଆବଶ୍ୟକତା',
            'fertilizer_recommendations': 'ସାର ପ୍ରୟୋଗ ସୁପାରିଶ',
            'harvest_timeline': 'ଫସଲ କଟାଇ ସମୟ',
            'market_insights': 'ବଜାରର ଅନ୍ତର୍ଦୃଷ୍ଟି',
            'current_market_price': 'ବର୍ତ୍ତମାନର ବଜାର ମୂଲ୍ୟ',
            'demand_trend': 'ଚାହିଦାର ପ୍ରବୃତ୍ତି',
            'click_to_analyze': 'ଫସଲ ସୁପାରିଶ ପାଇବା ପାଇଁ ବିଶ୍ଳେଷଣ ବଟନ୍ ଦବାନ୍ତୁ',
            'ph_level': 'pH ସ୍ତର',
            'moisture': 'ଆର୍ଦ୍ରତା',
            'organic_matter': 'ଜୈବିକ ପଦାର୍ଥ',
            'wind_speed': 'ପବନ ଗତି',
            'created_by': '❤️ ସହିତ ସୃଷ୍ଟି',
            'team_name': 'ଦଳ ଆଗ୍ରୋନୋଭା',
            'for_sih': 'SIH 2025 ପାଇଁ'
        },
        'states': {
            "Punjab": "ପଞ୍ଜାବ",
            "Haryana": "ହରିୟାଣା",
            "Uttar Pradesh": "ଉତ୍ତର ପ୍ରଦେଶ",
            "Maharashtra": "ମହାରାଷ୍ଟ୍ର",
            "Karnataka": "କର୍ଣାଟକ",
            "Tamil Nadu": "ତାମିଲନାଡୁ",
            "Andhra Pradesh": "ଆନ୍ଧ୍ର ପ୍ରଦେଶ",
            "Gujarat": "ଗୁଜରାଟ",
            "Odisha": "ଓଡିଶା",
            "Jharkhand": "ଝାଡ଼ଖଣ୍ଡ",
            "West Bengal": "ପଶ୍ଚିମ ବଙ୍ଗ",
            "Bihar": "ବିହାର"
        },
        'crops': {
            'Wheat': 'ଗହମ',
            'Rice': 'ଧାନ',
            'Maize': 'ମକା',
            'Cotton': 'କପାହ',
            'Soybean': 'ସୋୟାବିନ',
            'Pulses': 'ଡାଲି'
        }
    }
}

# Helper functions for language support
def get_available_languages():
    return list(LANGUAGES.keys())

def get_state_name(state_code, lang='en'):
    return LANGUAGES[lang]['states'].get(state_code, state_code)

def get_language_for_state(state_code):
    # Map states to their primary languages
    state_language_map = {
        "Punjab": "en",
        "Haryana": "hi",
        "Uttar Pradesh": "hi",
        "Maharashtra": "en",
        "Karnataka": "en",
        "Tamil Nadu": "en",
        "Andhra Pradesh": "te",
        "Gujarat": "en",
        "Odisha": "or",
        "Jharkhand": "hi",
        "West Bengal": "bn",
        "Bihar": "hi"
    }
    return state_language_map.get(state_code, "en")

# Enhanced CSS with better colors and design
def get_css():
    return """
    <style>
        /* Main styles */
        .main-header {
            font-size: 3.5rem;
            color: #1B5E20;
            text-align: center;
            font-weight: bold;
            margin-bottom: 0;
            font-family: 'Arial', sans-serif;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }
        .tagline {
            font-size: 1.2rem;
            color: #388E3C;
            text-align: center;
            margin-top: 0;
            font-style: italic;
            font-family: 'Arial', sans-serif;
        }
        .sub-header {
            font-size: 1.8rem;
            color: #2E7D32;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
            font-family: 'Arial', sans-serif;
        }
        
        /* Card styles */
        .card {
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
            margin: 15px 0;
            background-color: #FFFFFF;
            border-left: 5px solid #4CAF50;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px 0 rgba(0,0,0,0.15);
        }
        .recommendation-card {
            background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #4CAF50;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }
        
        /* Metric styles */
        .metric-label {
            font-size: 14px;
            color: #616161;
            font-weight: 500;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 24px;
            color: #1B5E20;
            font-weight: bold;
        }
        
        /* Weather card styles */
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
        
        /* Soil image styles */
        .soil-image {
            border-radius: 12px;
            width: 100%;
            height: 180px;
            object-fit: cover;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Footer styles */
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background-color: #2E7D32;
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .team-name {
            font-weight: bold;
            color: #FFD700;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
            border-radius: 4px;
        }
        
        /* Button styles */
        .stButton button {
            background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .stButton button:hover {
            background: linear-gradient(135deg, #43A047 0%, #1B5E20 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Language selector */
        .language-selector {
            background-color: #E8F5E9;
            padding: 8px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #F1F8E9;
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
            color: white;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(135deg, #F1F8E9 0%, #E8F5E9 100%);
        }
    </style>
    """

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

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'last_state' not in st.session_state:
    st.session_state.last_state = ''

# Apply custom CSS
st.markdown(get_css(), unsafe_allow_html=True)

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
