import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.cluster import KMeans

# Debug: Ensure Streamlit is properly imported
try:
    print(f"Streamlit version: {st.__version__}")
except NameError:
    st.error("Streamlit is not properly imported. Please ensure you're running this script with `streamlit run`.")
    st.stop()

# Initialize Streamlit configuration
st.set_page_config(
    page_title="🔍 Statistical Detective",
    page_icon="🕵️",
    layout="wide"
)

# Set environment variable for KMeans (to avoid warnings)
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
if "show_correct_answer" not in st.session_state:
    st.session_state.show_correct_answer = False  # Track whether to show the correct answer

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

# Define crime types and their associated evidence
crime_evidence = {
    "Assault": "A heavy metal rod was found at the scene with fingerprints.",
    "Burglary": "Pry marks on the door match a specific crowbar pattern.",
    "Kidnapping": "Residue of chloroform detected on a nearby cloth.",
    "Theft": "Bag strap cut cleanly with a small sharp blade.",
    "Robbery": "Security footage shows a handgun was used.",
    "Fraud": "Forged documents left behind at the scene."
}

# Define time periods
def get_time_period(hour):
    if 6 <= hour < 12:
        return "Morning (6 AM - 12 PM)"
    elif 12 <= hour < 18:
        return "Afternoon (12 PM - 6 PM)"
    elif 18 <= hour < 24:
        return "Evening (6 PM - 12 AM)"
    else:
        return "Night (12 AM - 6 AM)"

# Generate crime data (hidden time period/evidence)
@st.cache_data
def generate_crime_data():
    crime_types = list(crime_evidence.keys())
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    for _ in range(10):
        crime_time_minutes = random.randint(0, 1439)
        hour = crime_time_minutes // 60
        time_period = get_time_period(hour)
        formatted_time = datetime.strptime(f"{hour}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        
        crime_type = random.choice(crime_types)
        data.append({
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Crime_Type": crime_type,
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female", "Other"]),
            # Hidden analysis columns:
            "_Time_Period": time_period,
            "_Evidence": crime_evidence[crime_type],
            "Time_Minutes": crime_time_minutes
        })
    return pd.DataFrame(data)

df = generate_crime_data()

# Display crime database (without hidden columns)
st.header("📊 Recent Crime Cases")
st.dataframe(
    df.drop(columns=["_Time_Period", "_Evidence", "Time_Minutes"], errors="ignore"),
    use_container_width=True
)

# Crime pattern detection
location_map = {"Manjalpur": 0, "Fatehgunj": 1, "Gorwa": 2, "Makarpura": 3}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1, "Other": 2})

# Use multiple features for clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code", "Time_Minutes"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

# Enhanced cluster hints with time patterns
def generate_cluster_hints(df):
    cluster_hints = {}
    for cluster in df['Cluster'].unique():
        cluster_data = df[df['Cluster'] == cluster]
        most_common_period = cluster_data["_Time_Period"].mode()[0]
        location = cluster_data["Location"].mode()[0]
        
        # Get time pattern statistics
        period_counts = cluster_data["_Time_Period"].value_counts(normalize=True).to_dict()
        period_stats = "\n".join([f"- {k}: {v*100:.1f}% of cases" for k,v in period_counts.items()])
        
        cluster_hints[cluster] = {
            "location": location,
            "time_pattern": f"Most crimes occur during {most_common_period}",
            "period_stats": period_stats
        }
    return cluster_hints

# Select a case for the player
if st.session_state.selected_case is None or st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0  # Reset hints for new case
    st.session_state.show_correct_answer = False  # Reset correct answer display

selected_case = st.session_state.selected_case

# Investigation Toolkit Section
st.divider()
st.header("🕵️ Investigation Toolkit")

# Always show basic clues
st.write(f"🔖 Age Estimate: {selected_case['Suspect_Age']-5}-{selected_case['Suspect_Age']+5} years")

# Location analysis hint combining cluster and time patterns
cluster_info = generate_cluster_hints(df)[selected_case['Cluster']]
st.write(f"""
**📍 Location Analysis**  
This area ({cluster_info['location']}) shows:  
{cluster_info['time_pattern']}  
Time distribution:  
{cluster_info['period_stats']}
""")

# Gradual evidence revelation
if st.session_state.hints_revealed >= 1:
    st.write(f"🔍 Crime Scene Evidence: {selected_case['_Evidence']}")
if st.session_state.hints_revealed >= 2:
    st.write(f"🕒 Exact Crime Time: {selected_case['Time']} ({selected_case['_Time_Period']})")

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
            feedback.append("📍 Location doesn't match.")
        if abs(guessed_age - selected_case['Suspect_Age']) > 5:
            feedback.append("📈 Age estimate significantly off.")
        elif guessed_age != selected_case['Suspect_Age']:
            feedback.append("📈 Age estimate close but not exact.")
        if guessed_gender != selected_case['Suspect_Gender']:
            feedback.append("👤 Gender mismatch.")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
            st.session_state.hints_revealed += 1  # Reveal more hints
        else:
            st.session_state.show_correct_answer = True  # Show correct answer

# Display correct answer if attempts are exhausted
if st.session_state.show_correct_answer:
    st.error("❌ Case Closed. No attempts left! The correct answer was:")
    st.write(f"📍 Location: {selected_case['Location']}")
    st.write(f"🔢 Age: {selected_case['Suspect_Age']}")
    st.write(f"👤 Gender: {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female' if selected_case['Suspect_Gender'] == 1 else 'Other'}")
    st.session_state.new_game = True  # Reset the game after revealing the correct answer
    st.session_state.attempts = difficulty_levels[difficulty]  # Reset attempts for the next game
    st.session_state.show_correct_answer = False  # Reset correct answer display

# Status bar
st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Attempts Left: {st.session_state.attempts}")

# New case button
if st.button("🔄 Start New Case"):
    st.session_state.new_game = True
    st.session_state.hints_revealed = 0  # Reset hints for new case
    st.session_state.show_correct_answer = False  # Reset correct answer display
