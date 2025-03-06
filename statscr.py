import os
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🕵️ Crack the Mystery")
st.write("Find the real culprit by analyzing evidence and interrogating suspects!")

# ---------- Crime Data ----------
crime_reports = [
    "A robbery at a mall. Suspect seen near the food court.",
    "An arson case occurred in an industrial area at midnight.",
    "A burglary in the suburbs. Suspect fled before police arrived.",
]
locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]

@st.cache_data
def generate_case():
    crime_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
    return {
        "Crime_Report": random.choice(crime_reports),
        "Date": crime_date.strftime('%Y-%m-%d'),
        "Location": random.choice(locations),
        "Culprit": random.choice(["John", "Sarah", "Mike"]),
    }

if "case" not in st.session_state:
    st.session_state.case = generate_case()

case = st.session_state.case
st.subheader("📜 Crime Report:")
st.write(f"{case['Crime_Report']}\n📅 Date: {case['Date']} | 📍 Location: {case['Location']}")

# ---------- Suspect Generation ----------
suspects = {"John": "Security guard, fired recently.", "Sarah": "Owes money, desperate.", "Mike": "Recently fired, struggling."}
culprit = case["Culprit"]

def generate_suspects():
    profiles = []
    for name, background in suspects.items():
        profiles.append({
            "Name": name,
            "Background": background,
            "Alibi": random.choice([
                "Claims to have been home alone.",
                "Says they were out but no proof.",
                "A friend vouches, but timeline is off.",
            ]) if name == culprit else "A solid alibi, but is it true?",
        })
    return profiles

if "suspects" not in st.session_state:
    st.session_state.suspects = generate_suspects()

st.subheader("👥 Suspects")
for s in st.session_state.suspects:
    st.write(f"**{s['Name']}**: {s['Background']}\n_Alibi_: {s['Alibi']}")
    st.markdown("---")

# ---------- Evidence & Puzzle ----------
evidence = [
    {"title": "DNA Report", "detail": "Traces found but inconclusive."},
    {"title": "CCTV Footage", "detail": "Blurred figure seen leaving."},
    {"title": "Mysterious Note", "detail": "Contains scrambled text: *EHT PLIURCT SI HOJN*"},
]

st.subheader("🔎 Evidence Board")
for item in evidence:
    with st.expander(item["title"]):
        st.write(item["detail"])

# ---------- Final Guess ----------
st.subheader("🕵️ Who is the Culprit?")
guess = st.selectbox("Choose your suspect:", [s["Name"] for s in st.session_state.suspects])
if st.button("🚔 Submit Your Guess"):
    if guess == culprit:
        st.success("🎉 You solved the case!")
    else:
        st.error("❌ Wrong suspect! Try again.")

if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.session_state.suspects = generate_suspects()
    st.experimental_rerun()
