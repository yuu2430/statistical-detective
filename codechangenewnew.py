import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from scipy import stats  # For confidence interval calculation

# Set page config must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Statistical Detective 🕵️‍♂️", page_icon="🕵️‍♂️")

# Check if Plotly is available
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly is not installed. Interactive visualizations will be disabled.")

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
    }
    .stMarkdown h1 {
        font-size: 2.5rem;
    }
    .stMarkdown h2 {
        font-size: 2rem;
    }
    .stMarkdown h3 {
        font-size: 1.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and Introduction
st.title("🕵️‍♂️ Statistical Detective")
st.markdown("**Use statistics and hints to analyze the data, interpret the probabilities, and catch the suspect!**")

# Game difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}

# Initialize session state for attempts, selected case, and game over state
if "attempts" not in st.session_state:
    st.session_state.attempts = difficulty_levels["Easy"]  # Default to Easy mode
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"  # Default to Easy mode
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "new_game" not in st.session_state:
    st.session_state.new_game = False

# Update difficulty and attempts if the user changes the difficulty level
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.new_game = True  # Reset game when difficulty changes

@st.cache_data  # Cache dataset to keep cases consistent
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 11):
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

# Generate the crime data
df = generate_crime_data()

# Display the data in a structured layout
st.subheader("📊 Crime Data Overview")
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
if "selected_case" not in st.session_state or st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

# Display hints and attempts
st.subheader("🔍 Hints and Attempts")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**📍 Location Analysis:** {selected_case['Cluster_Hint']}")
with col2:
    st.markdown(f"**🔄 Attempts Left:** {st.session_state.attempts}")

# Progress bar for attempts
st.progress(st.session_state.attempts / difficulty_levels[difficulty])

# Interactive visualization (if Plotly is available)
if PLOTLY_AVAILABLE:
    st.subheader("📈 Crime Patterns Visualization")
    fig = px.scatter(df, x="Location_Code", y="Time_Minutes", color="Cluster_Location", title="Crime Locations and Times")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Interactive visualizations are disabled because Plotly is not installed.")
    st.write("Here's a static table of the data:")
    st.dataframe(df[["Location", "Time", "Crime_Type", "Suspect_Age", "Suspect_Gender"]])

# Game interaction
st.subheader("🕵️‍♂️ Solve the Case")
with st.form("guess_form"):
    guessed_location = st.selectbox("Where did the crime occur?", list(location_map.keys()), key="crime_location")
    guessed_age = st.slider("What is the suspect's age?", 18, 50, key="suspect_age")
    guessed_gender = st.radio("What is the suspect's gender?", ["Male", "Female"], key="suspect_gender")
    guessed_gender = 0 if guessed_gender == "Male" else 1

    if st.form_submit_button("Submit Guess") and not st.session_state.game_over:
        st.session_state.attempts -= 1  # Decrement attempts before checking conditions

        correct_location = guessed_location == selected_case["Location"]
        correct_age = guessed_age == selected_case["Sus
