import os 
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from scipy import stats  # For confidence interval calculation

# Set page configuration first
st.set_page_config(layout="wide")  # Wide layout for better display

# Debug: Ensure Streamlit is properly imported
try:
    print(f"Streamlit version: {st.__version__}")
except NameError:
    st.error("Streamlit is not properly imported. Please ensure you're running this script with `streamlit run`.")
    st.stop()

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

st.title("\U0001F50E Statistical Detective")
st.write("Use statistics and hints! Analyze the data, interpret the probabilities, and catch the suspect!")

# Game difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")

# Initialize attempts in session state
if "attempts" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.attempts = difficulty_levels[difficulty]

@st.cache_data  # Cache dataset to keep cases consistent
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 11):  # Generate 20 cases
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        data.append({
            "Case_ID": i,
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
            "Time_Minutes": crime_time_minutes
        })
    return pd.DataFrame(data)

df = generate_crime_data()
st.dataframe(df.drop(columns=["Time_Minutes"], errors="ignore"), use_container_width=True)

# Crime pattern detection
location_map = {"Manjalpur": 0, "Fatehgunj": 1, "Gorwa": 2, "Makarpura": 3}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

cluster_hints = {
    "High-Risk Zone A": "Data shows 70% of crimes here happen at night, often involving weapons.",
    "High-Risk Zone B": "Statistically, fraud and pickpocketing occur 60% of the time in this zone.",
    "High-Risk Zone C": "Burglary incidents make up 55% of crimes in this area, usually in the evenings."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)

# Select a case for the player
if "selected_case" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

# Calculate the confidence interval for suspect age
age_group = selected_case['Suspect_Age'] // 10 * 10
age_data = df['Suspect_Age']
age_count = age_data[(age_data // 10 * 10) == age_group].count()
total_cases = len(age_data)

# Proportion of suspects in the same age group
proportion = age_count / total_cases

# 95% confidence interval for proportion
ci_low, ci_high = stats.norm.interval(0.95, loc=proportion, scale=np.sqrt(proportion * (1 - proportion) / total_cases))

# Convert confidence interval into percentage
confidence_percent_low = int(ci_low * 100)
confidence_percent_high = int(ci_high * 100)

st.write("\U0001F4CA Hints:")
st.write(f"\U0001F575 Probability suggests the suspect is likely in their {age_group}s.")
st.write(f"\U0001F4CD Location Analysis: {selected_case['Cluster_Hint']}")

st.write(f"🔢 Attempts left: {st.session_state.attempts}")

# Create columns for horizontal layout
col1, col2, col3 = st.columns(3)

# Place each widget in its respective column
with col1:
    guessed_location = st.selectbox("Where did the crime occur?", list(location_map.keys()), key="crime_location")

with col2:
    guessed_age = st.slider("What is the suspect's age?", 18, 50, key="suspect_age")

with col3:
    guessed_gender = st.radio("What is the suspect's gender?", ["Male", "Female"], key="suspect_gender")
    guessed_gender = 0 if guessed_gender == "Male" else 1

# Submit button (only one instance)
if st.button("Submit Guess", key="submit_guess"):
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success(f"\U0001F389 Correct! You've solved the case. Reward: You win a sweet treat! yay!")
        st.balloons()  # Show balloons for correct answer
    else:
        st.session_state.attempts -= 1
        feedback = []
        if not correct_location:
            feedback.append("The location probability suggests another area...")
        if not correct_age:
            feedback.append("The age probability doesn't align with the data...")
        if not correct_gender:
            feedback.append("Gender statistics indicate a different suspect...")
        
        if st.session_state.attempts > 0:
            st.error("\U0001F480 Not quite! " + " ".join(feedback) + f" Attempts left: {st.session_state.attempts}")
        else:
            st.error("\U0001F480 No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"\U0001F575 Age: {selected_case['Suspect_Age']}")
            st.write(f"👤 Gender: {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female'}")

# New Game button
if st.button("🔄 New Game"):
    st.session_state.new_game = True
    st.session_state.attempts = difficulty_levels[difficulty]
    st.cache_data.clear()  # Clear previous dataset to generate new random crime cases
    st.rerun()
