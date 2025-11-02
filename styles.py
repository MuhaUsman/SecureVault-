"""
Premium CSS styling for SecureVault Pro
Modern dark mode with glassmorphism effects and smooth animations
"""

import streamlit as st

def load_custom_css():
    """Load premium custom CSS styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Logo Container */
    .logo-container {
        text-align: center;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
    }
    
    .logo-text {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .logo-tagline {
        font-size: 0.75rem;
        color: #a0a0c0;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Balance Card with Gradient */
    .balance-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .balance-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }
    
    .balance-amount {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
        position: relative;
        z-index: 1;
    }
    
    .balance-label {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Labels */
    .stTextInput>label,
    .stNumberInput>label,
    .stSelectbox>label {
        color: #a0a0c0;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    /* Transaction Cards */
    .transaction-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border-left: 4px solid #667eea;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .transaction-card:hover {
        background: rgba(255, 255, 255, 0.06);
        transform: translateX(5px);
    }
    
    .transaction-credit {
        border-left-color: #00d4aa;
    }
    
    .transaction-debit {
        border-left-color: #ff6b9d;
    }
    
    /* Stats Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        border-color: #667eea;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #a0a0c0;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Success Message */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.1) 0%, rgba(0, 212, 170, 0.05) 100%);
        border-left: 4px solid #00d4aa;
        border-radius: 12px;
        padding: 1rem 1.5rem;
    }
    
    /* Error Message */
    .stError {
        background: linear-gradient(135deg, rgba(255, 107, 157, 0.1) 0%, rgba(255, 107, 157, 0.05) 100%);
        border-left: 4px solid #ff6b9d;
        border-radius: 12px;
        padding: 1rem 1.5rem;
    }
    
    /* Warning Message */
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 217, 61, 0.1) 0%, rgba(255, 217, 61, 0.05) 100%);
        border-left: 4px solid #ffd93d;
        border-radius: 12px;
        padding: 1rem 1.5rem;
    }
    
    /* Info Message */
    .stInfo {
        background: linear-gradient(135deg, rgba(107, 207, 255, 0.1) 0%, rgba(107, 207, 255, 0.05) 100%);
        border-left: 4px solid #6bcfff;
        border-radius: 12px;
        padding: 1rem 1.5rem;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.03);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #a0a0c0;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Welcome Hero Section */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #a0a0c0;
        margin-bottom: 2rem;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-success {
        background: rgba(0, 212, 170, 0.2);
        color: #00d4aa;
        border: 1px solid #00d4aa;
    }
    
    .badge-warning {
        background: rgba(255, 217, 61, 0.2);
        color: #ffd93d;
        border: 1px solid #ffd93d;
    }
    
    .badge-danger {
        background: rgba(255, 107, 157, 0.2);
        color: #ff6b9d;
        border: 1px solid #ff6b9d;
    }
    
    .badge-info {
        background: rgba(107, 207, 255, 0.2);
        color: #6bcfff;
        border: 1px solid #6bcfff;
    }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Progress Bar for Password Strength */
    .password-strength-bar {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .password-strength-fill {
        height: 100%;
        transition: all 0.3s ease;
        border-radius: 10px;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .balance-amount {
            font-size: 2rem;
        }
        
        .glass-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_password_strength(password):
    """Display visual password strength indicator"""
    if not password:
        return
    
    # Calculate strength
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 20
    else:
        feedback.append("Use at least 8 characters")
    
    if len(password) >= 12:
        score += 10
    
    if any(c.islower() for c in password):
        score += 15
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 15
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 15
    else:
        feedback.append("Add numbers")
    
    if any(c in "@#$%&*!" for c in password):
        score += 15
    else:
        feedback.append("Add special characters")
    
    # Bonus for variety
    if len(set(password)) >= 8:
        score += 10
    
    # Determine strength level and color
    if score < 30:
        strength = "Very Weak"
        color = "#ff6b9d"
    elif score < 50:
        strength = "Weak"
        color = "#ffd93d"
    elif score < 70:
        strength = "Fair"
        color = "#6bcfff"
    elif score < 90:
        strength = "Good"
        color = "#00d4aa"
    else:
        strength = "Excellent"
        color = "#00d4aa"
    
    # Display strength indicator
    st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #a0a0c0;">Password Strength</span>
                <span style="color: {color}; font-weight: 600;">{strength}</span>
            </div>
            <div class="password-strength-bar">
                <div class="password-strength-fill" style="background: {color}; width: {score}%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    return score, strength, feedback