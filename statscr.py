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
st.write("Solve the crime by analyzing clues, interrogating multiple suspects, and using AI insights!")

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
    data = []
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    
    # Generate 5 cases for variety
    for i in range(1, 6):
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        
        data.append({
            "Case_ID": i,
            "Crime_Report": random.choice(crime_reports),
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": formatted_time,
            "Location": random.choice(locations),
            # This will be used as the true culprit’s details
            "Suspect_Name": random.choice(["John", "Sarah", "Mike", "Emma", "David"]),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
        })
    
    return pd.DataFrame(data)

df = generate_crime_data()

# Select a random case for the detective
if "selected_case" not in st.session_state:
    st.session_state.selected_case = df.sample(1).iloc[0]

selected_case = st.session_state.selected_case

# ---------- Crime Report ----------
st.subheader("📜 Crime Report:")
st.write(selected_case["Crime_Report"])
st.write(f"📅 Date: {selected_case['Date']} | ⏰ Time: {selected_case['Time']} | 📍 Location: {selected_case['Location']}")

# ---------- Generate Suspects ----------
def generate_suspects(case):
    """Generate a list of suspect profiles including one culprit and two decoys."""
    culprit = {
         "Name": case["Suspect_Name"],
         "Age": case["Suspect_Age"],
         "Gender": case["Suspect_Gender"],
         "Role": "Culprit"
    }
    # List of possible names
    all_names = ["John", "Sarah", "Mike", "Emma", "David"]
    decoy_names = [name for name in all_names if name != case["Suspect_Name"]]
    decoy1 = {
         "Name": random.choice(decoy_names),
         "Age": random.randint(18, 50),
         "Gender": random.choice(["Male", "Female"]),
         "Role": "Decoy"
    }
    decoy_names = [name for name in decoy_names if name != decoy1["Name"]]
    decoy2 = {
         "Name": random.choice(decoy_names),
         "Age": random.randint(18, 50),
         "Gender": random.choice(["Male", "Female"]),
         "Role": "Decoy"
    }
    return [culprit, decoy1, decoy2]

if "suspects" not in st.session_state:
    st.session_state.suspects = generate_suspects(selected_case)

# Display suspect profiles (names only for now)
st.subheader("👥 Suspect List")
for suspect in st.session_state.suspects:
    st.write(f"- **{suspect['Name']}**")

# ---------- Clue Board UI ----------
st.subheader("🔎 Clue Board")
clues = [
    f"👤 A witness mentioned a suspect that looks like {st.session_state.suspects[0]['Name']}.",
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

# ---------- Interrogation Section ----------
st.subheader("🗣️ Interrogate Suspects")
# Define possible questions and responses
question_list = [
    "Where were you last night?",
    "Do you know the victim?",
    "What were you doing at the crime scene?"
]

# Responses vary by suspect role (Culprit vs. Decoy)
responses = {
    "Where were you last night?": {
        "Culprit": "I was at home... though I did step out for a bit.",
        "Decoy": "I was home with my family all night."
    },
    "Do you know the victim?": {
        "Culprit": "I barely knew the victim.",
        "Decoy": "Yes, we used to work together."
    },
    "What were you doing at the crime scene?": {
        "Culprit": "I was just passing by, nothing more.",
        "Decoy": "I wasn't anywhere near that area."
    }
}

# Let player select a suspect to interrogate
suspect_names = [s["Name"] for s in st.session_state.suspects]
selected_suspect_name = st.selectbox("Select a suspect to interrogate:", suspect_names, key="suspect_select")

# Get the suspect object from the list
selected_suspect = next(s for s in st.session_state.suspects if s["Name"] == selected_suspect_name)

selected_question = st.selectbox("Select a question to ask:", question_list, key="question_select")

if st.button("🎙️ Ask Question"):
    # Determine the suspect's role for response selection
    role = selected_suspect["Role"]
    answer = responses[selected_question][role]
    st.write(f"🕵️ {selected_suspect['Name']} answers: {answer}")

# ---------- AI-Assisted Crime Pattern Detection ----------
st.subheader("📊 AI Crime Analysis")

location_map = {"Downtown": 0, "City Park": 1, "Suburbs": 2, "Industrial Area": 3, "Mall": 4}
df["Location_Code"] = df["Location"].map(location_map)

# Use K-Means clustering to assign crime zones
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "Hotspot A", 1: "Hotspot B", 2: "Hotspot C"})

zone_hint = df[df['Location'] == selected_case['Location']]['Cluster_Location'].values[0]
st.write(f"📍 Crime Zone: {zone_hint}")
st.write("📈 AI analysis indicates this area has a high probability of recurring crimes.")

# ---------- Make the Final Guess ----------
st.subheader("🕵️‍♂️ Make Your Final Guess")
final_guess = st.selectbox("Who is the culprit?", suspect_names, key="final_guess")

if st.button("🚔 Submit Arrest Warrant"):
    # The culprit is the suspect with Role "Culprit"
    culprit = next(s for s in st.session_state.suspects if s["Role"] == "Culprit")
    if final_guess == culprit["Name"]:
        st.success(f"🎉 You solved the case! {culprit['Name']} has been arrested.")
    else:
        st.error("❌ Wrong suspect! The real culprit is still at large. Re-examine the clues and interrogations.")

# ---------- Restart Game ----------
if st.button("🔄 New Case"):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.suspects = generate_suspects(st.session_state.selected_case)
    st.session_state.clue_index = 0
    st.experimental_rerun()
