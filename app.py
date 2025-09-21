import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime, timedelta
import os
import json
import gtts
from googletrans import Translator
import speech_recognition as sr
import requests
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="VARUN AI Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced VARUN branding
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2E8B57;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
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
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    .recommendation-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
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
        margin: 10px 0;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        background-color: #2E8B57;
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .factor-score {
        font-size: 14px;
        color: #2E8B57;
        font-weight: bold;
    }
    .language-selector {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    .voice-btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        margin: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .voice-btn:hover {
        background-color: #3e8e41;
    }
</style>
""", unsafe_allow_html=True)

# Language support
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Odia": "or",
    "Telugu": "te",
    "Bengali": "bn"
}

# Translations
TRANSLATIONS = {
    "main_title": {
        "English": "VARUN AI Crop Recommendation",
        "Hindi": "वरुण एआई फसल सिफारिश",
        "Odia": "ଭରୁଣ ଏଆଇ ଫସଲ ପରାମର୍ଶ",
        "Telugu": "వరుణ్ AI పంట సిఫార్సు",
        "Bengali": "বরুণ এআই ফসল সুপারিশ"
    },
    "tagline": {
        "English": "Advanced Modern Transformation for Optimal Guidance",
        "Hindi": "इष्टतम मार्गदर्शन के लिए उन्नत आधुनिक परिवर्तन",
        "Odia": "ସର୍ବୋତ୍ତମ ମାର୍ଗଦର୍ଶନ ପାଇଁ ଉନ୍ନତ ଆଧୁନିକ ପରିବର୍ତ୍ତନ",
        "Telugu": "ఆప్టిమల్ మార్గదర్శకత్వం కోసం అధునాతన ఆధునిక పరివర్తన",
        "Bengali": "সর্বোত্তম নির্দেশনার জন্য উন্নত আধুনিক রূপান্তর"
    },
    "farmer_details": {
        "English": "Farmer Details",
        "Hindi": "किसान का विवरण",
        "Odia": "କୃଷକର ବିବରଣୀ",
        "Telugu": "రైతు వివరాలు",
        "Bengali": "কৃষকের বিবরণ"
    },
    "full_name": {
        "English": "Full Name",
        "Hindi": "पूरा नाम",
        "Odia": "ପୂରା ନାମ",
        "Telugu": "పూర్తి పేరు",
        "Bengali": "পুরো নাম"
    },
    "region": {
        "English": "Region",
        "Hindi": "क्षेत्र",
        "Odia": "ଅଞ୍ଚଳ",
        "Telugu": "ప్రాంతం",
        "Bengali": "অঞ্চল"
    },
    "farm_size": {
        "English": "Farm Size (acres)",
        "Hindi": "खेत का आकार (एकड़)",
        "Odia": "ଚାଷ ଜମିର ଆକାର (ଏକର)",
        "Telugu": "వ్యవసాయ భూమి పరిమాణం (ఎకరాలు)",
        "Bengali": "খামারের আকার (একর)"
    },
    "soil_properties": {
        "English": "Soil Properties",
        "Hindi": "मिट्टी के गुण",
        "Odia": "ମୃତ୍ତିକାର ଗୁଣ",
        "Telugu": "నేల లక్షణాలు",
        "Bengali": "মাটির বৈশিষ্ট্য"
    },
    "soil_type": {
        "English": "Soil Type",
        "Hindi": "मिट्टी का प्रकार",
        "Odia": "ମୃତ୍ତିକାର ପ୍ରକାର",
        "Telugu": "నేల రకం",
        "Bengali": "মাটির ধরন"
    },
    "soil_ph": {
        "English": "Soil pH",
        "Hindi": "मिट्टी का pH",
        "Odia": "ମୃତ୍ତିକାର pH",
        "Telugu": "నేల pH",
        "Bengali": "মাটির pH"
    },
    "soil_moisture": {
        "English": "Soil Moisture (%)",
        "Hindi": "मिट्टी की नमी (%)",
        "Odia": "ମୃତ୍ତିକାର ଆର୍ଦ୍ରତା (%)",
        "Telugu": "నేల తేమ (%)",
        "Bengali": "মাটির আর্দ্রতা (%)"
    },
    "nitrogen": {
        "English": "Nitrogen (kg/ha)",
        "Hindi": "नाइट्रोजन (kg/ha)",
        "Odia": "ନାଇଟ୍ରୋଜେନ (kg/ha)",
        "Telugu": "నత్రజని (kg/ha)",
        "Bengali": "নাইট্রোজেন (kg/ha)"
    },
    "phosphorus": {
        "English": "Phosphorus (kg/ha)",
        "Hindi": "फॉस्फोरस (kg/ha)",
        "Odia": "ଫସଫରସ (kg/ha)",
        "Telugu": "భాస్వరం (kg/ha)",
        "Bengali": "ফসফরাস (kg/ha)"
    },
    "potassium": {
        "English": "Potassium (kg/ha)",
        "Hindi": "पोटैशियम (kg/ha)",
        "Odia": "ପୋଟାସିଅମ (kg/ha)",
        "Telugu": "పొటాషియం (kg/ha)",
        "Bengali": "পটাশিয়াম (kg/ha)"
    },
    "env_factors": {
        "English": "Environmental Factors",
        "Hindi": "पर्यावरणीय कारक",
        "Odia": "ପରିବେଶଗତ କାରକ",
        "Telugu": "పర్యావరణ కారకాలు",
        "Bengali": "পরিবেশগত কারণ"
    },
    "temperature": {
        "English": "Temperature (°C)",
        "Hindi": "तापमान (°C)",
        "Odia": "ତାପମାତ୍ରା (°C)",
        "Telugu": "ఉష్ణోగ్రత (°C)",
        "Bengali": "তাপমাত্রা (°C)"
    },
    "rainfall": {
        "English": "Annual Rainfall (mm)",
        "Hindi": "वार्षिक वर्षा (mm)",
        "Odia": "ବାର୍ଷିକ ବର୍ଷା (mm)",
        "Telugu": "వార్షిక వర్షపాతం (mm)",
        "Bengali": "বার্ষিক বৃষ্টিপাত (mm)"
    },
    "humidity": {
        "English": "Humidity (%)",
        "Hindi": "आर्द्रता (%)",
        "Odia": "ଆର୍ଦ୍ରତା (%)",
        "Telugu": "ఆర్ద్రత (%)",
        "Bengali": "আর্দ্রতা (%)"
    },
    "analyze_btn": {
        "English": "Analyze & Recommend",
        "Hindi": "विश्लेषण और सिफारिश करें",
        "Odia": "ବିଶ୍ଳେଷଣ ଏବଂ ପରାମର୍ଶ ଦିଅନ୍ତୁ",
        "Telugu": "విశ్లేషించండి మరియు సిఫార్సు చేయండి",
        "Bengali": "বিশ্লেষণ এবং সুপারিশ করুন"
    },
    "farm_overview": {
        "English": "Farm Overview",
        "Hindi": "खेत का अवलोकन",
        "Odia": "ଚାଷ ଜମିର ସମୀକ୍ଷା",
        "Telugu": "వ్యవసాయ భూమి అవలోకనం",
        "Bengali": "খামারের ওভারভিউ"
    },
    "crop_recommendation": {
        "English": "Crop Recommendation",
        "Hindi": "फसल सिफारिश",
        "Odia": "ଫସଲ ପରାମର୍ଶ",
        "Telugu": "పంట సిఫార్సు",
        "Bengali": "ফসল সুপারিশ"
    },
    "soil_analysis": {
        "English": "Soil Analysis",
        "Hindi": "मिट्टी का विश्लेषण",
        "Odia": "ମୃତ୍ତିକା ବିଶ୍ଳେଷଣ",
        "Telugu": "నేల విశ్లేషణ",
        "Bengali": "মাটির বিশ্লেষণ"
    },
    "weather_forecast": {
        "English": "Weather Forecast",
        "Hindi": "मौसम का पूर्वानुमान",
        "Odia": "ପାଗ ପୂର୍ବାନୁମାନ",
        "Telugu": "వాతావరణ పూర్వానుమానం",
        "Bengali": "আবহাওয়ার পূর্বাভাস"
    },
    "top_recommendation": {
        "English": "Top Recommendation",
        "Hindi": "शीर्ष सिफारिश",
        "Odia": "ଶୀର୍ଷ ପରାମର୍ଶ",
        "Telugu": "టాప్ సిఫార్సు",
        "Bengali": "শীর্ষ সুপারিশ"
    },
    "expected_yield": {
        "English": "Expected Yield",
        "Hindi": "अनुमानित उपज",
        "Odia": "ଆଶା କରାଯାଉଥିବା ଫଳାଫଳ",
        "Telugu": "అంచనా దిగుబడి",
        "Bengali": "প্রত্যাশিত ফলন"
    },
    "success_probability": {
        "English": "Success Probability",
        "Hindi": "सफलता की संभावना",
        "Odia": "ସଫଳତାର ସମ୍ଭାବନା",
        "Telugu": "విజయ సంభావ్యత",
        "Bengali": "সাফল্যের সম্ভাবনা"
    },
    "why_this_crop": {
        "English": "Why this crop?",
        "Hindi": "यह फसल क्यों?",
        "Odia": "ଏହି ଫସଲ କାହିଁକି?",
        "Telugu": "ఈ పంట ఎందుకు?",
        "Bengali": "এই ফসল কেন?"
    },
    "best_planting_time": {
        "English": "Best Planting Time",
        "Hindi": "बुवाई का सबसे अच्छा समय",
        "Odia": "ସର୍ବୋତ୍ତମ ରୋପଣ ସମୟ",
        "Telugu": "ఉత్తమ నాటే సమయం",
        "Bengali": "সেরা রোপণের সময়"
    },
    "water_requirements": {
        "English": "Water Requirements",
        "Hindi": "पानी की आवश्यकता",
        "Odia": "ଜଳ ଆବଶ୍ୟକତା",
        "Telugu": "నీటి అవసరాలు",
        "Bengali": "জলের প্রয়োজনীয়তা"
    },
    "fertilizer_recommendations": {
        "English": "Fertilizer Recommendations",
        "Hindi": "उर्वरक सिफारिशें",
        "Odia": "ସାର ପରାମର୍ଶ",
        "Telugu": "ఎరువు సిఫార్సులు",
        "Bengali": "সার সুপারিশ"
    },
    "harvest_timeline": {
        "English": "Harvest Timeline",
        "Hindi": "फसल कटाई का समय",
        "Odia": "ଫସଲ କଟାଣି ସମୟସୀମା",
        "Telugu": "విత్తన సమయరేఖ",
        "Bengali": "ফসল কাটার সময়সীমা"
    },
    "market_insights": {
        "English": "Market Insights",
        "Hindi": "बाजार की जानकारी",
        "Odia": "ବଜାରର ଅନ୍ତର୍ଦୃଷ୍ଟି",
        "Telugu": "మార్కెట్ ఇన్సైట్స్",
        "Bengali": "বাজার অন্তর্দৃষ্টি"
    },
    "current_market_price": {
        "English": "Current market price",
        "Hindi": "वर्तमान बाजार मूल्य",
        "Odia": "ବର୍ତ୍ତମାନର ବଜାର ମୂଲ୍ୟ",
        "Telugu": "ప్రస్తుత మార్కెట్ ధర",
        "Bengali": "বর্তমান বাজার মূল্য"
    },
    "demand_trend": {
        "English": "Demand trend",
        "Hindi": "मांग की प्रवृत्ति",
        "Odia": "ଚାହିଦା ପ୍ରବୃତ୍ତି",
        "Telugu": "డిమాండ్ ట్రెండ్",
        "Bengali": "চাহিদার প্রবণতা"
    },
    "alternative_options": {
        "English": "Alternative Options",
        "Hindi": "वैकल्पिक विकल्प",
        "Odia": "ବିକଳ୍ପ ବିକଳ୍ପ",
        "Telugu": "ప్రత్యామ్నాయ ఎంపికలు",
        "Bengali": "বিকল্প বিকল্প"
    },
    "detailed_factor_analysis": {
        "English": "Detailed Factor Analysis",
        "Hindi": "विस्तृत कारक विश्लेषण",
        "Odia": "ବିସ୍ତୃତ କାରକ ବିଶ୍ଳେଷଣ",
        "Telugu": "వివరణాత్మక కారకం విశ్లేషణ",
        "Bengali": "বিস্তারিত ফ্যাক্টর বিশ্লেষণ"
    },
    "ph_level": {
        "English": "pH Level",
        "Hindi": "pH स्तर",
        "Odia": "pH ସ୍ତର",
        "Telugu": "pH స్థాయి",
        "Bengali": "pH স্তর"
    },
    "moisture": {
        "English": "Moisture",
        "Hindi": "नमी",
        "Odia": "ଆର୍ଦ୍ରତା",
        "Telugu": "తేమ",
        "Bengali": "আর্দ্রতা"
    },
    "organic_matter": {
        "English": "Organic Matter",
        "Hindi": "कार्बनिक पदार्थ",
        "Odia": "ଜୈବିକ ପଦାର୍ଥ",
        "Telugu": "సేంద్రీయ పదార్థం",
        "Bengali": "জৈব পদার্থ"
    },
    "wind_speed": {
        "English": "Wind Speed",
        "Hindi": "हवा की गति",
        "Odia": "ପବନ ଗତି",
        "Telugu": "గాలి వేగం",
        "Bengali": "বাতাসের গতি"
    },
    "click_to_analyze": {
        "English": "Click the 'Analyze & Recommend' button to get crop recommendations",
        "Hindi": "फसल सिफारिशें प्राप्त करने के लिए 'विश्लेषण और सिफारिश करें' बटन पर क्लिक करें",
        "Odia": "ଫସଲ ପରାମର୍ଶ ପାଇବା ପାଇଁ 'ବିଶ୍ଳେଷଣ ଏବଂ ପରାମର୍ଶ ଦିଅନ୍ତୁ' ବଟନ୍ ଦବାନ୍ତୁ",
        "Telugu": "పంట సిఫార్సులను పొందడానికి 'విశ్లేషించండి మరియు సిఫార్సు చేయండి' బటన్పై క్లిక్ చేయండి",
        "Bengali": "ফসলের সুপারিশ পেতে 'বিশ্লেষণ এবং সুপারিশ করুন' বোতামে ক্লিক করুন"
    },
    "analyzing_data": {
        "English": "Analyzing your farm data and generating recommendations...",
        "Hindi": "आपके खेत के डेटा का विश्लेषण और सिफारिशें तैयार की जा रही हैं...",
        "Odia": "ଆପଣଙ୍କ ଚାଷ ଜମିର ତଥ୍ୟ ବିଶ୍ଳେଷଣ ଏବଂ ପରାମର୍ଶ ଉତ୍ପାଦନ କରୁଛି...",
        "Telugu": "మీ వ్యవసాయ భూమి డేటాను విశ్లేషిస్తోంది మరియు సిఫార్సులను రూపొందిస్తోంది...",
        "Bengali": "আপনার খামারের ডেটা বিশ্লেষণ এবং সুপারিশ তৈরি করা হচ্ছে..."
    }
}

# Initialize translator
translator = Translator()

def translate_text(text, dest_lang):
    """Translate text to destination language"""
    try:
        if dest_lang == "en":
            return text
        translation = translator.translate(text, dest=dest_lang)
        return translation.text
    except:
        return text

def get_current_location():
    """Get current location using IP address"""
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data.get('loc', '').split(',')
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        
        if location and len(location) == 2:
            return float(location[0]), float(location[1]), city, region, country
        return None, None, city, region, country
    except:
        return None, None, "Unknown", "Unknown", "Unknown"

def get_weather_data(lat, lon):
    """Get weather data from OpenWeatherMap API"""
    try:
        # This is a placeholder - you would need to sign up for an API key
        api_key = "your_openweathermap_api_key_here"
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        # Simulate rainfall data as it's not directly available in free tier
        rainfall = np.random.uniform(0, 10) if np.random.random() > 0.7 else 0
        
        return temperature, humidity, rainfall
    except:
        # Return random values if API fails
        return np.random.uniform(20, 35), np.random.uniform(40, 80), np.random.uniform(0, 5)

def get_soil_data(lat, lon):
    """Get soil data - this would typically come from a soil database or satellite imagery"""
    # This is a simulation - in a real app, you would use actual soil data APIs
    try:
        # Simulate soil type based on location
        soil_types = ["Loam", "Clay", "Sandy", "Silt"]
        soil_type = np.random.choice(soil_types, p=[0.4, 0.3, 0.2, 0.1])
        
        # Simulate other soil parameters
        soil_ph = round(np.random.uniform(5.5, 7.5), 1)
        soil_moisture = np.random.randint(30, 70)
        nitrogen = np.random.randint(30, 80)
        phosphorus = np.random.randint(20, 60)
        potassium = np.random.randint(40, 90)
        
        return soil_type, soil_ph, soil_moisture, nitrogen, phosphorus, potassium
    except:
        return "Loam", 6.5, 50, 50, 40, 60

def text_to_speech(text, lang_code):
    """Convert text to speech"""
    try:
        tts = gtts.gTTS(text=text, lang=lang_code, slow=False)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        
        # Encode audio to base64 for embedding in HTML
        audio_base64 = base64.b64encode(audio_file.read()).decode()
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        return audio_html
    except:
        return ""

def speech_to_text():
    """Convert speech to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        except:
            return ""

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

# Language selector
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    selected_language = st.selectbox("🌐 Language", list(LANGUAGES.keys()), index=0)

# Get translations for selected language
def t(key):
    return TRANSLATIONS.get(key, {}).get(selected_language, key)

# App header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f'<h1 class="main-header">VARUN<span style="color: #FFD700;">ai</span></h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="tagline">{t("tagline")}</p>', unsafe_allow_html=True)

# Voice assistance button
if st.button("🎤 Voice Assistance", key="voice_btn"):
    st.info("Voice assistance is activated. Please speak your query.")
    query = speech_to_text()
    if query:
        st.success(f"Your query: {query}")
        # Simple voice command processing
        if "analyze" in query.lower() or "recommend" in query.lower():
            analyze_button = True
        elif "weather" in query.lower():
            st.experimental_set_query_params(tab="Weather Forecast")
        elif "soil" in query.lower():
            st.experimental_set_query_params(tab="Soil Analysis")
        else:
            response = "I can help you with crop recommendations, weather information, and soil analysis. Please try again."
            audio_html = text_to_speech(response, LANGUAGES[selected_language])
            st.components.v1.html(audio_html, height=0)

# Get current location and auto-fill data
try:
    lat, lon, city, region, country = get_current_location()
    
    if lat and lon:
        # Get weather data
        temperature, humidity, rainfall = get_weather_data(lat, lon)
        
        # Get soil data
        soil_type, soil_ph, soil_moisture, nitrogen, phosphorus, potassium = get_soil_data(lat, lon)
        
        # Set default region based on location
        indian_states = ["Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", 
                        "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Gujarat",
                        "Odisha", "Jharkhand", "West Bengal", "Bihar"]
        
        default_region = region if region in indian_states else "Select"
    else:
        # Default values if location cannot be determined
        temperature, humidity, rainfall = 25, 60, 800
        soil_type, soil_ph, soil_moisture, nitrogen, phosphorus, potassium = "Loam", 6.5, 50, 50, 40, 60
        default_region = "Select"
except:
    temperature, humidity, rainfall = 25, 60, 800
    soil_type, soil_ph, soil_moisture, nitrogen, phosphorus, potassium = "Loam", 6.5, 50, 50, 40, 60
    default_region = "Select"

# Sidebar
with st.sidebar:
    try:
        st.image("assets/logo.png", width=280)
    except:
        st.warning("Logo image not found")
    
    st.markdown(f"## {t('farmer_details')}")
    
    farmer_name = st.text_input(t("full_name"), "Rajesh Kumar")
    farm_location = st.selectbox(t("region"), ["Select", "Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", 
                                           "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Gujarat",
                                           "Odisha", "Jharkhand", "West Bengal", "Bihar"], 
                                           index=0 if default_region == "Select" else list(indian_states).index(default_region) + 1)
    farm_size = st.slider(t("farm_size"), 1, 100, 10)
    
    st.markdown(f"## {t('soil_properties')}")
    soil_type = st.selectbox(t("soil_type"), ["Select", "Loam", "Clay", "Sandy", "Silt"], 
                           index=1 if soil_type == "Loam" else 2 if soil_type == "Clay" else 3 if soil_type == "Sandy" else 4 if soil_type == "Silt" else 0)
    soil_ph = st.slider(t("soil_ph"), 4.0, 9.0, soil_ph)
    soil_moisture = st.slider(t("soil_moisture"), 0, 100, soil_moisture)
    nitrogen = st.slider(t("nitrogen"), 0, 200, nitrogen)
    phosphorus = st.slider(t("phosphorus"), 0, 200, phosphorus)
    potassium = st.slider(t("potassium"), 0, 200, potassium)
    
    st.markdown(f"## {t('env_factors')}")
    temperature = st.slider(t("temperature"), 0, 45, int(temperature))
    rainfall = st.slider(t("rainfall"), 0, 2000, int(rainfall))
    humidity = st.slider(t("humidity"), 0, 100, int(humidity))
    
    analyze_button = st.button(t("analyze_btn"), type="primary")

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

# Function to display detailed factor analysis
def display_factor_analysis(details):
    st.markdown(f"#### {t('detailed_factor_analysis')}")
    
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
tab1, tab2, tab3, tab4 = st.tabs([
    t("farm_overview"), 
    t("crop_recommendation"), 
    t("soil_analysis"), 
    t("weather_forecast")
])

with tab1:
    st.markdown(f'<h2 class="sub-header">{t("farm_overview")}</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.markdown(f'<div class="card"><h3>{t("farm_size").split("(")[0].strip()}</h3><p style="font-size: 24px; color: #2E8B57;">{farm_size} acres</p></div>', unsafe_allow_html=True)
    with col2: 
        soil_display = soil_type if soil_type != "Select" else "Not specified"
        st.markdown(f'<div class="card"><h3>{t("soil_type")}</h3><p style="font-size: 24px; color: #2E8B57;">{soil_display}</p></div>', unsafe_allow_html=True)
    with col3: 
        region_display = farm_location if farm_location != "Select" else "Not specified"
        st.markdown(f'<div class="card"><h3>{t("region")}</h3><p style="font-size: 24px; color: #2E8B57;">{region_display}</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown(f'<h2 class="sub-header">{t("crop_recommendation")}</h2>', unsafe_allow_html=True)
    
    if analyze_button:
        with st.spinner(t("analyzing_data")):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            recommendations = predict_best_crop(soil_type, soil_ph, nitrogen, phosphorus, 
                                              potassium, temperature, rainfall, humidity, farm_location)
            
            # Display top recommendation
            top_recommendation = recommendations[0]
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown(f"### 🌱 {t('top_recommendation')}: {top_recommendation['crop']}")
            st.markdown(f"{t('expected_yield')}: {top_recommendation['yield']} tons/acre")
            st.markdown(f"{t('success_probability')}: {top_recommendation['probability']}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display suitability chart
            st.plotly_chart(create_suitability_chart(top_recommendation['details'], top_recommendation['crop']), 
                           use_container_width=True)
            
            # Display detailed factor analysis
            display_factor_analysis(top_recommendation['details'])
            
            # Display reasons
            st.markdown(f"#### {t('why_this_crop')}")
            for reason in top_recommendation['reasons']:
                st.info(f"• {reason}")
            
            # Display crop details
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(t("best_planting_time"))
                st.write(top_recommendation['planting_time'])
                st.markdown(t("water_requirements"))
                st.write(top_recommendation['water_req'])
            with col2:
                st.markdown(t("fertilizer_recommendations"))
                st.write(top_recommendation['fertilizer'])
                st.markdown(t("harvest_timeline"))
                st.write(top_recommendation['harvest_time'])
            
            # Display market insights
            st.markdown(f"#### {t('market_insights')}")
            st.success(f"{t('current_market_price')}: {top_recommendation['market_price']} per kg")
            st.write(f"{t('demand_trend')}: {top_recommendation['demand_trend']}")
            
            # Show alternative options
            if len(recommendations) > 1:
                st.markdown(f"#### {t('alternative_options')}")
                cols = st.columns(len(recommendations) - 1)
                for idx, rec in enumerate(recommendations[1:]):
                    with cols[idx]:
                        st.markdown(f'<div class="analysis-card"><h4>{rec["crop"]}</h4><p>Score: {rec["score"]:.1f}</p><p>Probability: {rec["probability"]}%</p></div>', 
                                  unsafe_allow_html=True)
            
            # Voice output of the recommendation
            recommendation_text = f"Based on your farm data, I recommend growing {top_recommendation['crop']}. " \
                                 f"Expected yield is {top_recommendation['yield']} tons per acre with a success probability of {top_recommendation['probability']} percent. " \
                                 f"The best planting time is {top_recommendation['planting_time']} and water requirements are {top_recommendation['water_req']}."
            
            audio_html = text_to_speech(recommendation_text, LANGUAGES[selected_language])
            st.components.v1.html(audio_html, height=0)
    
    else:
        st.info(t("click_to_analyze"))

with tab3:
    st.markdown(f'<h2 class="sub-header">{t("soil_analysis")}</h2>', unsafe_allow_html=True)
    
    if soil_type != "Select":
        try:
            soil_img = Image.open(f"assets/soil_types/{soil_type.lower()}.png")
            st.image(soil_img, caption=f"{soil_type} Soil", use_container_width=True)
        except:
            st.warning("Soil image not available")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown(f'<div class="weather-card"><h4>{t("ph_level")}</h4><p style="font-size: 20px;">{soil_ph}</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><h4>{t("moisture")}</h4><p style="font-size: 20px;">{soil_moisture}%</p></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown(f'<div class="weather-card"><h4>{t("nitrogen")}</h4><p style="font-size: 20px;">{nitrogen} kg/ha</p></div>', unsafe_allow_html=True)
    with col4: 
        st.markdown(f'<div class="weather-card"><h4>{t("organic_matter")}</h4><p style="font-size: 20px;">3.2%</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: 
        st.markdown(f'<div class="weather-card"><h4>{t("phosphorus")}</h4><p style="font-size: 20px;">{phosphorus} kg/ha</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><h4>{t("potassium")}</h4><p style="font-size: 20px;">{potassium} kg/ha</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown(f'<h2 class="sub-header">{t("weather_forecast")}</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.markdown(f'<div class="weather-card"><h4>{t("temperature")}</h4><p style="font-size: 20px;">{temperature}°C</p></div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div class="weather-card"><h4>{t("humidity")}</h4><p style="font-size: 20px;">{humidity}%</p></div>', unsafe_allow_html=True)
    with col3: 
        st.markdown(f'<div class="weather-card"><h4>{t("rainfall")}</h4><p style="font-size: 20px;">{rainfall} mm</p></div>', unsafe_allow_html=True)
    with col4: 
        st.markdown(f'<div class="weather-card"><h4>{t("wind_speed")}</h4><p style="font-size: 20px;">12 km/h</p></div>', unsafe_allow_html=True)
    
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

