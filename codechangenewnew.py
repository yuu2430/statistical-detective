import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.cluster import KMeans

# Initialize Streamlit configuration
st.set_page_config(
    page_title="🔍 Statistical Detective",
    page_icon="🕵️",
    layout="wide"
)

# Custom CSS for styling (keep previous styles)
# ... [Same CSS as before] ...

# ---------------------------
# Improved Data Generation
# ---------------------------
def generate_realistic_crimes():
    locations = {
        "Manjalpur": {
            "time_range": (20, 4),  # 8 PM to 4 AM
            "common_crimes": ["Robbery", "Assault"],
            "common_weapons": ["Knife", "Gun"],
            "age_range": (18, 30)
        },
        "Fatehgunj": {
            "time_range": (9, 17),  # 9 AM to 5 PM
            "common_crimes": ["Fraud", "Pickpocketing"],
            "common_weapons": ["None"],
            "age_range": (25, 45)
        },
        "Gorwa": {
            "time_range": (18, 23),  # 6 PM to 11 PM
            "common_crimes": ["Burglary", "Vandalism"],
            "common_weapons": ["Crowbar", "None"],
            "age_range": (30, 50)
        }
    }
    
    data = []
    for _ in range(15):  # Larger dataset
        loc = random.choice(list(locations.keys()))
        pattern = locations[loc]
        
        # Generate time within location's common hours
        start_hour, end_hour = pattern["time_range"]
        hour = random.randint(start_hour, end_hour) % 24
        minute = random.randint(0, 59)
        
        data.append({
            "Time": f"{hour:02d}:{minute:02d}",
            "Location": loc,
            "Crime_Type": random.choice(pattern["common_crimes"]),
            "Suspect_Age": random.randint(*pattern["age_range"]),
            "Suspect_Gender": random.choices(["Male", "Female", "Other"], weights=[60, 35, 5])[0],
            "Weapon_Used": random.choices(pattern["common_weapons"] + ["None"], 
                                       weights=[70, 30])[0],
            "Time_Minutes": hour * 60 + minute
        })
    return pd.DataFrame(data)

# ---------------------------
# Game Logic
# ---------------------------
def main():
    st.title("🔍 Statistical Detective")
    st.write("### Crack the Case Through Statistical Patterns")

    # Initialize session state
    if "attempts" not in st.session_state:
        st.session_state.attempts = 3
    if "current_case" not in st.session_state:
        st.session_state.current_case = None
    if "hints" not in st.session_state:
        st.session_state.hints = []

    # Generate consistent crime data
    df = generate_realistic_crimes()
    
    # Select new case
    if st.session_state.current_case is None:
        case = df.sample(1).iloc[0]
        st.session_state.current_case = case
        st.session_state.hints = [
            f"🕒 Crime occurred between {case['Time']}",
            f"🔫 Common weapons in area: {', '.join(set(df[df['Location'] == case['Location']]['Weapon_Used'].unique()))}",
            f"👥 Typical suspect age range: {df[df['Location'] == case['Location']]['Suspect_Age'].mean()-5:.0f}-{df[df['Location'] == case['Location']]['Suspect_Age'].mean()+5:.0f}"
        ]

    case = st.session_state.current_case

    # Display case data
    st.header("📊 Crime Database")
    st.dataframe(df.drop(columns=["Time_Minutes"])

    # Investigation Section
    st.divider()
    st.header("🕵️ Investigation Panel")

    # Dynamic hints system
    with st.expander("🔍 Investigation Clues", expanded=True):
        for i, hint in enumerate(st.session_state.hints[:st.session_state.attempts+1]):
            st.write(hint)

    # Inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        loc_guess = st.selectbox("Crime Location", df['Location'].unique())
    with col2:
        age_guess = st.slider("Suspect Age", 18, 50, 30)
    with col3:
        gender_guess = st.radio("Suspect Gender", ["Male", "Female", "Other"])

    # Submit logic
    if st.button("Submit Findings"):
        st.session_state.attempts -= 1
        
        correct = [
            loc_guess == case["Location"],
            abs(age_guess - case["Suspect_Age"]) <= 5,
            gender_guess == case["Suspect_Gender"]
        ]

        if all(correct):
            st.success("🎉 Case Solved! You've identified the suspect!")
            st.balloons()
            st.session_state.current_case = None
            st.session_state.attempts = 3
            st.rerun()
        else:
            feedback = []
            if not correct[0]:
                feedback.append("Location mismatch")
            if not correct[1]:
                feedback.append("Age estimate off by >5 years")
            if not correct[2]:
                feedback.append("Gender incorrect")
                
            if st.session_state.attempts > 0:
                st.error(f"🚨 Issues: {', '.join(feedback)}. Try again!")
            else:
                st.error(f"❌ Case Closed. Correct answer: {case['Location']}, Age {case['Suspect_Age']}, {case['Suspect_Gender']}")
                st.session_state.current_case = None
                st.session_state.attempts = 3
                st.rerun()

if __name__ == "__main__":
    main()
