import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from scipy import stats

# Initialize Streamlit configuration first
st.set_page_config(
    page_title="🔍 Vadodara Crime Solver",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Custom styling for Vadodara theme
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF5E6;
        color: #2F4F4F;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #8B4513 !important;
        color: #FFFFFF !important;
        border-radius: 5px !important;
    }
    .stSlider div[data-testid="stThumbValue"] {
        color: #2F4F4F !important;
    }
    .stRadio div[role="radiogroup"] {
        background-color: #FFEBCD !important;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #CD853F !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        padding: 10px 24px;
        border: 2px solid #8B4513;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #A0522D !important;
        transform: scale(1.05);
    }
    .stSuccess {
        background-color: #98FB98 !important;
        color: #006400 !important;
        border: 1px solid #228B22;
    }
    .stError {
        background-color: #FFB6C1 !important;
        color: #8B0000 !important;
        border: 1px solid #8B0000;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 Vadodara Crime Solver")
st.write("*Analyze local crime patterns and catch the culprit!*")

# Game settings
difficulty_levels = {
    "Easy": {"attempts": 3, "hints": 3},
    "Medium": {"attempts": 2, "hints": 2},
    "Hard": {"attempts": 1, "hints": 1}
}

difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()))
current_difficulty = difficulty_levels[difficulty]

@st.cache_data
def generate_crime_data():
    patterns = {
        "Street Robbery": {
            "locations": ["Manjalpur", "Fatehgunj"],
            "time_range": (20, 6),  # 8PM-6AM
            "age_range": (20, 35),
            "gender_bias": {"Male": 0.85, "Female": 0.15}
        },
        "Vehicle Theft": {
            "locations": ["Makarpura", "Gorwa"],
            "time_range": (22, 4),  # 10PM-4AM
            "age_range": (25, 40),
            "gender_bias": {"Male": 0.9, "Female": 0.1}
        },
        "Chain Snatching": {
            "locations": ["Fatehgunj", "Manjalpur"],
            "time_range": (18, 23),  # 6PM-11PM
            "age_range": (18, 30),
            "gender_bias": {"Male": 0.95, "Female": 0.05)
        },
        "Cyber Fraud": {
            "locations": ["Gorwa", "Makarpura"],
            "time_range": (10, 16),  # 10AM-4PM
            "age_range": (25, 45),
            "gender_bias": {"Male": 0.7, "Female": 0.3}
        }
    }

    cases = []
    for case_id in range(1, 11):
        crime_type = random.choice(list(patterns.keys()))
        pattern = patterns[crime_type]
        
        # Generate location
        location = random.choice(pattern["locations"])
        
        # Generate time
        start_hour, end_hour = pattern["time_range"]
        hour = random.randint(start_hour, end_hour) % 24
        minute = random.choice(["00", "15", "30", "45"])
        time = f"{hour:02d}:{minute}"
        
        # Generate age
        age = int(np.clip(np.random.normal(
            sum(pattern["age_range"])/2,
            (pattern["age_range"][1] - pattern["age_range"][0])/6
        ), 18, 65))
        
        # Generate gender
        gender = random.choices(
            list(pattern["gender_bias"].keys()),
            weights=list(pattern["gender_bias"].values())
        )[0]

        cases.append({
            "Case_ID": case_id,
            "Date": (datetime(2024, 1, 1) + 
                    timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            "Location": location,
            "Crime_Type": crime_type,
            "Time": time,
            "Suspect_Age": age,
            "Suspect_Gender": gender
        })

    return pd.DataFrame(cases)

df = generate_crime_data()

def generate_hints(selected_case, difficulty_level):
    hints = []
    crime_type = selected_case["Crime_Type"]
    pattern = {
        "Street Robbery": {
            "locations": ["Manjalpur", "Fatehgunj"],
            "time": "late evening to early morning",
            "age": "typically 20-35 years old",
            "gender": "almost always male (85%)"
        },
        "Vehicle Theft": {
            "locations": ["Makarpura", "Gorwa"],
            "time": "late night hours (10PM-4AM)",
            "age": "usually 25-40 years old",
            "gender": "predominantly male (90%)"
        },
        "Chain Snatching": {
            "locations": ["Fatehgunj", "Manjalpur"],
            "time": "evening rush hours",
            "age": "young adults (18-30 years)",
            "gender": "overwhelmingly male (95%)"
        },
        "Cyber Fraud": {
            "locations": ["Gorwa", "Makarpura"],
            "time": "daytime working hours",
            "age": "25-45 years old",
            "gender": "mostly male (70%)"
        }
    }.get(crime_type, {})

    if pattern:
        hints.extend([
            f"🔍 {crime_type} cases usually occur in {', '.join(pattern['locations'])}",
            f"🕒 Common time: {pattern['time']}",
            f"👤 Typical suspect: {pattern['age']}, {pattern['gender']}"
        ])
    
    return hints[:difficulty_levels[difficulty_level]["hints"]]

# Session state management
if "target_case" not in st.session_state:
    st.session_state.target_case = df.sample(1).iloc[0]
    st.session_state.attempts = current_difficulty["attempts"]
    st.session_state.hints_used = 0

# Display crime database
st.header("📊 Recent Crime Cases")
st.dataframe(df, use_container_width=True, height=300)

st.divider()
st.header("🕵️♂️ Investigation Toolkit")

# Hint system
with st.expander("🔍 Reveal Investigation Clues", expanded=difficulty=="Easy"):
    hints = generate_hints(st.session_state.target_case, difficulty)
    for hint in hints:
        st.write(f"🔖 {hint}")
    st.session_state.hints_used = len(hints)

# Investigation inputs
col1, col2, col3 = st.columns(3)
with col1:
    loc_guess = st.selectbox("Crime Location", df["Location"].unique())
with col2:
    age_guess = st.slider("Suspect Age", 18, 65, 30)
with col3:
    gender_guess = st.radio("Suspect Gender", ["Male", "Female"])

# Submit investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    target = st.session_state.target_case
    correct = (loc_guess == target["Location"]) & (age_guess == target["Suspect_Age"]) & (gender_guess == target["Suspect_Gender"])
    
    if correct:
        st.success("🎉 Case Solved! You've identified the suspect!")
        st.balloons()
    else:
        feedback = []
        if loc_guess != target["Location"]:
            feedback.append("📍 Location doesn't match crime pattern")
        if abs(age_guess - target["Suspect_Age"]) > 5:
            feedback.append("📈 Age estimate significantly off")
        elif age_guess != target["Suspect_Age"]:
            feedback.append("📈 Age estimate close but not exact")
        if gender_guess != target["Suspect_Gender"]:
            feedback.append("👤 Gender probability mismatch")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
        else:
            st.error(f"❌ Case Closed. Correct answer: {target['Location']}, Age {target['Suspect_Age']}, {target['Suspect_Gender']}")
            st.session_state.target_case = df.sample(1).iloc[0]
            st.session_state.attempts = current_difficulty["attempts"]

# Status bar
st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Clues Used: {st.session_state.hints_used}/{current_difficulty['hints']}")

# New case button
if st.button("🔄 Start New Case"):
    st.session_state.target_case = df.sample(1).iloc[0]
    st.session_state.attempts = current_difficulty["attempts"]
    st.rerun()
    
