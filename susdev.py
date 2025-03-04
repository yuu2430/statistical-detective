import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

os.environ["OMP_NUM_THREADS"] = "1"

st.set_page_config(layout="wide")  # Wide layout for better display

st.title("🌍 Sustainability Detective: Data to the Rescue")
st.write("Use statistics and AI to solve environmental mysteries! Analyze the data, interpret the probabilities, and take action for a sustainable world.")

# Game difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
attempts_left = difficulty_levels[difficulty]
if "attempts" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.attempts = attempts_left

@st.cache_data  # Cache dataset to keep cases consistent
def generate_sustainability_data():
    issue_types = ["Water Pollution", "Deforestation", "Air Pollution", "Illegal Waste Dumping", "Carbon Emissions"]
    locations = ["Coastal Area", "National Park", "Urban Center", "Industrial Zone", "Agricultural Land"]
    suspected_sources = ["Factory", "Logging Company", "Power Plant", "Unregulated Farm", "Shipping Industry"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):  # Generate 20 cases
        report_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        data.append({
            "Case_ID": i,
            "Date": report_date.strftime('%Y-%m-%d'),
            "Location": random.choice(locations),
            "Environmental_Issue": random.choice(issue_types),
            "Suspected_Source": random.choice(suspected_sources),
            "Severity_Level": random.randint(1, 10),
            "Evidence": random.choice(["Satellite Imagery", "Water Sample Data", "Air Quality Report", "Eyewitness Report", "CO2 Emission Data"]),
            "Status": random.choice(["Unresolved", "Resolved"])
        })
    return pd.DataFrame(data)

df = generate_sustainability_data()
st.dataframe(df, use_container_width=True)

# Select a case for the player
if "selected_case" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.selected_case = df.sample(1).iloc[0].to_dict()
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

st.write("📊 AI Predictions Based on Past Data:")
st.write(f"🌱 Probability suggests the environmental issue is likely caused by a {selected_case['Suspected_Source']} (~{random.randint(60, 80)}% confidence).")
st.write(f"📍 The issue was reported in a {selected_case['Location']} region.")
st.write(f"🔢 Attempts left: {st.session_state.attempts}")

guessed_location = st.selectbox("Where did the issue occur?", df["Location"].unique(), key="issue_location")
guessed_source = st.selectbox("What is the suspected source?", df["Suspected_Source"].unique(), key="suspected_source")
guessed_evidence = st.selectbox("What evidence do you think supports your claim?", df["Evidence"].unique(), key="evidence")

if st.button("Submit Investigation", key="submit_guess"):
    correct_location = guessed_location == selected_case["Location"]
    correct_source = guessed_source == selected_case["Suspected_Source"]
    correct_evidence = guessed_evidence == selected_case["Evidence"]
    
    if correct_location and correct_source and correct_evidence:
        st.success(f"🎉 Correct! You've identified the source of the problem. Reward: 🌿 {difficulty} Level Badge")
    else:
        st.session_state.attempts -= 1
        feedback = []
        if not correct_location:
            feedback.append("Satellite data suggests another location...")
        if not correct_source:
            feedback.append("Emission patterns don't match this source...")
        if not correct_evidence:
            feedback.append("The data points to a different type of evidence...")
        
        if st.session_state.attempts > 0:
            st.error("⚠️ Not quite! " + " ".join(feedback) + f" Attempts left: {st.session_state.attempts}")
        else:
            st.error("❌ No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"🏭 Source: {selected_case['Suspected_Source']}")
            st.write(f"📜 Evidence: {selected_case['Evidence']}")

if st.button("🔄 New Investigation"):
    st.session_state.new_game = True
    st.session_state.attempts = difficulty_levels[difficulty]
    st.rerun()
