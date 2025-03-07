import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.cluster import KMeans

# Initialize Streamlit configuration
st.set_page_config(
    page_title="🔍 Statistical Detective",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 3  # Default attempts
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "new_game" not in st.session_state:
    st.session_state.new_game = True
if "hints_revealed" not in st.session_state:
    st.session_state.hints_revealed = 0  # Track how many hints have been revealed

# Difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
st.session_state.attempts = difficulty_levels[difficulty]

# Generate crime data
@st.cache_data
def generate_crime_data():
    crime_types = ["Theft", "Robbery", "Assault", "Burglary", "Fraud", "Kidnapping"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    for _ in range(10):  # Generate 10 cases
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        data.append({
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female", "Other"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
            "Time_Minutes": crime_time_minutes
        })
    return pd.DataFrame(data)

df = generate_crime_data()

# Select a case
if st.session_state.selected_case is None or st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0

selected_case = st.session_state.selected_case

# Investigation inputs
guessed_location = st.selectbox("Crime Location", df["Location"].unique(), key="crime_location")
guessed_age = st.slider("Suspect Age", 18, 50, 30, key="suspect_age")
guessed_gender = st.radio("Suspect Gender", ["Male", "Female", "Other"], key="suspect_gender")

# Submit investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Case Solved! You've identified the suspect!")
        st.session_state.score += 1
        st.session_state.new_game = True
    else:
        feedback = []
        if not correct_location:
            feedback.append("📍 Location doesn't match.")
        if abs(guessed_age - selected_case["Suspect_Age"]) > 5:
            feedback.append("📈 Age estimate significantly off.")
        elif guessed_age != selected_case["Suspect_Age"]:
            feedback.append("📈 Age estimate close but not exact.")
        if guessed_gender != selected_case["Suspect_Gender"]:
            feedback.append("👤 Gender mismatch.")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
            st.session_state.hints_revealed += 1
        else:
            st.error("❌ Case Closed. No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"🔢 Age: {selected_case['Suspect_Age']}")
            st.write(f"👤 Gender: {selected_case['Suspect_Gender']}")
            st.session_state.new_game = True

# Reset the game
if st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0
    st.rerun()
