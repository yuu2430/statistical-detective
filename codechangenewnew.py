import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from scipy import stats

os.environ["OMP_NUM_THREADS"] = "1"

# Custom aesthetic styling
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5DC;
        color: #4B3832;
        font-family: 'Courier New', monospace;
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
    .stSelectbox, .stSlider, .stRadio {
        background-color: #FFF4E6 !important;
        border: 1px solid #6F4E37 !important;
        border-radius: 5px;
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
    .dataframe {
        background-color: #FFF4E6 !important;
        border: 2px solid #6F4E37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 The Logical Sleuth")
st.write("*Analyze the crime database, follow the evidence, and identify the suspect!*")

# Game settings
difficulty_levels = {
    "Easy": {"attempts": 3, "hints": 3},
    "Hard": {"attempts": 2, "hints": 2},
    "Expert": {"attempts": 1, "hints": 1}
}

difficulty = st.selectbox("Choose Your Challenge Level", list(difficulty_levels.keys()))
current_difficulty = difficulty_levels[difficulty]

@st.cache_data
def generate_crime_data():
    crimes = pd.DataFrame({
        "Case_ID": range(1, 21),
        "Date": [datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(20)],
        "Location": random.choices(["Old Town", "Financial District", "Industrial Zone", "Residential Area"], k=20),
        "Crime_Type": random.choices(["Burglary", "Fraud", "Assault", "Cyber Crime"], k=20),
        "Time": [f"{random.randint(0,23):02d}:{random.randint(0,59):02d}" for _ in range(20)],
        "Suspect_Age": np.random.normal(35, 8, 20).astype(int),
        "Suspect_Gender": random.choices(["Male", "Female"], weights=[0.7, 0.3], k=20)
    })
    return crimes

df = generate_crime_data()

# Data analysis for logical hints
def generate_hints(selected_case, difficulty):
    hints = []
    location_data = df[df["Location"] == selected_case["Location"]]
    
    # Age analysis
    age_mean = location_data["Suspect_Age"].mean()
    age_std = location_data["Suspect_Age"].std()
    hints.append(f"📊 Historical data shows suspects in {selected_case['Location']} tend to be between {int(age_mean - age_std)}-{int(age_mean + age_std)} years old")
    
    # Time analysis
    crime_times = pd.to_datetime(location_data["Time"]).dt.hour
    common_time = stats.mode(crime_times).mode[0]
    hints.append(f"🕒 Most crimes here occur around {common_time}:00")
    
    # Gender analysis
    gender_dist = location_data["Suspect_Gender"].value_counts(normalize=True)
    hints.append(f"👥 Suspect gender ratio: {gender_dist.get('Male', 0)*100:.1f}% Male, {gender_dist.get('Female', 0)*100:.1f}% Female")
    
    return hints[:current_difficulty["hints"]]

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

st.caption(f"🔑 Difficulty: {difficulty} • � Hints Used: {st.session_state.hints_used}/{current_difficulty['hints']}")

if st.button("🔄 Start New Investigation"):
    st.session_state.target_case = df.sample(1).iloc[0]
    st.session_state.attempts = current_difficulty["attempts"]
    st.rerun()
