import os 
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

os.environ["OMP_NUM_THREADS"] = "1"

st.set_page_config(layout="wide")

st.title("🔎 Statistical Detective: AI to the Rescue")
st.write("Analyze the clues, consider the AI's patterns, and solve the mystery!")

@st.cache_data
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):
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

location_map = {"Downtown": 0, "City Park": 1, "Suburbs": 2, "Industrial Area": 3, "Mall": 4}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

cluster_hints = {
    "High-Risk Zone A": "Activity in this area tends to peak under the cover of darkness.",
    "High-Risk Zone B": "Incidents here tend to involve swift, discreet acts during the daytime.",
    "High-Risk Zone C": "Patterns suggest a preference for quieter residential zones."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)
st.write("AI-Detected Crime Hotspots:")
st.dataframe(df[['Case_ID', 'Location', 'Time', 'Cluster_Location', 'Cluster_Hint']], use_container_width=True)

if "selected_case" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

st.write("🔎 AI Predictions:")
st.write("🕵️ Observations suggest the suspect falls within a particular age range.")
st.write("⏰ Timing patterns indicate a certain period when the incident likely occurred.")
st.write("📍 Location patterns suggest an area where similar cases have happened before.")
st.write("🧐 Witness accounts imply a general description of the suspect.")

guessed_location = st.selectbox("Select Crime Location", list(location_map.keys()), key="crime_location")
guessed_age = st.slider("Guess Suspect Age", 18, 50, key="suspect_age")
guessed_gender = st.radio("Guess Suspect Gender", ["Male", "Female"], key="suspect_gender")
guessed_gender = 0 if guessed_gender == "Male" else 1

if st.button("Submit Guess", key="submit_guess"):
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Your deductions were spot on! Case solved!")
    else:
        hints = []
        if not correct_location:
            hints.append("The location doesn’t match the patterns observed.")
        if not correct_age:
            hints.append("Age estimate might need reconsideration.")
        if not correct_gender:
            hints.append("Witness descriptions suggest a different gender.")
        
        st.warning("Not quite there! Consider the following observations:")
        for hint in hints:
            st.write(f"- {hint}")
        
        st.write("🔍 Take another look at the case details and try again!")

if st.button("🔄 New Game"):
    st.session_state.new_game = True
    st.rerun()
