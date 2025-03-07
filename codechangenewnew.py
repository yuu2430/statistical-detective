import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.cluster import KMeans

# Initialize Streamlit
st.set_page_config(
    page_title="🔍 Statistical Detective",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Sidebar instructions
st.sidebar.header("How to Play")
st.sidebar.write("""
1. Select a difficulty level.
2. Analyze the crime data and use the hints provided.
3. Guess the suspect's location, age, and gender.
4. Submit your findings and see if you're correct!
5. You have a limited number of attempts. Use them wisely!
""")

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 3
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "hints_revealed" not in st.session_state:
    st.session_state.hints_revealed = 0
if "new_game" not in st.session_state:
    st.session_state.new_game = True

# Generate consistent crime data
@st.cache_data
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson", "Pickpocketing", "Vandalism"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    for _ in range(10):
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        data.append({
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female", "Other"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
            "Time_Minutes": crime_time_minutes
        })
    return pd.DataFrame(data)

df = generate_crime_data()

# Ensure a fixed case for the game session
if st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.attempts = 3
    st.session_state.hints_revealed = 0
    st.session_state.new_game = False
selected_case = st.session_state.selected_case

# Clustering for location analysis
location_map = {"Manjalpur": 0, "Fatehgunj": 1, "Gorwa": 2, "Makarpura": 3}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1, "Other": 2})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code", "Time_Minutes"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

# Crime hints based on actual data
cluster_hints = {
    "High-Risk Zone A": "Most incidents here involve property damage or theft.",
    "High-Risk Zone B": "Fraud and cyber-related crimes are frequent in this area.",
    "High-Risk Zone C": "Violent crimes occur more often, particularly at night."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)

# Display investigation hints
st.header("🕵️ Investigation Toolkit")
st.write(f"🔖 The suspect is likely between {selected_case['Suspect_Age'] - 5} and {selected_case['Suspect_Age'] + 5} years old.")
st.write(f"🔖 Location Analysis: {selected_case['Cluster_Hint']}")
if st.session_state.hints_revealed >= 1:
    st.write(f"🔖 Crime Type Hint: {selected_case['Crime_Type']} was committed.")
if st.session_state.hints_revealed >= 2:
    st.write(f"🔖 Weapon Used: The suspect used a {selected_case['Weapon_Used']}.")

# Investigation inputs
col1, col2, col3 = st.columns(3)
with col1:
    guessed_location = st.selectbox("Crime Location", list(location_map.keys()), key="crime_location")
with col2:
    guessed_age = st.slider("Suspect Age", 18, 50, 30, key="suspect_age")
with col3:
    guessed_gender = st.radio("Suspect Gender", ["Male", "Female", "Other"], key="suspect_gender")

guessed_gender = {"Male": 0, "Female": 1, "Other": 2}[guessed_gender]

# Submit Investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Case Solved! You win!")
        st.balloons()
        st.session_state.score += 1
        st.session_state.new_game = True
    else:
        feedback = []
        if not correct_location:
            feedback.append(f"📍 Incorrect location. The crime was in {selected_case['Location']}.")
        if abs(guessed_age - selected_case["Suspect_Age"]) > 5:
            feedback.append(f"📈 Age estimate significantly off. Correct age: {selected_case['Suspect_Age']}.")
        elif guessed_age != selected_case["Suspect_Age"]:
            feedback.append(f"📈 Age estimate close but not exact. Correct age: {selected_case['Suspect_Age']}.")
        if guessed_gender != selected_case["Suspect_Gender"]:
            feedback.append(f"👤 Gender mismatch. Correct gender: {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female' if selected_case['Suspect_Gender'] == 1 else 'Other'}.")
        
        if st.session_state.attempts > 0:
            st.error("🚨 " + " • ".join(feedback))
            st.session_state.hints_revealed += 1
        else:
            st.error(f"❌ Case Closed. Correct answer: {selected_case['Location']}, Age {selected_case['Suspect_Age']}, {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female' if selected_case['Suspect_Gender'] == 1 else 'Other'}.")
            st.session_state.new_game = True

if st.button("🔄 Start New Case"):
    st.session_state.new_game = True
    st.rerun()
