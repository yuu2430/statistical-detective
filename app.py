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
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    clothing_colors = ["Red", "Blue", "Black", "White", "Green"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):  # Generate 20 cases
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        data.append({
            "Case_ID": i,
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Suspect_Clothing": random.choice(clothing_colors),
            "Outcome": random.choice(["Unsolved", "Solved"])
        })
    return pd.DataFrame(data)

df = generate_crime_data()
st.dataframe(df, use_container_width=True)

# Select a case for the player
if "selected_case" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.selected_case = df.sample(1).iloc[0].to_dict()
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

st.write("📊 AI Predictions Based on Past Data:")
st.write(f"🕵️ Probability suggests the suspect is likely in their {selected_case['Suspect_Age'] // 10 * 10}s (~{random.randint(60, 80)}% confidence).")
st.write(f"🧥 The suspect was last seen wearing a {selected_case['Suspect_Clothing']} outfit.")
st.write(f"🔢 Attempts left: {st.session_state.attempts}")

guessed_location = st.selectbox("Where did the crime occur?", df["Location"].unique(), key="crime_location")
guessed_age = st.slider("What is the suspect's age?", 18, 50, key="suspect_age")
guessed_gender = st.radio("What is the suspect's gender?", ["Male", "Female"], key="suspect_gender")
guessed_clothing = st.selectbox("What color was the suspect's clothing?", df["Suspect_Clothing"].unique(), key="suspect_clothing")
guessed_gender = 0 if guessed_gender == "Male" else 1

if st.button("Submit Guess", key="submit_guess"):
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == (0 if selected_case["Suspect_Gender"] == "Male" else 1)
    correct_clothing = guessed_clothing == selected_case["Suspect_Clothing"]
    
    if correct_location and correct_age and correct_gender and correct_clothing:
        st.success(f"🎉 Correct! You've solved the case. Reward: 🎖 {difficulty} Level Badge")
    else:
        st.session_state.attempts -= 1
        feedback = []
        if not correct_location:
            feedback.append("The location probability suggests another area...")
        if not correct_age:
            feedback.append("The age probability doesn't align with the data...")
        if not correct_gender:
            feedback.append("Gender statistics indicate a different suspect...")
        if not correct_clothing:
            feedback.append("Eyewitness reports mention a different clothing color...")
        
        if st.session_state.attempts > 0:
            st.error("💀 Not quite! " + " ".join(feedback) + f" Attempts left: {st.session_state.attempts}")
        else:
            st.error("💀 No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"🕵️ Age: {selected_case['Suspect_Age']}")
            st.write(f"👤 Gender: {selected_case['Suspect_Gender']}")
            st.write(f"🧥 Clothing: {selected_case['Suspect_Clothing']}")

if st.button("🔄 New Game"):
    st.session_state.new_game = True
    st.session_state.attempts = difficulty_levels[difficulty]
    st.rerun()import os 
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
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    clothing_colors = ["Red", "Blue", "Black", "White", "Green"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 21):  # Generate 20 cases
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        data.append({
            "Case_ID": i,
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Location": random.choice(locations),
            "Crime_Type": random.choice(crime_types),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Suspect_Clothing": random.choice(clothing_colors),
            "Outcome": random.choice(["Unsolved", "Solved"])
        })
    return pd.DataFrame(data)

df = generate_crime_data()
st.dataframe(df, use_container_width=True)

# Select a case for the player
if "selected_case" not in st.session_state or st.session_state.get("new_game", False):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False

selected_case = st.session_state.selected_case

st.write("📊 AI Predictions Based on Past Data:")
st.write(f"🕵️ Probability suggests the suspect is likely in their {selected_case['Suspect_Age'] // 10 * 10}s (~{random.randint(60, 80)}% confidence).")
st.write(f"🧥 The suspect was last seen wearing a {selected_case['Suspect_Clothing']} outfit.")
st.write(f"🔢 Attempts left: {st.session_state.attempts}")

guessed_location = st.selectbox("Where did the crime occur?", df["Location"].unique(), key="crime_location")
guessed_age = st.slider("What is the suspect's age?", 18, 50, key="suspect_age")
guessed_gender = st.radio("What is the suspect's gender?", ["Male", "Female"], key="suspect_gender")
guessed_clothing = st.selectbox("What color was the suspect's clothing?", df["Suspect_Clothing"].unique(), key="suspect_clothing")
guessed_gender = 0 if guessed_gender == "Male" else 1

if st.button("Submit Guess", key="submit_guess"):
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == (0 if selected_case["Suspect_Gender"] == "Male" else 1)
    correct_clothing = guessed_clothing == selected_case["Suspect_Clothing"]
    
    if correct_location and correct_age and correct_gender and correct_clothing:
        st.success(f"🎉 Correct! You've solved the case. Reward: 🎖 {difficulty} Level Badge")
    else:
        st.session_state.attempts -= 1
        feedback = []
        if not correct_location:
            feedback.append("The location probability suggests another area...")
        if not correct_age:
            feedback.append("The age probability doesn't align with the data...")
        if not correct_gender:
            feedback.append("Gender statistics indicate a different suspect...")
        if not correct_clothing:
            feedback.append("Eyewitness reports mention a different clothing color...")
        
        if st.session_state.attempts > 0:
            st.error("💀 Not quite! " + " ".join(feedback) + f" Attempts left: {st.session_state.attempts}")
        else:
            st.error("💀 No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"🕵️ Age: {selected_case['Suspect_Age']}")
            st.write(f"👤 Gender: {selected_case['Suspect_Gender']}")
            st.write(f"🧥 Clothing: {selected_case['Suspect_Clothing']}")

if st.button("🔄 New Game"):
    st.session_state.new_game = True
    st.session_state.attempts = difficulty_levels[difficulty]
    st.rerun()
