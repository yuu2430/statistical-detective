import os
os.environ["OMP_NUM_THREADS"] = "1"

import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

# Title and description
st.title("Statistical Detective: AI to the Rescue")
st.write("Solve the crime mystery using AI and statistical models!")

# Sample dataset (fictional crime data with more randomness)
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    data = []
    for i in range(1, 21):  # Increased cases for more complexity
        data.append({
            "Case_ID": i,
            "Date": 20240100 + (i * random.randint(1, 5)),
            "Time": random.randint(18, 23),
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"])
        })
    return pd.DataFrame(data)

df = generate_crime_data()
st.dataframe(df)  # Ensuring better display of the dataset

# Encoding categorical variables
location_map = {"Downtown": 0, "City Park": 1, "Suburbs": 2, "Industrial Area": 3, "Mall": 4}
df["Location"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1})

# Clustering Model (K-Means for crime hotspots)
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location", "Time"]])
st.write("AI-Detected Crime Hotspots:", df[['Case_ID', 'Location', 'Time', 'Cluster']])

# Regression Model (Predict next crime time based on past data)
reg = LinearRegression()
reg.fit(df[["Date"]], df[["Time"]])
next_crime_time = reg.predict(pd.DataFrame([[20240130]], columns=["Date"]))
st.write(f"AI Prediction: The next crime might happen at {int(next_crime_time[0][0])}:00 hours.")

# Classification Model (Predicting suspect involvement)
clf = DecisionTreeClassifier()
clf.fit(df[["Suspect_Age", "Suspect_Gender"]], df["Outcome"])
pred_suspect = clf.predict(pd.DataFrame([[random.randint(18, 50), random.choice([0, 1])]], columns=["Suspect_Age", "Suspect_Gender"]))
st.write(f"AI Prediction: The suspect is likely to have outcome - {pred_suspect[0]}.")

# Game Difficulty Selection
difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Hard", "Expert"])

# Limited Attempts & Clues
attempts = 3 if difficulty == "Easy" else 2 if difficulty == "Hard" else 1
score = 0

# User Input (Solve the Case)
st.write("Solve the case by guessing the crime location and suspect details!")
guessed_location = st.selectbox("Select Crime Location", list(location_map.keys()))
guessed_age = st.slider("Guess Suspect Age", 18, 50)
guessed_gender = st.radio("Guess Suspect Gender", ["Male", "Female"])
guessed_gender = 0 if guessed_gender == "Male" else 1

# Select a random case instead of always using df.iloc[0]
selected_case = df.sample(1).iloc[0]
correct_location = selected_case["Location"]
correct_age = selected_case["Suspect_Age"]
correct_gender = selected_case["Suspect_Gender"]

if st.button("Submit Guess"):
    if guessed_location == list(location_map.keys())[correct_location] and guessed_age == correct_age and guessed_gender == correct_gender:
        st.success("Correct! You've solved the case.")
        score += 100
    else:
        attempts -= 1
        if attempts > 0:
            st.warning(f"Wrong guess! You have {attempts} attempts left.")
            if difficulty == "Easy":
                st.info("Hint: The crime location is near a popular area.")
        else:
            st.error("Game Over! The case remains unsolved.")

st.write(f"Your final score: {score}")

st.write("Use AI and your detective skills to crack the mystery!")
