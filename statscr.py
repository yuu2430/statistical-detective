import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🔍 Mystery Solver: Logical Deduction Challenge")
st.write("Analyze subtle patterns and hidden connections. One clear truth emerges from multiple lies...")

# ---------- Crime Data Generation ----------
crime_types = {
    "Mall Robbery": {"location": "Mall", "time": "evening", "weapon": "crowbar"},
    "Factory Arson": {"location": "Industrial Area", "time": "night", "weapon": "lighter"},
    "Suburban Burglary": {"location": "Suburbs", "time": "afternoon", "weapon": "screwdriver"}
}

@st.cache_data
def generate_case():
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {
        "evening": "6:00 PM - 8:00 PM",
        "night": "10:00 PM - 12:00 AM",
        "afternoon": "2:00 PM - 4:00 PM"
    }
    
    suspects = {
        "Alex": {"occupation": "Security Guard", "connection": "Works at crime scene"},
        "Sam": {"occupation": "Electrician", "connection": "Recently fired from site"},
        "Jordan": {"occupation": "Delivery Driver", "connection": "Regular route nearby"},
        "Taylor": {"occupation": "Janitor", "connection": "Night shift worker"},
        "Casey": {"occupation": "Shop Owner", "connection": "Financial troubles"}
    }
    
    culprit = random.choice(list(suspects.keys()))
    
    # Create subtle evidence patterns
    evidence = {
        "Security Footage": f"Blurry figure wearing {random.choice(['red', 'blue', 'black'])} jacket",
        "Tool Markings": f"Matches {details['weapon']} found in {random.choice(['parking lot', 'storage room'])}",
        "Witness Account": f"Noticed someone with {random.choice(['backpack', 'toolbox'])} near scene",
        "Digital Records": f"Unauthorized access during {details['time']} hours"
    }
    
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": time_window[details["time"]],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence
    }

if "case" not in st.session_state:
    st.session_state.case = generate_case()

case = st.session_state.case

# ---------- Game Interface ----------
st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")

# ---------- Evidence Board ----------
st.subheader("🔎 Compromised Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Could match multiple suspects)")

# ---------- Suspect Profiles ----------
st.subheader("👥 Persons of Interest")
for name, info in case["suspects"].items():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(f"https://i.pravatar.cc/150?img={random.randint(1,70)}", width=100)
    with col2:
        st.write(f"### {name}")
        st.write(f"**Occupation**: {info['occupation']}")
        st.write(f"**Connection**: {info['connection']}")
        st.write(f"**Alibi**: {random.choice([
            'Was alone during the incident',
            'Claims to be running errands',
            'Says they were helping a friend',
            'Mentions being stuck in traffic'
        ])}")
    st.markdown("---")

# ---------- Deduction Mechanics ----------
st.subheader("🕵️ Logical Analysis")

# Hidden connection system
occupation_weapon = {
    "Security Guard": "crowbar",
    "Electrician": "screwdriver",
    "Delivery Driver": "crowbar",
    "Janitor": "lighter",
    "Shop Owner": "screwdriver"
}

time_consistency = {
    "evening": ["Security Guard", "Shop Owner"],
    "night": ["Janitor", "Electrician"],
    "afternoon": ["Delivery Driver", "Shop Owner"]
}

# ---------- Solution Check ----------
user_guess = st.selectbox("Select the culprit:", list(case["suspects"].keys()))
if st.button("🔒 Submit Final Answer"):
    correct = user_guess == case["true_culprit"]
    
    # Verify logical consistency
    occupation_match = occupation_weapon[case["suspects"][case["true_culprit"]]["occupation"]] == case["crime_types"][case["crime"]]["weapon"]
    time_match = case["suspects"][case["true_culprit"]]["occupation"] in time_consistency[case["crime"].split()[-1].lower()]]
    
    if correct and occupation_match and time_match:
        st.success("🎉 Perfect deduction! You identified the hidden patterns!")
        st.balloons()
    elif correct:
        st.warning("✅ Correct suspect, but did you catch the full pattern? (Occupation + Time + Weapon)")
    else:
        st.error("❌ Incorrect. The truth hides in: Occupation-Weapon match + Typical schedule")

# ---------- Restart ----------
if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.experimental_rerun()
