import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.cluster import KMeans
from scipy import stats  # For confidence interval calculation

# Initialize Streamlit configuration
st.set_page_config(
    page_title="🔍 Statistical Detective",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f0e6;
        color: #4f2022;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #9a816b !important;
        color: #ffffff !important;
        border-radius: 5px !important;
    }
    .stSlider div[data-testid="stThumbValue"] {
        color: #4f2022 !important;
    }
    .stSlider div[data-baseweb="slider"] {
        background-color: transparent;
    }
    .stRadio div[role="radiogroup"] {
        background-color: #ffffff !important;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #9a816b;
    }
    .stButton>button {
        background-color: #65b1df !important;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 10px 24px;
        border: 2px solid #4f2022;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4f2022 !important;
        transform: scale(1.05);
    }
    .stSuccess {
        background-color: #acdb01 !important;
        color: #4f2022 !important;
        border: 1px solid #9a816b;
    }
    .stError {
        background-color: #9a816b !important;
        color: #ffffff !important;
        border: 1px solid #4f2022;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for game instructions and status
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
    st.session_state.attempts = 3  # Default attempts
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "new_game" not in st.session_state:
    st.session_state.new_game = True
if "hints_revealed" not in st.session_state:
    st.session_state.hints_revealed = 0  # Track how many hints have been revealed

# Game title and storyline
st.title("🔍 Statistical Detective")
st.write("""
### 🕵️‍♂️ The Case of the Serial Suspect
The city is in chaos! A series of crimes have been reported, and the police need your help to catch the suspects. 
Use your statistical skills to analyze the data, interpret the clues, and identify the culprits. 
Can you solve the case before time runs out?
""")

# Difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
attempts_left = difficulty_levels[difficulty]

# Display score
st.sidebar.write(f"🎯 Score: {st.session_state.score}")

# Generate crime data
@st.cache_data
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    for _ in range(10):  # Generate 10 cases
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

# Display crime database
st.header("📊 Recent Crime Cases")
st.dataframe(
    df.drop(columns=["Time_Minutes"], errors="ignore"),
    use_container_width=True,
    height=(len(df) + 1) * 35 + 3  # Dynamic height based on rows
)

# Crime pattern detection
location_map = {"Manjalpur": 0, "Fatehgunj": 1, "Gorwa": 2, "Makarpura": 3}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1, "Other": 2})

# Use multiple features for clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code", "Time_Minutes"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

cluster_hints = {
    "High-Risk Zone A": "Data shows 70% of crimes here happen at night, often involving weapons.",
    "High-Risk Zone B": "Statistically, fraud and pickpocketing occur 60% of the time in this zone.",
    "High-Risk Zone C": "Burglary incidents make up 55% of crimes in this area, usually in the evenings."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)

# Select a case for the player
if st.session_state.selected_case is None or st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0  # Reset hints for new case

selected_case = st.session_state.selected_case

# Calculate the confidence interval for suspect age using bootstrapping
def bootstrap_confidence_interval(data, n_bootstrap=1000):
    bootstrap_means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_means.append(np.mean(sample))
    return np.percentile(bootstrap_means, [2.5, 97.5])

age_data = df['Suspect_Age']
ci_low, ci_high = bootstrap_confidence_interval(age_data)

# Investigation toolkit
st.divider()
st.header("🕵️ Investigation Toolkit")

# Always show investigation clues (no dropdown)
st.write(f"🔖 Probability suggests the suspect is likely between {int(ci_low)} and {int(ci_high)} years old (95% confidence).")
st.write(f"🔖 Location Analysis: {selected_case['Cluster_Hint']}")

# Gradual hints based on attempts
if st.session_state.hints_revealed >= 1:
    st.write(f"🔖 Crime Type: The crime type is {selected_case['Crime_Type']}.")
if st.session_state.hints_revealed >= 2:
    st.write(f"🔖 Weapon Used: The weapon used was {selected_case['Weapon_Used']}.")

# Investigation inputs
col1, col2, col3 = st.columns(3)
with col1:
    guessed_location = st.selectbox("Crime Location", list(location_map.keys()), key="crime_location")
with col2:
    guessed_age = st.slider("Suspect Age", 18, 50, 30, key="suspect_age")
with col3:
    guessed_gender = st.radio("Suspect Gender", ["Male", "Female", "Other"], key="suspect_gender")

guessed_gender = 0 if guessed_gender == "Male" else 1 if guessed_gender == "Female" else 2

# Submit investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Case Solved! You've identified the suspect! You win a sweet treat :)")
        st.balloons()
        st.session_state.score += 1  # Increase score
        st.session_state.new_game = True  # Reset the game after solving the case
    else:
        feedback = []
        if not correct_location:
            feedback.append(f"📍 Location doesn't match. Correct location: {selected_case['Location']}")
        if abs(guessed_age - selected_case["Suspect_Age"]) > 5:
            feedback.append(f"📈 Age estimate significantly off. Correct age: {selected_case['Suspect_Age']}")
        elif guessed_age != selected_case["Suspect_Age"]:
            feedback.append(f"📈 Age estimate close but not exact. Correct age: {selected_case['Suspect_Age']}")
        if guessed_gender != selected_case["Suspect_Gender"]:
            feedback.append(f"👤 Gender mismatch. Correct gender: {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female' if selected_case['Suspect_Gender'] == 1 else 'Other'}")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
            st.session_state.hints_revealed += 1  # Reveal more hints
        else:
            st.error(f"❌ Case Closed. Correct answer: {selected_case['Location']}, Age {selected_case['Suspect_Age']}, {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female' if selected_case['Suspect_Gender'] == 1 else 'Other'}")
            st.session_state.new_game = True  # Reset the game after running out of attempts

# Reset the game if new_game is True
if st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0  # Reset hints for new case
    st.rerun()

# Status bar
st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Attempts Left: {st.session_state.attempts}")

# New case button
if st.button("🔄 Start New Case"):
    st.session_state.new_game = True
    st.rerun()
