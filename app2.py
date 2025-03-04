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
            background-color: #5c3038;
            color: #cccccc;
        }
        .stButton>button {
            background-color: #d25b5b;
            color: white;
            border-radius: 10px;
        }
        .stSelectbox, .stSlider, .stRadio {
            color: white;
        }
        .main {
            background-color: #640404;
            border-radius: 15px;
            padding: 20px;
        }
        .stDataFrame {
            width: 70% !important;  /* Ensure dataset table takes up 70% of the window */
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Statistical Detective: AI to the Rescue")
st.write("Solve the crime mystery using AI and statistical models!")

def time_to_minutes(time_str):
    dt = datetime.strptime(time_str, "%I:%M %p")
    return dt.hour * 60 + dt.minute

def minutes_to_time(minutes):
    return datetime.strptime(f"{minutes // 60}:{minutes % 60}", "%H:%M").strftime("%I:%M %p")

@st.cache_data  # Cache the dataset so it doesn't change every interaction
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):  # 20 crime cases
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time = random.randint(0, 23)
        formatted_time = datetime.strptime(str(crime_time), "%H").strftime("%I:%M %p")
        data.append({
            "Case_ID": i,
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": formatted_time,
            "Time_Minutes": time_to_minutes(formatted_time),
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"])
        })
    return pd.DataFrame(data)

df = generate_crime_data()
st.dataframe(df, use_container_width=True)

location_map = {"Downtown": 0, "City Park": 1, "Suburbs": 2, "Industrial Area": 3, "Mall": 4}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code", "Time_Minutes"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

cluster_hints = {
    "High-Risk Zone A": "Frequent night-time crimes, often involve armed suspects.",
    "High-Risk Zone B": "Daylight crimes, usually fraud or pickpocketing.",
    "High-Risk Zone C": "Suburban area, burglary cases more common."
}

df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)
st.write("AI-Detected Crime Hotspots:")
st.dataframe(df[['Case_ID', 'Location', 'Time', 'Cluster_Location', 'Cluster_Hint']], use_container_width=True)

reg = LinearRegression()
reg.fit(df[["Time_Minutes"]], df[["Location_Code"]])
next_crime_minutes = reg.predict(pd.DataFrame([[time_to_minutes("12:00 PM")]], columns=["Time_Minutes"]))
next_crime_time = minutes_to_time(max(0, min(1439, int(next_crime_minutes[0][0]))))
st.write(f"AI Prediction: The next crime might happen at {next_crime_time}.")

clf = DecisionTreeClassifier()
clf.fit(df[["Suspect_Age", "Suspect_Gender"]], df["Outcome"])
pred_suspect = clf.predict(pd.DataFrame([[random.randint(18, 50), random.choice([0, 1])]], columns=["Suspect_Age", "Suspect_Gender"]))
st.write(f"AI Prediction: The suspect is likely to have outcome - {pred_suspect[0]}.")

difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Hard", "Expert"], key="difficulty_level")
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
        st.success("Correct! You've solved the case.")
        score += 100
    else:
        attempts -= 1
        if attempts > 0:
            st.warning(f"Wrong guess! You have {attempts} attempts left.")
            if difficulty == "Easy":
                st.info("Hint: The crime happened in an area with previous reports.")
        else:
            st.error("Game Over! The case remains unsolved.")

st.write(f"Your final score: {score}")
st.write("Use AI and your detective skills to crack the mystery!")
