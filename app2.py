import os 
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

os.environ["OMP_NUM_THREADS"] = "1"

st.set_page_config(layout="wide")  # Wide layout for better display

st.title("🔎 Statistical Detective: AI to the Rescue")
st.write("Solve the crime mystery using AI! Analyze the hints, make deductions, and crack the case!")

# Game difficulty settings
difficulty_levels = {"Easy": 5, "Hard": 3, "Expert": 2}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
if "selected_difficulty" not in st.session_state or st.session_state.selected_difficulty != difficulty:
    st.session_state.selected_difficulty = difficulty
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.new_game = True

@st.cache_data  # Cache dataset to keep cases consistent
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):  # Generate 20 cases
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
st.dataframe(df.drop(columns=["Time_Minutes"], errors="ignore"), use_container_width=True)

# Crime pattern detection
location_map = {"Downtown": 0, "City Park": 1, "Suburbs": 2, "Industrial Area": 3, "Mall": 4}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

cluster_hints = {
    "High-Risk Zone A": "Locals whisper about strange figures lurking in the shadows at odd hours...",
    "High-Risk Zone B": "The bustling crowd here makes it easier for quick hands to strike unnoticed...",
    "High-Risk Zone C": "Neighbors have reported missing items when they return home late..."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)
st.write("AI-Detected Crime Hotspots:")
st.dataframe(df[['Case_ID', 'Location', 'Time', 'Cluster_Location', 'Cluster_Hint']], use_container_width=True)

# Select a case for the player
if "selected_case" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

st.write("🔎 AI Predictions:")
st.write(f"🕵️ Witness reports suggest the suspect is likely in their {selected_case['Suspect_Age'] // 10 * 10}s.")
st.write(f"⏰ Some say they noticed unusual activity around {selected_case['Time']}.")
st.write(f"📍 Crime occurred in a place known for {df[df['Location'] == selected_case['Location']]['Cluster_Hint'].values[0]}")

st.write(f"🔢 Attempts left: {st.session_state.attempts}")

guessed_location = st.selectbox("Where did the crime occur?", list(location_map.keys()), key="crime_location")
guessed_age = st.slider("What is the suspect's age?", 18, 50, key="suspect_age")
guessed_gender = st.radio("What is the suspect's gender?", ["Male", "Female"], key="suspect_gender")
guessed_gender = 0 if guessed_gender == "Male" else 1

if st.button("Submit Guess", key="submit_guess"):
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success(f"🎉 Correct! You've solved the case. Reward: 🎖 {difficulty} Level Badge")
    else:
        st.session_state.attempts -= 1
        feedback = []
        if not correct_location:
            feedback.append("The location doesn't seem quite right...")
        if not correct_age:
            feedback.append("The suspect's age estimate seems off...")
        if not correct_gender:
            feedback.append("Something feels different about the suspect's description...")
        
        if st.session_state.attempts > 0:
            st.error("💀 Not quite! " + " ".join(feedback) + f" Attempts left: {st.session_state.attempts}")
        else:
            st.error("💀 No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"🕵️ Age: {selected_case['Suspect_Age']}")
            st.write(f"👤 Gender: {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female'}")

if st.button("🔄 New Game"):
    st.session_state.new_game = True
    st.session_state.attempts = difficulty_levels[difficulty]
    st.rerun()
