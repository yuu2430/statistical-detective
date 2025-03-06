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
st.write("Analyze clues, interrogate suspects, and piece together the mystery. Not everything is as it seems...")

# ---------- Crime Report Setup ----------
crime_reports = [
    "🔍 A robbery was reported at a mall. The suspect was last seen near the food court.",
    "🔥 A mysterious arson case occurred in an industrial area at midnight. Witnesses reported a shadowy figure.",
    "💰 A burglary took place in the suburbs. The suspect fled on foot before police arrived.",
    "📞 A fraud case was reported downtown. The victim lost thousands due to an online scam.",
]

# ---------- Generate Crime Data ----------
@st.cache_data
def generate_crime_data():
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    data = []
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    
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
            "Suspect_Name": random.choice(["John", "Sarah", "Mike", "Emma", "David"]),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
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

# ---------- Interactive Evidence Board with Probability Hints ----------
st.subheader("🔎 Evidence Board")
evidence_items = [
    {"title": "Fingerprint Analysis", "detail": f"Fingerprints found at the scene match one suspect with {random.randint(50, 90)}% probability."},
    {"title": "DNA Sample", "detail": f"DNA traces suggest a {random.randint(40, 85)}% match to one of the suspects."},
    {"title": "CCTV Footage", "detail": f"The figure in the footage has a {random.randint(30, 75)}% resemblance to a suspect."},
    {"title": "Time-stamped Call", "detail": f"A call made near the crime scene suggests a {random.randint(20, 70)}% chance of being linked to a suspect."},
    {"title": "Forensic Report", "detail": f"Unusual chemical traces were found, with a {random.randint(45, 80)}% probability of belonging to someone working in the area."},
]

random.shuffle(evidence_items)
for item in evidence_items:
    with st.expander(item["title"]):
        st.write(item["detail"])

# ---------- Restart Game ----------
if st.button("🔄 New Case"):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.experimental_rerun()
