import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🕵️ The Ultimate Detective Challenge")
st.write("Analyze evidence, interrogate suspects, and uncover the truth!")

# ---------- Crime Data Generation ----------
crime_reports = [
    "A high-profile burglary at a luxury estate. No signs of forced entry.",
    "A missing person case where the victim was last seen at a cafe.",
    "An arson attack on a storage unit with confidential documents.",
]
locations = ["Downtown", "Suburbs", "Warehouse District", "Mall", "Train Station"]

@st.cache_data
def generate_case():
    crime_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
    return {
        "Crime_Report": random.choice(crime_reports),
        "Date": crime_date.strftime('%Y-%m-%d'),
        "Location": random.choice(locations),
        "Culprit": random.choice(["Alex", "Jordan", "Casey", "Morgan"]),
    }

if "case" not in st.session_state:
    st.session_state.case = generate_case()

case = st.session_state.case
st.subheader("📜 Case Details:")
st.write(f"{case['Crime_Report']}\n📅 Date: {case['Date']} | 📍 Location: {case['Location']}")

# ---------- Suspect Generation with Hidden Clues ----------
suspects = {
    "Alex": "A tech specialist with access to surveillance systems.",
    "Jordan": "A former detective with a history of rule-breaking.",
    "Casey": "A financial advisor with major gambling debts.",
    "Morgan": "An investigative journalist working on an exposé.",
}
culprit = case["Culprit"]

def generate_suspects():
    profiles = []
    for name, background in suspects.items():
        profiles.append({
            "Name": name,
            "Background": background,
            "Alibi": random.choice([
                "Claims to have been at home but no one can confirm.",
                "Says they were at a bar, but left alone midway.",
                "Mentions being with a friend, but the timelines don’t match.",
            ]) if name == culprit else random.choice([
                "A reliable witness confirms their whereabouts.",
                "Surveillance footage suggests they were elsewhere.",
                "Has a work-related timestamp proving their alibi.",
            ]),
        })
    return profiles

if "suspects" not in st.session_state:
    st.session_state.suspects = generate_suspects()

st.subheader("👥 Suspects")
for s in st.session_state.suspects:
    st.write(f"**{s['Name']}**: {s['Background']}\n_Alibi_: {s['Alibi']}")
    st.markdown("---")

# ---------- Evidence & Hidden Clues ----------
evidence = [
    {"title": "Phone Records", "detail": "One suspect made a call near the crime scene before midnight."},
    {"title": "Security Footage", "detail": "A car similar to one owned by a suspect was spotted nearby."},
    {"title": "Confidential Document", "detail": "A classified file was accessed using someone’s credentials."},
    {"title": "Witness Statement", "detail": "A witness claims to have seen someone wearing a red jacket leaving hurriedly."},
]

st.subheader("🔎 Evidence Board")
for item in evidence:
    with st.expander(item["title"]):
        st.write(item["detail"])

# ---------- Final Guess ----------
st.subheader("🕵️ Make Your Deduction")
guess = st.selectbox("Choose the suspect you believe is guilty:", [s["Name"] for s in st.session_state.suspects])
if st.button("🚔 Submit Your Guess"):
    if guess == culprit:
        st.success("🎉 Correct! You solved the case!")
    else:
        st.error("❌ Incorrect! The real culprit remains at large. Reevaluate the clues and suspects.")

if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.session_state.suspects = generate_suspects()
    st.experimental_rerun()
