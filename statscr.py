import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🕵️ Statistical Detective: AI to the Rescue")
st.write("Solve the crime by analyzing clues, interrogating suspects, and using AI insights!")

# Crime Report Setup
crime_reports = [
    "🔍 A robbery was reported at a mall. The suspect was last seen near the food court.",
    "🔥 A mysterious arson case occurred in an industrial area at midnight. Witnesses saw a shadowy figure.",
    "💰 A burglary took place in the suburbs. The suspect fled on foot before police arrived.",
    "📞 A fraud case was reported downtown. The victim lost thousands due to an online scam.",
]

# Generate crime data
@st.cache_data
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    suspects = ["John", "Sarah", "Mike", "Emma", "David"]
    data = []
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)

    for i in range(1, 6):  # Generate 5 cases
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        
        data.append({
            "Case_ID": i,
            "Crime_Report": random.choice(crime_reports),
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Suspect_Name": random.choice(suspects),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
        })
    
    return pd.DataFrame(data)

df = generate_crime_data()

# Show crime report first instead of raw data
selected_case = df.sample(1).iloc[0]
st.subheader("📜 Crime Report:")
st.write(selected_case["Crime_Report"])
st.write(f"📅 Date: {selected_case['Date']} | ⏰ Time: {selected_case['Time']} | 📍 Location: {selected_case['Location']}")

# ---------- Clue Board UI ----------
st.subheader("🔎 Clue Board")
clues = [
    f"👤 Witnesses saw someone matching the description of {selected_case['Suspect_Name']}.",
    f"🕒 The crime happened around {selected_case['Time']}.",
    f"🔪 Weapon involved: {selected_case['Weapon_Used']}.",
]

# Reveal clues step by step
if "clue_index" not in st.session_state:
    st.session_state.clue_index = 0

if st.button("🔍 Reveal Next Clue"):
    if st.session_state.clue_index < len(clues):
        st.session_state.clue_index += 1

for i in range(st.session_state.clue_index):
    st.write(clues[i])

# ---------- Suspect Interrogation ----------
st.subheader("🗣️ Interrogate a Suspect")
question = st.radio("Ask a question:", ["Where were you last night?", "Do you know the victim?", "What were you doing at the crime scene?"])

if st.button("🎙️ Ask Question"):
    responses = {
        "Where were you last night?": "I was at home watching TV, I swear!",
        "Do you know the victim?": "I have never met them before...",
        "What were you doing at the crime scene?": "I was just passing by, wrong place wrong time!",
    }
    st.write(f"🕵️ Suspect: {responses[question]}")

# ---------- AI-Assisted Crime Pattern Detection ----------
st.subheader("📊 AI Crime Analysis")

location_map = {"Downtown": 0, "City Park": 1, "Suburbs": 2, "Industrial Area": 3, "Mall": 4}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "Hotspot A", 1: "Hotspot B", 2: "Hotspot C"})

st.write(f"📍 Crime Zone: {df[df['Location'] == selected_case['Location']]['Cluster_Location'].values[0]}")
st.write("📈 AI suggests this zone has a high probability of repeat crimes.")

# ---------- Make a Guess ----------
st.subheader("🕵️‍♂️ Make Your Guess")
guessed_name = st.selectbox("Who is the suspect?", df["Suspect_Name"].unique())
guessed_age = st.slider("What is the suspect's age?", 18, 50)
guessed_gender = st.radio("What is the suspect's gender?", ["Male", "Female"])
guessed_gender = 0 if guessed_gender == "Male" else 1

if st.button("🚔 Submit Arrest Warrant"):
    correct_name = guessed_name == selected_case["Suspect_Name"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]

    if correct_name and correct_age and correct_gender:
        st.success(f"🎉 You solved the case! {selected_case['Suspect_Name']} has been arrested!")
    else:
        st.error("❌ Incorrect! The suspect is still at large. Try again!")

# ---------- Restart Game ----------
if st.button("🔄 New Case"):
    st.session_state.clue_index = 0
    st.rerun()
