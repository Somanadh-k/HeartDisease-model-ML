import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="CardioPredict - Heart Health Analysis",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, professional styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #f8f9fa;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Top header bar */
    .top-bar {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.2rem 2rem;
        margin: -6rem -6rem 2rem -6rem;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-text {
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .tagline {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 3px;
    }
    
    /* Main content container */
    .main-card {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Section headers */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Info banner */
    .info-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 12px;
        margin-bottom: 2.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .info-banner h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    .info-banner p {
        margin: 0;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Input labels */
    .stSelectbox label, .stNumberInput label, .stSlider label {
        font-weight: 500 !important;
        color: #334155 !important;
        font-size: 0.95rem !important;
    }
    
    /* Result cards */
    .result-card {
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 2rem;
        border: 2px solid;
    }
    
    .result-high {
        background: #fef2f2;
        border-color: #dc2626;
        color: #991b1b;
    }
    
    .result-high .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .result-high h2 {
        color: #dc2626;
        font-size: 1.8rem;
        margin: 0.5rem 0;
        font-weight: 700;
    }
    
    .result-low {
        background: #f0fdf4;
        border-color: #16a34a;
        color: #166534;
    }
    
    .result-low .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .result-low h2 {
        color: #16a34a;
        font-size: 1.8rem;
        margin: 0.5rem 0;
        font-weight: 700;
    }
    
    .result-description {
        font-size: 1rem;
        line-height: 1.6;
        margin-top: 1rem;
        opacity: 0.9;
    }
    
    /* Action button */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        padding: 0.85rem 3rem;
        border-radius: 10px;
        border: none;
        font-size: 1.05rem;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
        transition: all 0.2s;
        width: auto;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
    }
    
    /* Recommendations box */
    .recommendations {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
    }
    
    .recommendations h4 {
        margin: 0 0 1rem 0;
        color: #1e293b;
        font-size: 1.1rem;
    }
    
    .recommendations ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .recommendations li {
        margin-bottom: 0.5rem;
        color: #475569;
        line-height: 1.6;
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #64748b;
        font-size: 0.9rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }
    
    /* Compact spacing */
    .stSlider, .stSelectbox, .stNumberInput {
        margin-bottom: 0.3rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load model artifacts
@st.cache_resource
def load_model_artifacts():
    try:
        model = joblib.load("KNN_heart.pkl")
        scaler = joblib.load("scaler.pkl")
        expected_columns = joblib.load("columns.pkl")
        return model, scaler, expected_columns
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please ensure all required files are present.")
        st.stop()

model, scaler, expected_columns = load_model_artifacts()

# Custom header
st.markdown("""
    <div class="top-bar">
        <div class="logo-section">
            <div>
                <div class="logo-text">🫀 CardioPredict</div>
                <div class="tagline">AI-Powered Cardiovascular Risk Assessment</div>
            </div>
        </div>
        <div style="color: #94a3b8; font-size: 0.9rem;">Developed by Somanadh</div>
    </div>
""", unsafe_allow_html=True)

# Info banner
st.markdown("""
    <div class="info-banner">
        <h3>Welcome to Your Heart Health Analysis</h3>
        <p>This clinical decision support tool uses advanced machine learning to evaluate cardiovascular risk factors. 
        Please provide accurate medical information for a comprehensive assessment. Results should be reviewed with your healthcare provider.</p>
    </div>
""", unsafe_allow_html=True)

# Main form in a card
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Create form layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section-title">👤 Demographics</div>', unsafe_allow_html=True)
    age = st.slider("Age", 18, 100, 40)
    sex = st.selectbox("Biological Sex", ["M", "F"], format_func=lambda x: "Male" if x == "M" else "Female")
    
    st.markdown('<div class="section-title" style="margin-top: 2rem;">🩺 Blood Work</div>', unsafe_allow_html=True)
    cholesterol = st.number_input("Total Cholesterol (mg/dL)", 100, 600, 200)
    fasting_bs = st.selectbox("Fasting Blood Sugar", [0, 1],
                              format_func=lambda x: "Normal (≤120 mg/dL)" if x == 0 else "Elevated (>120 mg/dL)")

with col2:
    st.markdown('<div class="section-title">💓 Cardiovascular Metrics</div>', unsafe_allow_html=True)
    resting_bp = st.number_input("Resting BP (mm Hg)", 80, 200, 120)
    max_hr = st.slider("Peak Heart Rate", 60, 220, 150)
    exercise_angina = st.selectbox("Exercise Angina", ["N", "Y"], 
                                   format_func=lambda x: "Absent" if x == "N" else "Present")
    oldpeak = st.slider("ST Depression (Oldpeak)", 0.0, 6.0, 1.0, 0.1)

with col3:
    st.markdown('<div class="section-title">📊 Clinical Findings</div>', unsafe_allow_html=True)
    chest_pain = st.selectbox("Chest Pain Classification", ["ATA", "NAP", "TA", "ASY"],
                             format_func=lambda x: {
                                 "ATA": "Atypical Angina",
                                 "NAP": "Non-Anginal Pain", 
                                 "TA": "Typical Angina",
                                 "ASY": "Asymptomatic"
                             }[x])
    
    resting_ecg = st.selectbox("ECG Results", ["Normal", "ST", "LVH"],
                               format_func=lambda x: {
                                   "Normal": "Normal",
                                   "ST": "ST-T Abnormality",
                                   "LVH": "LV Hypertrophy"
                               }[x])
    
    st_slope = st.selectbox("ST Segment Slope", ["Up", "Flat", "Down"],
                           format_func=lambda x: {
                               "Up": "Upsloping",
                               "Flat": "Flat",
                               "Down": "Downsloping"
                           }[x])

st.markdown('</div>', unsafe_allow_html=True)

# Analysis button
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    analyze = st.button("Analyze Risk Profile", use_container_width=True)

# Prediction logic
if analyze:
    with st.spinner('Processing medical data...'):
        # Prepare input
        raw_input = {
            'Age': age,
            'RestingBP': resting_bp,
            'Cholesterol': cholesterol,
            'FastingBS': fasting_bs,
            'MaxHR': max_hr,
            'Oldpeak': oldpeak,
            'Sex_' + sex: 1,
            'ChestPainType_' + chest_pain: 1,
            'RestingECG_' + resting_ecg: 1,
            'ExerciseAngina_' + exercise_angina: 1,
            'ST_Slope_' + st_slope: 1
        }

        input_df = pd.DataFrame([raw_input])

        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[expected_columns]
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]

        # Display results
        if prediction == 1:
            st.markdown("""
                <div class="result-card result-high">
                    <div class="result-icon">⚠️</div>
                    <h2>Elevated Cardiovascular Risk Detected</h2>
                    <p class="result-description">
                        Based on the clinical parameters provided, the model indicates increased risk factors 
                        for cardiovascular disease. Immediate medical consultation is strongly recommended.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="recommendations">
                    <h4>Recommended Next Steps</h4>
                    <ul>
                        <li>Schedule an appointment with a cardiologist within 1-2 weeks</li>
                        <li>Request comprehensive cardiac workup including stress test and echocardiogram</li>
                        <li>Monitor blood pressure and heart rate daily</li>
                        <li>Review current medications with your physician</li>
                        <li>Consider lifestyle modifications: diet, exercise, stress management</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
                <div class="result-card result-low">
                    <div class="result-icon">✓</div>
                    <h2>Favorable Cardiovascular Profile</h2>
                    <p class="result-description">
                        Current risk assessment indicates lower probability of cardiovascular disease. 
                        Continue maintaining healthy habits and regular medical check-ups.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="recommendations">
                    <h4>Maintenance Recommendations</h4>
                    <ul>
                        <li>Continue annual cardiovascular screening</li>
                        <li>Maintain regular physical activity (150 minutes moderate exercise weekly)</li>
                        <li>Follow heart-healthy Mediterranean-style diet</li>
                        <li>Keep BMI in healthy range (18.5-24.9)</li>
                        <li>Manage stress through mindfulness or relaxation techniques</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="custom-footer">
        <p><strong>Medical Disclaimer:</strong> This tool provides risk assessment based on statistical models and should not replace professional medical diagnosis. 
        All predictions must be validated by qualified healthcare providers. For medical emergencies, contact emergency services immediately.</p>
        <p style="margin-top: 1rem;">© 2024 CardioPredict | Machine Learning Research Project</p>
    </div>
""", unsafe_allow_html=True)
