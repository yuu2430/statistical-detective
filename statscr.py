import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🕵️ Ultimate Detective Challenge")
st.write("Analyze clues, interrogate suspects, and solve a crime where deception is key!")

# ---------- Crime Report Setup ----------
crime_reports = [
    "A rare artifact was stolen from the museum. The thief knew exactly what to take.",
    "A high-profile scientist was poisoned at a conference. The suspect was among the attendees.",
    "A CEO was found unconscious in his office. The security footage is missing a critical hour.",
    "A journalist investigating corporate fraud disappeared. A cryptic note was found at the scene.",
]

# ---------- Generate Crime Data ----------
@st.cache_data
def generate_crime_data():
    locations = ["Museum", "Conference Hall", "Corporate Office", "Park"]
    suspects = ["Alice", "Bob", "Charlie", "Dana", "Ethan"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)

    for i in range(5):
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time = f"{random.randint(10, 23)}:{random.randint(0, 59):02d}"

        data.append({
            "Case_ID": i + 1,
            "Crime_Report": random.choice(crime_reports),
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": crime_time,
            "Location": random.choice(locations),
            "Suspect_Name": random.choice(suspects),
            "Motive": random.choice(["Revenge", "Financial Gain", "Accidental", "Framed"]),
            "Lies": random.choice([True, False]),  # Some suspects will lie!
        })
    return pd.DataFrame(data)

df = generate_crime_data()

# ---------- Select a Random Case ----------
if "selected_case" not in st.session_state:
    st.session_state.selected_case = df.sample(1).iloc[0]
selected_case = st.session_state.selected_case

st.subheader("📜 Crime Report:")
st.write(selected_case["Crime_Report"])
st.write(f"📅 Date: {selected_case['Date']} | ⏰ Time: {selected_case['Time']} | 📍 Location: {selected_case['Location']}")

# ---------- Enriched Suspect Profiles ----------
def generate_suspects(case):
    all_suspects = ["Alice", "Bob", "Charlie", "Dana", "Ethan"]
    culprit_name = case["Suspect_Name"]
    random.shuffle(all_suspects)
    
    suspects = []
    for name in all_suspects[:3]:
        is_culprit = name == culprit_name
        suspects.append({
            "Name": name,
            "Motive": "Unknown" if not is_culprit else case["Motive"],
            "Alibi": "Unconfirmed",  # Will be revealed in interrogation
            "Lying": case["Lies"] if is_culprit else random.choice([True, False]),
        })
    return suspects

if "suspects" not in st.session_state:
    st.session_state.suspects = generate_suspects(selected_case)

st.subheader("👥 Suspects")
for suspect in st.session_state.suspects:
    st.write(f"**{suspect['Name']}** - Motive: {suspect['Motive']}")
    st.markdown("---")

# ---------- Evidence Board ----------
st.subheader("🔎 Evidence Board")
evidence_items = [
    {"title": "Security Footage", "detail": "Partially corrupted. A shadowy figure seen leaving at the time of the crime."},
    {"title": "Fingerprint Analysis", "detail": "Two sets of prints found, but one is smudged."},
    {"title": "Suspicious Transaction", "detail": "A large sum of money was withdrawn by a suspect before the crime."},
    {"title": "Witness Statement", "detail": "A person in a dark hoodie was seen rushing out, but the witness isn't certain."},
]
random.shuffle(evidence_items)
for item in evidence_items:
    with st.expander(item["title"]):
        st.write(item["detail"])

# ---------- Interrogation ----------
st.subheader("🗣️ Interrogate Suspects")
suspect_names = [s["Name"] for s in st.session_state.suspects]
selected_suspect_name = st.selectbox("Choose a suspect to interrogate:", suspect_names, key="suspect_select")
selected_suspect = next(s for s in st.session_state.suspects if s["Name"] == selected_suspect_name)

questions = ["Where were you?", "Did you know the victim?", "Why were you seen near the crime scene?"]
selected_question = st.selectbox("Choose a question:", questions, key="question_select")

if st.button("🎙️ Ask Question"):
    if selected_suspect["Lying"]:
        st.write(f"🕵️ {selected_suspect['Name']} hesitates: 'Uh, I was just passing by, I guess...' 😬")
    else:
        st.write(f"🕵️ {selected_suspect['Name']} confidently replies: 'I was home all night, my roommate can confirm.' 😊")

# ---------- Make the Final Guess ----------
st.subheader("🚔 Make Your Arrest")
final_guess = st.selectbox("Who is the culprit?", suspect_names, key="final_guess")
if st.button("Submit Arrest Warrant"):
    if final_guess == selected_case["Suspect_Name"]:
        st.success("🎉 You solved the case! The suspect was guilty.")
    else:
        st.error("❌ Wrong suspect! The real culprit escapes.")

# ---------- Restart Game ----------
if st.button("🔄 New Case"):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.suspects = generate_suspects(st.session_state.selected_case)
    st.experimental_rerun()
