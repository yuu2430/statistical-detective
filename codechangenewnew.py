import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from scipy import stats

os.environ["OMP_NUM_THREADS"] = "1"

# Enhanced color scheme with proper dropdown styling
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5DC;
        color: #4B3832;
        font-family: 'Courier New', monospace;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #6F4E37 !important;
        color: #FFFFFF !important;
        border-radius: 5px !important;
    }
    .stSlider div[data-testid="stThumbValue"] {
        color: #4B3832 !important;
    }
    .stRadio div[role="radiogroup"] {
        background-color: #FFF4E6 !important;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #6F4E37 !important;
        color: #FFF4E6 !important;
        border-radius: 8px;
        padding: 10px 24px;
        border: 2px solid #4B3832;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4B3832 !important;
        transform: scale(1.05);
    }
    .stSuccess {
        background-color: #D8CCA3 !important;
        color: #4B3832 !important;
        border: 1px solid #6F4E37;
    }
    .stError {
        background-color: #FFE4C4 !important;
        color: #8B0000 !important;
        border: 1px solid #8B0000;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 The Logical Sleuth")
st.write("*Analyze the crime database, follow the evidence, and identify the suspect!*")

# Game settings with enhanced data validation
difficulty_levels = {
    "Easy": {"attempts": 3, "hints": 3},
    "Hard": {"attempts": 2, "hints": 2},
    "Expert": {"attempts": 1, "hints": 1}
}

difficulty = st.selectbox("Choose Your Challenge Level", list(difficulty_levels.keys()))
current_difficulty = difficulty_levels[difficulty]

@st.cache_data
def generate_crime_data():
    # Create logical patterns
    patterns = {
        "Burglary": {
            "locations": ["Residential Area", "Old Town"],
            "time_range": (20, 6),  # 8PM-6AM
            "age_range": (25, 45),
            "gender_bias": {"Male": 0.8, "Female": 0.2}
        },
        "Fraud": {
            "locations": ["Financial District", "Old Town"],
            "time_range": (9, 17),  # 9AM-5PM
            "age_range": (35, 55),
            "gender_bias": {"Male": 0.4, "Female": 0.6}
        },
        "Assault": {
            "locations": ["Industrial Zone", "Old Town"],
            "time_range": (18, 23),  # 6PM-11PM
            "age_range": (20, 40),
            "gender_bias": {"Male": 0.85, "Female": 0.15}
        },
        "Cyber Crime": {
            "locations": ["Financial District", "Residential Area"],
            "time_range": (12, 4),  # 12PM-4AM
            "age_range": (18, 35),
            "gender_bias": {"Male": 0.7, "Female": 0.3}
        }
    }

    cases = []
    for case_id in range(1, 11):
        crime_type = random.choice(list(patterns.keys()))
        pattern = patterns[crime_type]
        
        # Generate logically connected data
        location = random.choice(pattern["locations"])
        
        # Time generation based on pattern
        start_hour, end_hour = pattern["time_range"]
        hour = random.randint(start_hour, end_hour) % 24
        minute = random.choice(["00", "15", "30", "45"])
        time = f"{hour:02d}:{minute}"
        
        # Age generation with pattern-based distribution
        age = int(np.clip(np.random.normal(
            sum(pattern["age_range"])/2,  # Mean of range
            (pattern["age_range"][1] - pattern["age_range"][0])/6  # Std dev
        ), 18, 65))
        
        # Gender selection with pattern bias
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

# Enhanced hint generation with error handling
def generate_hints(selected_case, difficulty):
    hints = []
    crime_type = selected_case["Crime_Type"]
    pattern = {
        "Burglary": {
            "locations": ["Residential Area", "Old Town"],
            "time": "night hours (8PM-6AM)",
            "age": "25-45 years old",
            "gender": "predominantly male (80%)"
        },
        "Fraud": {
            "locations": ["Financial District", "Old Town"],
            "time": "business hours (9AM-5PM)",
            "age": "35-55 years old",
            "gender": "mixed gender (40% male)"
        },
        "Assault": {
            "locations": ["Industrial Zone", "Old Town"],
            "time": "evening hours (6PM-11PM)",
            "age": "20-40 years old",
            "gender": "mostly male (85%)"
        },
        "Cyber Crime": {
            "locations": ["Financial District", "Residential Area"],
            "time": "late hours (12PM-4AM)",
            "age": "18-35 years old",
            "gender": "male-dominated (70%)"
        }
    }.get(crime_type, {})

    if pattern:
        hints.extend([
            f"🔍 This type of crime ({crime_type}) typically occurs in {', '.join(pattern['locations'])}",
            f"🕒 Common timeframe: {pattern['time']}",
            f"👤 Suspect profile: {pattern['age']}, {pattern['gender']}"
        ])
    
    return hints[:current_difficulty["hints"]]
    
# Session state initialization with validation
if "target_case" not in st.session_state:
    st.session_state.target_case = df.sample(1).iloc[0]
    st.session_state.attempts = current_difficulty["attempts"]
    st.session_state.hints_used = 0

st.header("Crime Database")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.header("Case Analysis Toolkit")

with st.expander("🔍 Reveal Investigative Hints", expanded=difficulty=="Easy"):
    hints = generate_hints(st.session_state.target_case, difficulty)
    for hint in hints:
        st.write(f"🔖 {hint}")
    st.session_state.hints_used = len(hints)

col1, col2, col3 = st.columns(3)
with col1:
    loc_guess = st.selectbox("Crime Location", df["Location"].unique())
with col2:
    age_guess = st.slider("Suspect Age", 18, 65, 30)
with col3:
    gender_guess = st.radio("Suspect Gender", ["Male", "Female"])

if st.button("Submit Forensic Report"):
    st.session_state.attempts -= 1
    target = st.session_state.target_case
    correct = (loc_guess == target["Location"]) & (age_guess == target["Suspect_Age"]) & (gender_guess == target["Suspect_Gender"])
    
    if correct:
        st.success("🎉 Case Solved! The evidence matches perfectly!")
        st.balloons()
    else:
        feedback = []
        if loc_guess != target["Location"]:
            feedback.append("📍 Location mismatch with crime patterns")
        if abs(age_guess - target["Suspect_Age"]) > 5:
            feedback.append("📈 Age estimate significantly off demographic profile")
        elif age_guess != target["Suspect_Age"]:
            feedback.append("📈 Age estimate close but not exact")
        if gender_guess != target["Suspect_Gender"]:
            feedback.append("👤 Gender probability mismatch")
        
        if st.session_state.attempts > 0:
            st.error(f"🔍 Inconsistent Findings: {' • '.join(feedback)}")
        else:
            st.error(f"❌ Case Closed Unresolved. Correct answer was: {target['Location']}, Age {target['Suspect_Age']}, {target['Suspect_Gender']}")
            st.session_state.target_case = df.sample(1).iloc[0]
            st.session_state.attempts = current_difficulty["attempts"]

st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Hints Used: {st.session_state.hints_used}/{current_difficulty['hints']}")

if st.button("🔄 Start New Investigation"):
    st.session_state.target_case = df.sample(1).iloc[0]
    st.session_state.attempts = current_difficulty["attempts"]
    st.rerun()
