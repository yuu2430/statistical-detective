import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from scipy import stats

# Initialize Streamlit configuration first
st.set_page_config(
    page_title="🔍 Vadodara Crime Solver",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Updated Nature-inspired Color Theme with original table styling
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



st.title("🔍 Vadodara Crime Solver")
st.write("*Analyze local crime patterns and catch the culprit!*")

# Game settings
difficulty_levels = {
    "Easy": {"attempts": 3, "hints": 3},
    "Medium": {"attempts": 2, "hints": 2},
    "Hard": {"attempts": 1, "hints": 1}
}

difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()))
current_difficulty = difficulty_levels[difficulty]

@st.cache_data
def generate_crime_data():
    patterns = {
        "Street Robbery": {
            "locations": ["Manjalpur", "Fatehgunj"],
            "time_range": (18, 23),  # 6PM-11PM
            "age_range": (20, 35),
            "gender_bias": {"Male": 0.85, "Female": 0.15}
        },
        "Vehicle Theft": {
            "locations": ["Makarpura", "Gorwa"],
            "time_range": (20, 4),   # 8PM-4AM
            "age_range": (25, 40),
            "gender_bias": {"Male": 0.9, "Female": 0.1}
        },
        "Chain Snatching": {
            "locations": ["Fatehgunj", "Manjalpur"],
            "time_range": (16, 20),  # 4PM-8PM
            "age_range": (18, 30),
            "gender_bias": {"Male": 0.95, "Female": 0.05}
        },
        "Cyber Fraud": {
            "locations": ["Gorwa", "Makarpura"],
            "time_range": (9, 17),   # 9AM-5PM
            "age_range": (25, 45),
            "gender_bias": {"Male": 0.7, "Female": 0.3}
        }
    }

    cases = []
    for case_id in range(1, 11):
        crime_type = random.choice(list(patterns.keys()))
        pattern = patterns[crime_type]
        
        # Generate location
        location = random.choice(pattern["locations"])
        
        # Generate time
        start_hour, end_hour = pattern["time_range"]
        if start_hour <= end_hour:
            hour = random.randint(start_hour, end_hour)
        else:
            possible_hours = list(range(start_hour, 24)) + list(range(0, end_hour + 1))
            hour = random.choice(possible_hours)
        
        minute = random.choice(["00", "15", "30", "45"])
        time = f"{hour:02d}:{minute}"
        
        # Generate age
        age = int(np.clip(np.random.normal(
            sum(pattern["age_range"])/2,
            (pattern["age_range"][1] - pattern["age_range"][0])/6
        ), 18, 65))
        
        # Generate gender
        gender = random.choices(
            list(pattern["gender_bias"].keys()),
            weights=list(pattern["gender_bias"].values())
        )[0]

        cases.append({
            "Case_ID": case_id,
            "Date": (datetime(2024, 1, 1) + 
                    timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            "Location": location,
            "Crime_Type": crime_type,
            "Time": time,
            "Suspect_Age": age,
            "Suspect_Gender": gender
        })

    return pd.DataFrame(cases)

df = generate_crime_data()

def generate_hints(selected_case, difficulty_level):
    hints = []
    crime_type = selected_case["Crime_Type"]
    pattern = {
        "Street Robbery": {
            "locations": ["Manjalpur", "Fatehgunj"],
            "time": "evening hours (6PM-11PM)",
            "age": "typically 20-35 years old",
            "gender": "mostly male (85%)"
        },
        "Vehicle Theft": {
            "locations": ["Makarpura", "Gorwa"],
            "time": "late night to early morning (8PM-4AM)",
            "age": "usually 25-40 years old",
            "gender": "predominantly male (90%)"
        },
        "Chain Snatching": {
            "locations": ["Fatehgunj", "Manjalpur"],
            "time": "evening rush hours (4PM-8PM)",
            "age": "young adults (18-30 years)",
            "gender": "overwhelmingly male (95%)"
        },
        "Cyber Fraud": {
            "locations": ["Gorwa", "Makarpura"],
            "time": "daytime working hours (9AM-5PM)",
            "age": "25-45 years old",
            "gender": "mostly male (70%)"
        }
    }.get(crime_type, {})

    if pattern:
        hints.extend([
            f"🔍 {crime_type} cases usually occur in {', '.join(pattern['locations'])}",
            f"🕒 Common time: {pattern['time']}",
            f"👤 Typical suspect: {pattern['age']}, {pattern['gender']}"
        ])
    
    return hints[:difficulty_levels[difficulty_level]["hints"]]

# Session state management
if "target_case" not in st.session_state:
    st.session_state.target_case = df.sample(1).iloc[0]
    st.session_state.attempts = current_difficulty["attempts"]
    st.session_state.hints_used = 0

# [ALL GAME CODE REMAINS THE SAME UNTIL THE DATA DISPLAY SECTION]

# Display crime database without scrolling (original table styling)
st.header("📊 Recent Crime Cases")
st.dataframe(
    df,
    use_container_width=True,
    height=(len(df) + 1) * 35 + 3  # Dynamic height based on rows
)

# [REST OF THE CODE REMAINS EXACTLY THE SAME]
st.divider()
st.header("🕵️♂️ Investigation Toolkit")

# Hint system
with st.expander("🔍 Reveal Investigation Clues", expanded=difficulty=="Easy"):
    hints = generate_hints(st.session_state.target_case, difficulty)
    for hint in hints:
        st.write(f"🔖 {hint}")
    st.session_state.hints_used = len(hints)

# Investigation inputs
col1, col2, col3 = st.columns(3)
with col1:
    loc_guess = st.selectbox("Crime Location", df["Location"].unique())
with col2:
    age_guess = st.slider("Suspect Age", 18, 65, 30)
with col3:
    gender_guess = st.radio("Suspect Gender", ["Male", "Female"])

# Submit investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    target = st.session_state.target_case
    correct = (loc_guess == target["Location"]) & (age_guess == target["Suspect_Age"]) & (gender_guess == target["Suspect_Gender"])
    
    if correct:
        st.success("🎉 Case Solved! You've identified the suspect!")
        st.balloons()
    else:
        feedback = []
        if loc_guess != target["Location"]:
            feedback.append("📍 Location doesn't match crime pattern")
        if abs(age_guess - target["Suspect_Age"]) > 5:
            feedback.append("📈 Age estimate significantly off")
        elif age_guess != target["Suspect_Age"]:
            feedback.append("📈 Age estimate close but not exact")
        if gender_guess != target["Suspect_Gender"]:
            feedback.append("👤 Gender probability mismatch")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
        else:
            st.error(f"❌ Case Closed. Correct answer: {target['Location']}, Age {target['Suspect_Age']}, {target['Suspect_Gender']}")
            st.session_state.target_case = df.sample(1).iloc[0]
            st.session_state.attempts = current_difficulty["attempts"]

# Status bar
st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Clues Used: {st.session_state.hints_used}/{current_difficulty['hints']}")

# New case button
if st.button("🔄 Start New Case"):
    st.session_state.target_case = df.sample(1).iloc[0]
    st.session_state.attempts = current_difficulty["attempts"]
    st.rerun()





















import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from scipy import stats  # For confidence interval calculation

# Initialize Streamlit configuration first
st.set_page_config(
    page_title="🔍 Statistical Detective",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Updated Nature-inspired Color Theme with original table styling
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

st.title("🔍 Statistical Detective")
st.write("*You are given the role of a Detective! Yay! Now, you have to use Statistics and Hints! Analyze the data, interpret the probabilities, and catch the suspect!*")

# Game difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")
attempts_left = difficulty_levels[difficulty]

# Initialize session state
if "attempts" not in st.session_state:
    st.session_state.attempts = attempts_left
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "new_game" not in st.session_state:
    st.session_state.new_game = True

@st.cache_data  # Cache dataset to keep cases consistent
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 11):  # Generate 10 cases
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        data.append({
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

# Display crime database without scrolling (original table styling)
st.header("📊 Recent Crime Cases")
st.dataframe(
    df.drop(columns=["Time_Minutes"], errors="ignore"),
    use_container_width=True,
    height=(len(df) + 1) * 35 + 3  # Dynamic height based on rows
)

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
if st.session_state.selected_case is None or st.session_state.new_game:
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

st.divider()
st.header("🕵️Investigation Toolkit")

# Hint system
with st.expander("🔍 Reveal Investigation Clues", expanded=difficulty=="Easy"):
    st.write(f"🔖 Probability suggests the suspect is likely in their {age_group}s (~{confidence_percent_low}%-{confidence_percent_high}% confidence).")
    st.write(f"🔖 Location Analysis: {selected_case['Cluster_Hint']}")

# Investigation inputs
col1, col2, col3 = st.columns(3)
with col1:
    guessed_location = st.selectbox("Crime Location", list(location_map.keys()), key="crime_location")
with col2:
    guessed_age = st.slider("Suspect Age", 18, 50, 30, key="suspect_age")
with col3:
    guessed_gender = st.radio("Suspect Gender", ["Male", "Female"], key="suspect_gender")

guessed_gender = 0 if guessed_gender == "Male" else 1

# Submit investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Case Solved! You've identified the suspect! You win a sweet treat :)")
        st.balloons()
        st.session_state.new_game = True  # Reset the game after solving the case
    else:
        feedback = []
        if not correct_location:
            feedback.append("📍 Location doesn't match crime pattern")
        if abs(guessed_age - selected_case["Suspect_Age"]) > 5:
            feedback.append("📈 Age estimate significantly off")
        elif guessed_age != selected_case["Suspect_Age"]:
            feedback.append("📈 Age estimate close but not exact")
        if guessed_gender != selected_case["Suspect_Gender"]:
            feedback.append("👤 Gender probability mismatch")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
        else:
            st.error(f"❌ Case Closed. Correct answer: {selected_case['Location']}, Age {selected_case['Suspect_Age']}, {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female'}")
            st.session_state.new_game = True  # Reset the game after running out of attempts

# Reset the game if new_game is True
if st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.new_game = False
    st.rerun()

# Status bar
st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Attempts Left: {st.session_state.attempts}")

# New case button
if st.button("🔄 Start New Case"):
    st.session_state.new_game = True
    st.rerun()






























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

# Define crime types, weapons, and crime scene evidence
crime_weapons = {
    "Assault": {"Weapon": "Metal Rod", "Evidence": "The suspect was last seen holding a heavy metal rod before the attack."},
    "Burglary": {"Weapon": "Crowbar", "Evidence": "A crowbar was found near the broken window, suggesting forced entry."},
    "Kidnapping": {"Weapon": "Chloroform", "Evidence": "A discarded cloth with traces of chloroform was found at the scene."},
    "Theft": {"Weapon": "Pocket Knife", "Evidence": "A small pocket knife was used to cut open the victim's bag strap."},
    "Robbery": {"Weapon": "Gun", "Evidence": "The suspect was seen fleeing with a gun in hand."},
    "Fraud": {"Weapon": "None", "Evidence": "No physical evidence was found at the scene."}
}

# Define time periods
time_periods = {
    "Morning": (360, 719),  # 6 AM - 11:59 AM
    "Afternoon": (720, 1079),  # 12 PM - 5:59 PM
    "Evening": (1080, 1439),  # 6 PM - 11:59 PM
    "Night": (0, 359)  # 12 AM - 5:59 AM
}

# Function to get time period based on time in minutes
def get_time_period(time_minutes):
    for period, (start, end) in time_periods.items():
        if start <= time_minutes <= end:
            return period
    return "Unknown"

# Generate crime data
@st.cache_data
def generate_crime_data():
    crime_types = list(crime_weapons.keys())
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    for _ in range(10):  # Generate 10 cases
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        crime_type = random.choice(crime_types)
        weapon = crime_weapons[crime_type]["Weapon"]
        evidence = crime_weapons[crime_type]["Evidence"]
        time_period = get_time_period(crime_time_minutes)
        data.append({
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Crime_Type": crime_type,
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female", "Other"]),
            "Weapon_Used": weapon,
            "Crime_Scene_Evidence": evidence,
            "Time_Period": time_period,
            "Outcome": random.choice(["Unsolved", "Solved"]),
            "Time_Minutes": crime_time_minutes
        })
    return pd.DataFrame(data)

df = generate_crime_data()

# Display crime database
st.header("📊 Recent Crime Cases")
st.dataframe(
    df.drop(columns=["Time_Minutes", "Crime_Scene_Evidence", "Time_Period"], errors="ignore"),
    use_container_width=True,
    height=(len(df) + 1) * 35 + 3  # Dynamic height based on rows
)

# Crime pattern detection
location_map = {"Manjalpur": 0, "Fatehgunj": 1, "Gorwa": 2, "Makarpura": 3}
df["Location_Code"] = df["Location"].map(location_map)
df["Suspect_Gender"] = df["Suspect_Gender"].map({"Male": 0, "Female": 1, "Other": 2})

# Use multiple features for clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code", "Time_Minutes"]])
df['Cluster_Location'] = df['Cluster'].map({0: "High-Risk Zone A", 1: "High-Risk Zone B", 2: "High-Risk Zone C"})

# Generate dynamic cluster hints
def generate_cluster_hints(df):
    cluster_hints = {}
    for cluster in df['Cluster'].unique():
        cluster_data = df[df['Cluster'] == cluster]
        night_crimes = cluster_data[cluster_data['Time_Minutes'] >= 1260]  # 9 PM - 5:59 AM
        weapon_crimes = cluster_data[cluster_data['Weapon_Used'] != "None"]
        burglary_crimes = cluster_data[cluster_data['Crime_Type'] == "Burglary"]
        
        if cluster == 0:
            hint = f"Crimes in this area often occur at night ({len(night_crimes) / len(cluster_data) * 100:.0f}% of cases)."
        elif cluster == 1:
            hint = f"This area has a high frequency of burglaries ({len(burglary_crimes) / len(cluster_data) * 100:.0f}% of cases)."
        elif cluster == 2:
            hint = f"Weapons are commonly used in crimes here ({len(weapon_crimes) / len(cluster_data) * 100:.0f}% of cases)."
        
        cluster_hints[f"High-Risk Zone {chr(65 + cluster)}"] = hint
    return cluster_hints

cluster_hints = generate_cluster_hints(df)
df['Cluster_Hint'] = df['Cluster_Location'].map(cluster_hints)

# Select a case for the player
if st.session_state.selected_case is None or st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0  # Reset hints for new case
    st.session_state.show_correct_answer = False  # Reset correct answer display

selected_case = st.session_state.selected_case

# Investigation toolkit
st.divider()
st.header("🕵️ Investigation Toolkit")

# Always show investigation clues (no dropdown)
st.write(f"🔖 Age Range: The suspect is likely between {selected_case['Suspect_Age'] - 5} and {selected_case['Suspect_Age'] + 5} years old.")
st.write(f"🔖 Location Analysis: A crime happened in this area that occurred during the {selected_case['Time_Period']}.")

# Gradual hints based on attempts
if st.session_state.hints_revealed >= 1:
    st.write(f"🔖 Crime Type: The crime type is {selected_case['Crime_Type']}.")
if st.session_state.hints_revealed >= 2:
    st.write(f"🔖 Crime Scene Evidence: {selected_case['Crime_Scene_Evidence']}")

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
