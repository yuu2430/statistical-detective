import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from scipy import stats  # For confidence interval calculation

# Initialize Streamlit configuration first
st.set_page_config(
    page_title="🔍 Statistical Detective",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Updated Nature-inspired Color Theme with original table styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f0e6;
        color: #4f2022;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #9a816b !important;
        color: #ffffff !important;
        border-radius: 5px !important;
    }
    .stSlider div[data-testid="stThumbValue"] {
        color: #4f2022 !important;
    }
    .stSlider div[data-baseweb="slider"] {
        background-color: transparent;
    }
    .stRadio div[role="radiogroup"] {
        background-color: #ffffff !important;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #9a816b;
    }
    .stButton>button {
        background-color: #65b1df !important;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 10px 24px;
        border: 2px solid #4f2022;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4f2022 !important;
        transform: scale(1.05);
    }
    .stSuccess {
        background-color: #acdb01 !important;
        color: #4f2022 !important;
        border: 1px solid #9a816b;
    }
    .stError {
        background-color: #9a816b !important;
        color: #ffffff !important;
        border: 1px solid #4f2022;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 Statistical Detective")
st.write("*Use statistics and hints! Analyze the data, interpret the probabilities, and catch the suspect!*")

# Game difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
attempts_left = difficulty_levels[difficulty]
if "attempts" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.attempts = attempts_left

@st.cache_data  # Cache dataset to keep cases consistent
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 11):  # Generate 20 cases
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        data.append({
            "Case_ID": i,
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
            "Time_Minutes": crime_time_minutes
        })
    return pd.DataFrame(data)

df = generate_crime_data()

# Display crime database without scrolling (original table styling)
st.header("📊 Recent Crime Cases")
st.dataframe(
    df.drop(columns=["Time_Minutes"], errors="ignore"),
    use_container_width=True,
    height=(len(df) + 1) * 35 + 3  # Dynamic height based on rows
)

# Crime pattern detection
location_map = {"Manjalpur": 0, "Fatehgunj": 1, "Gorwa": 2, "Makarpura": 3}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

cluster_hints = {
    "High-Risk Zone A": "Data shows 70% of crimes here happen at night, often involving weapons.",
    "High-Risk Zone B": "Statistically, fraud and pickpocketing occur 60% of the time in this zone.",
    "High-Risk Zone C": "Burglary incidents make up 55% of crimes in this area, usually in the evenings."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)

# Select a case for the player
if "selected_case" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

# Calculate the confidence interval for suspect age
age_group = selected_case['Suspect_Age'] // 10 * 10
age_data = df['Suspect_Age']
age_count = age_data[(age_data // 10 * 10) == age_group].count()
total_cases = len(age_data)

# Proportion of suspects in the same age group
proportion = age_count / total_cases

# 95% confidence interval for proportion
ci_low, ci_high = stats.norm.interval(0.95, loc=proportion, scale=np.sqrt(proportion * (1 - proportion) / total_cases))

# Convert confidence interval into percentage
confidence_percent_low = int(ci_low * 100)
confidence_percent_high = int(ci_high * 100)

st.divider()
st.header("🕵️♂️ Investigation Toolkit")

# Hint system
with st.expander("🔍 Reveal Investigation Clues", expanded=difficulty=="Easy"):
    st.write(f"🔖 Probability suggests the suspect is likely in their {age_group}s (~{confidence_percent_low}%-{confidence_percent_high}% confidence).")
    st.write(f"🔖 Location Analysis: {selected_case['Cluster_Hint']}")

# Investigation inputs
col1, col2, col3 = st.columns(3)
with col1:
    guessed_location = st.selectbox("Crime Location", list(location_map.keys()), key="crime_location")
with col2:
    guessed_age = st.slider("Suspect Age", 18, 50, 30, key="suspect_age")
with col3:
    guessed_gender = st.radio("Suspect Gender", ["Male", "Female"], key="suspect_gender")

guessed_gender = 0 if guessed_gender == "Male" else 1

# Submit investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Case Solved! You've identified the suspect!")
        st.balloons()
    else:
        feedback = []
        if not correct_location:
            feedback.append("📍 Location doesn't match crime pattern")
        if abs(guessed_age - selected_case["Suspect_Age"]) > 5:
            feedback.append("📈 Age estimate significantly off")
        elif guessed_age != selected_case["Suspect_Age"]:
            feedback.append("📈 Age estimate close but not exact")
        if guessed_gender != selected_case["Suspect_Gender"]:
            feedback.append("👤 Gender probability mismatch")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
        else:
            st.error(f"❌ Case Closed. Correct answer: {selected_case['Location']}, Age {selected_case['Suspect_Age']}, {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female'}")
            st.session_state.selected_case = df.sample(1).iloc[0]
            st.session_state.attempts = difficulty_levels[difficulty]

# Status bar
st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Attempts Left: {st.session_state.attempts}")

# New case button
if st.button("🔄 Start New Case"):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.attempts = difficulty_levels[difficulty]
    st.rerun()
