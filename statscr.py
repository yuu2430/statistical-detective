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
st.write("A crime has been committed! Analyze clues, interrogate suspects, and solve the case. But beware—things are not always as they seem...")

# ---------- Crime Report Setup ----------
crime_reports = [
    "💎 A priceless artifact was stolen from the museum. Witnesses saw a figure escape into the night!",
    "🔥 A warehouse fire broke out under suspicious circumstances. Evidence suggests foul play.",
    "💰 A high-stakes poker game ended in a heist. One player never made it home.",
    "📞 A tech CEO was scammed out of millions. The cybercriminal left a cryptic digital footprint.",
]

# ---------- Generate Crime Data ----------
@st.cache_data
def generate_crime_data():
    locations = ["Museum", "Warehouse District", "Casino", "Tech Park", "City Square"]
    suspects = ["John", "Sarah", "Mike", "Emma", "David"]
    weapons = ["Crowbar", "Molotov", "Fake ID", "Hacking Device", "None"]
    
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    
    for i in range(1, 6):
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time = f"{random.randint(0, 23)}:{random.randint(0, 59):02d}"
        
        data.append({
            "Case_ID": i,
            "Crime_Report": random.choice(crime_reports),
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": crime_time,
            "Location": random.choice(locations),
            "Suspect_Name": random.choice(suspects),
            "Weapon_Used": random.choice(weapons),
            "Outcome": random.choice(["Unsolved", "Solved"]),
        })
    
    return pd.DataFrame(data)

df = generate_crime_data()

# ---------- Select a Random Case ----------
if "selected_case" not in st.session_state:
    st.session_state.selected_case = df.sample(1).iloc[0]
selected_case = st.session_state.selected_case

st.subheader("📜 Crime Report:")
st.write(f"**{selected_case['Crime_Report']}**")
st.write(f"📅 **Date:** {selected_case['Date']} | ⏰ **Time:** {selected_case['Time']} | 📍 **Location:** {selected_case['Location']}")

# ---------- Suspect Profiles ----------
def generate_suspects(case):
    background_info = {
        "John": "A disgruntled ex-employee of the museum, fired last month.",
        "Sarah": "An aspiring journalist investigating corporate fraud.",
        "Mike": "A gambler with a history of rigging games.",
        "Emma": "A digital security expert—who may have gone rogue.",
        "David": "A night janitor who works in the crime location."
    }
    alibis = {
        "John": "Claims to have been at a bar all night, but no receipts were found.",
        "Sarah": "Says she was writing an article at home, alone.",
        "Mike": "Insists he was in another casino across town.",
        "Emma": "Claims she was fixing a security breach remotely.",
        "David": "Was seen leaving work early but denies any wrongdoing."
    }
    
    culprit_name = case["Suspect_Name"]
    all_names = list(background_info.keys())
    decoy_names = [name for name in all_names if name != culprit_name]
    random.shuffle(decoy_names)
    
    suspects = [{
        "Name": culprit_name,
        "Role": "Culprit",
        "Background": background_info.get(culprit_name, "No background available."),
        "Alibi": alibis.get(culprit_name, "No alibi provided."),
    }]
    
    for name in decoy_names[:2]:
        suspects.append({
            "Name": name,
            "Role": "Decoy",
            "Background": background_info.get(name, "No background available."),
            "Alibi": alibis.get(name, "No alibi provided."),
        })
    
    return suspects

if "suspects" not in st.session_state:
    st.session_state.suspects = generate_suspects(selected_case)

st.subheader("👥 Suspect Profiles")
for suspect in st.session_state.suspects:
    st.write(f"**{suspect['Name']}**")
    st.write(f"_Background_: {suspect['Background']}")
    st.write(f"_Alibi_: {suspect['Alibi']}")
    st.markdown("---")

# ---------- Interrogation ----------
st.subheader("🗣️ Interrogate a Suspect")
selected_suspect_name = st.selectbox("Select a suspect to interrogate:", [s["Name"] for s in st.session_state.suspects])
selected_suspect = next(s for s in st.session_state.suspects if s["Name"] == selected_suspect_name)

questions = ["Where were you last night?", "Do you know the victim?", "What were you doing at the crime scene?"]
selected_question = st.selectbox("Choose a question:", questions)

responses = {
    "Where were you last night?": {
        "Culprit": "I was home, but I might have stepped out briefly...",
        "Decoy": "I was at home all night, no one can dispute that."
    },
    "Do you know the victim?": {
        "Culprit": "We’ve met a few times, but that’s all.",
        "Decoy": "We worked together before. I had no issues with them."
    },
    "What were you doing at the crime scene?": {
        "Culprit": "I had business nearby, that’s just a coincidence.",
        "Decoy": "I wasn’t anywhere near that place."
    }
}

if st.button("🎙️ Ask Question"):
    role = selected_suspect["Role"]
    st.write(f"🕵️ {selected_suspect['Name']} answers: {responses[selected_question][role]}")

# ---------- Final Guess ----------
st.subheader("🕵️‍♂️ Make Your Final Guess")
final_guess = st.selectbox("Who is the culprit?", [s["Name"] for s in st.session_state.suspects])
if st.button("🚔 Submit Arrest Warrant"):
    if final_guess == selected_case["Suspect_Name"]:
        st.success(f"🎉 You solved the case! {final_guess} has been arrested.")
    else:
        st.error(f"❌ Wrong suspect! The real culprit was {selected_case['Suspect_Name']}. Try again!")
