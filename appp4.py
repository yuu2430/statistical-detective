import os 
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

os.environ["OMP_NUM_THREADS"] = "1"

st.set_page_config(layout="wide")  # Wide layout for better display

st.title("🔎 Statistical Detective: AI to the Rescue")
st.write("Use statistics and AI to solve crime mysteries! Analyze the data, interpret the probabilities, and catch the suspect!")

# Game difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
attempts_left = difficulty_levels[difficulty]
if "attempts" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.attempts = attempts_left

@st.cache_data  # Cache dataset to keep cases consistent
def generate_crime_data():
    crime_types = ["Violent Crimes", "Property Crimes", "Financial Crimes", "Drug-Related Crimes"]
    locations = ["Gorwa", "Manjalpur", "Makarpura", "Fatehgunj"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):  # Generate 20 cases
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
location_map = {"Gorwa": 0, "Manjalpur": 1, "Makarpura": 2, "Fatehgunj": 3}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

cluster_hints = {
    "High-Risk Zone A": "Data shows 70% of violent crimes here happen at night, often involving weapons.",
    "High-Risk Zone B": "Statistically, financial crimes and fraud occur 60% of the time in this zone.",
    "High-Risk Zone C": "Property crimes make up 55% of crimes in this area, usually in the evenings."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)
st.write("📊 AI-Detected Crime Hotspots:")
st.dataframe(df[['Case_ID', 'Location', 'Time', 'Cluster_Location', 'Cluster_Hint']], use_container_width=True)
