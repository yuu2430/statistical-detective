import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

os.environ["OMP_NUM_THREADS"] = "1"

st.set_page_config(layout="wide")  # Adjust layout to wide for better readability

st.markdown("""
    <style>
        body {
            background-color: #2c2f33;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #7289da;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stSelectbox, .stSlider, .stRadio {
            color: white;
        }
        .main {
            background-color: #23272a;
            border-radius: 15px;
            padding: 20px;
        }
        .stDataFrame {
            width: 80% !important;
        }
        .highlight {
            background-color: #ffcccb;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Statistical Detective: AI to the Rescue")
st.write("Solve the crime mystery using AI and statistical models! Use the hints and predictions to crack the case!")

@st.cache_data  # Cache the dataset so it doesn't change every interaction
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):  # 20 crime cases
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
    "High-Risk Zone A": "Frequent night-time crimes, often involve armed suspects.",
    "High-Risk Zone B": "Daylight crimes, usually fraud or pickpocketing.",
    "High-Risk Zone C": "Suburban area, burglary cases more common."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)
st.write("AI-Detected Crime Hotspots:")
st.dataframe(df[['Case_ID', 'Location', 'Time', 'Cluster_Location', 'Cluster_Hint']], use_container_width=True)

# AI Prediction Hints
model = DecisionTreeClassifier()
model.fit(df[["Location_Code", "Suspect_Gender"]], df["Crime_Type"])
df["Predicted_Crime"] = model.predict(df[["Location_Code", "Suspect_Gender"]])
st.write("🔮 AI Prediction Hints:")
st.dataframe(df[['Case_ID', 'Predicted_Crime']], use_container_width=True)

difficulty = st.radio("Select Difficulty Level", ["Easy", "Hard", "Expert"], key="difficulty_level")
attempts = 3 if difficulty == "Easy" else 2 if difficulty == "Hard" else 1
score = 0

guessed_location = st.selectbox("Select Crime Location", list(location_map.keys()), key="crime_location")
guessed_age = st.slider("Guess Suspect Age", 18, 50, key="suspect_age")
guessed_gender = st.radio("Guess Suspect Gender", ["Male", "Female"], key="suspect_gender")
guessed_gender = 0 if guessed_gender == "Male" else 1

selected_case = df.sample(1).iloc[0]
correct_location = selected_case["Location"]
correct_age = selected_case["Suspect_Age"]
correct_gender = selected_case["Suspect_Gender"]

if st.button("Submit Guess", key="submit_guess"):
    if guessed_location == correct_location and guessed_age == correct_age and guessed_gender == correct_gender:
        st.success("🎉 Correct! You've solved the case.")
        score += 100
    else:
        attempts -= 1
        if attempts > 0:
            st.warning(f"❌ Wrong guess! You have {attempts} attempts left.")
        else:
            st.error(f"💀 Game Over! The case remains unsolved.")
            df.loc[df['Location'] == correct_location, 'Location'] = f'**{correct_location}**'
            st.dataframe(df, use_container_width=True)
            st.write(f"🕵️ The correct answer was: Location - {correct_location}, Age - {correct_age}, Gender - {'Male' if correct_gender == 0 else 'Female'}.")
            if st.button("New Game", key="new_game"):
                st.experimental_rerun()

st.write(f"🏆 Your final score: {score}")
