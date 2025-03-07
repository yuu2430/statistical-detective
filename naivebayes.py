import os 
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

os.environ["OMP_NUM_THREADS"] = "1"

st.set_page_config(layout="wide")  # Wide layout for better display

st.title("\U0001F50E Statistical Detective: AI to the Rescue")
st.write("Use statistics and AI to solve crime mysteries! Analyze the data, interpret the probabilities, and catch the suspect!")

# Game difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
attempts_left = difficulty_levels[difficulty]
if "attempts" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.attempts = attempts_left

@st.cache_data  # Cache dataset to keep cases consistent
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 101):  # Generate 100 cases
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

# Train Naïve Bayes Model
label_encoder_location = LabelEncoder()
label_encoder_time = LabelEncoder()
label_encoder_crime = LabelEncoder()

df['Location_Code'] = label_encoder_location.fit_transform(df['Location'])
df['Time_Code'] = label_encoder_time.fit_transform(df['Time'])
df['Crime_Type_Code'] = label_encoder_crime.fit_transform(df['Crime_Type'])

X = df[['Location_Code', 'Time_Code']]
y = df['Crime_Type_Code']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = MultinomialNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
st.write(f"🔍 Naïve Bayes Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Predict Crime Type for Selected Case
selected_location = random.choice(["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"])
selected_time = df.sample(1)['Time'].values[0]
selected_location_code = label_encoder_location.transform([selected_location])[0]
selected_time_code = label_encoder_time.transform([selected_time])[0]
predicted_crime_code = model.predict([[selected_location_code, selected_time_code]])[0]
predicted_crime = label_encoder_crime.inverse_transform([predicted_crime_code])[0]

st.write(f"⚠ AI Prediction: Based on past data, the most likely crime at {selected_location} around {selected_time} is *{predicted_crime}*.")

if st.button("🔄 New Game"):
    st.session_state.new_game = True
    st.session_state.attempts = difficulty_levels[difficulty]
    st.rerun()
