import streamlit as st
import random

st.set_page_config(layout="wide")

# ---------- Initialize Statistics ----------
if "stats" not in st.session_state:
    st.session_state.stats = {"games_played": 0, "wins": 0, "losses": 0}

# ---------- Game Setup ----------
st.title("🔍 Mystery Solver: Logical Deduction Challenge")
st.write("Analyze subtle patterns and hidden clues. One clear truth emerges from multiple hints...")

# ---------- Crime Data Generation ----------
def generate_crime_types():
    return {
        "Mall Robbery": {"location": "Mall", "time": "evening", "weapon": "crowbar"},
        "Factory Arson": {"location": "Industrial Area", "time": "night", "weapon": "lighter"},
        "Suburban Burglary": {"location": "Suburbs", "time": "afternoon", "weapon": "screwdriver"}
    }

possible_occupations = ["Security Guard", "Electrician", "Delivery Driver", "Janitor", "Shop Owner"]

occupation_weapon = {
    "Security Guard": "crowbar",
    "Electrician": "screwdriver",
    "Delivery Driver": "crowbar",
    "Janitor": "lighter",
    "Shop Owner": "screwdriver"
}

time_consistency = {
    "evening": ["Security Guard", "Shop Owner"],
    "night": ["Janitor", "Electrician"],
    "afternoon": ["Delivery Driver", "Shop Owner"]
}

@st.cache_data()
def generate_case():
    crime_types = generate_crime_types()
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {
        "evening": "6:00 PM - 8:00 PM",
        "night": "10:00 PM - 12:00 AM",
        "afternoon": "2:00 PM - 4:00 PM"
    }
    
    # Shuffle occupations to ensure unique assignment per suspect
    shuffled_occupations = random.sample(possible_occupations, len(possible_occupations))
    suspect_names = ["Alex", "Sam", "Jordan", "Taylor", "Casey"]
    random.shuffle(suspect_names)
    
    suspects = {}
    for i, name in enumerate(suspect_names):
        suspects[name] = {
            "occupation": shuffled_occupations[i],
            "alibi": random.choice([
                'Was alone during the incident (weak alibi)',
                'Claims to be running errands',
                'Says they were helping a friend',
                'Mentions being stuck in traffic (weak alibi)'
            ])
        }
    
    culprit = random.choice(suspect_names)
    evidence = {
        "Security Footage": f"Blurry figure wearing {random.choice(['red', 'blue', 'black'])} jacket",
        "Tool Markings": f"Matches {details['weapon']} found in {random.choice(['parking lot', 'storage room'])}",
        "Witness Account": f"Noticed someone with {random.choice(['backpack', 'toolbox'])} near scene",
        "Digital Records": f"Unauthorized access during {details['time']} hours"
    }
    
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": time_window[details["time"]],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence,
        "crime_details": details  # storing details for later use
    }

# Initialize or reset game case
if "case" not in st.session_state:
    st.session_state.case = generate_case()

case = st.session_state.case

def calculate_probabilities(case):
    suspects = case["suspects"]
    weapon = generate_crime_types()[case["crime"]]["weapon"]
    time_period = generate_crime_types()[case["crime"]]["time"]
    
    for name, info in suspects.items():
        probability = 0
        if occupation_weapon[info["occupation"]] == weapon:
            probability += 30
        if info["occupation"] in time_consistency[time_period]:
            probability += 20
        if "weak" in info.get("alibi", ""):
            probability += 10
        
        suspects[name]["probability"] = min(probability, 100)
    
    return suspects

case["suspects"] = calculate_probabilities(case)

# Display Game Statistics
st.sidebar.header("📊 Game Statistics")
stats = st.session_state.stats
st.sidebar.write(f"Games Played: {stats['games_played']}")
st.sidebar.write(f"Wins: {stats['wins']}")
st.sidebar.write(f"Losses: {stats['losses']}")

st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")
st.subheader("👥 Persons of Interest")

shuffled_suspect_names = list(case["suspects"].keys())
cols = st.columns(len(shuffled_suspect_names))

for i, name in enumerate(shuffled_suspect_names):
    info = case["suspects"][name]
    with cols[i]:
        st.write(f"### {name}")
        st.write(f"**Occupation**: {info['occupation']}")
        with st.expander("Alibi"):
            st.write(info['alibi'])
        st.write(f"**Match Probability**: {info['probability']}%")

st.subheader("🔎 Compromised Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Could match multiple suspects)")

st.subheader("🕵️ Logical Analysis")
user_guess = st.selectbox("Select the culprit:", list(case["suspects"].keys()))

if st.button("🔒 Submit Final Answer"):
    st.session_state.stats["games_played"] += 1
    correct = user_guess == case["true_culprit"]
    weapon = generate_crime_types()[case["crime"]]["weapon"]
    occupation = case["suspects"][case["true_culprit"]]["occupation"]
    time_period = generate_crime_types()[case["crime"]]["time"]
    occupation_match = occupation_weapon[occupation] == weapon
    time_match = occupation in time_consistency[time_period]
    
    if correct and occupation_match and time_match:
        st.session_state.stats["wins"] += 1
        st.success("🎉 Perfect deduction! You identified the hidden patterns!")
        st.balloons()
    elif correct:
        st.session_state.stats["wins"] += 1
        st.warning("✅ Correct suspect, but did you catch the full pattern? (Occupation + Time + Weapon)")
    else:
        st.session_state.stats["losses"] += 1
        st.error(f"❌ Incorrect. The culprit was **{case['true_culprit']}**. The game is now over.")
    
    # Offer an option to start a new game after a submission
    if st.button("Play Again"):
        st.session_state.case = generate_case()
        st.experimental_rerun()
