# utils/style.py
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

    /* Custom select box styling */
    .stSelectbox > div > div {
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }

    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--hover-shadow);
    }

    /* Custom slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, var(--accent-color) 0%, #8BC34A 100%);
    }

    /* Tab styling */
    .stTabs > div > div > div
