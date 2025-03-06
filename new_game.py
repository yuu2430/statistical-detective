import streamlit as st
import random

st.set_page_config(layout="wide")

# ---------- Initialize Statistics ----------
if "stats" not in st.session_state:
    st.session_state.stats = {"games_played": 0, "wins": 0, "losses": 0}

# ---------- Game Setup ----------
st.title("🔍 Mystery Solver: Logical Deduction Challenge")
st.write("Use the clues about uniforms, accessories, and other subtle hints to deduce the culprit.")

# ---------- Crime and Culprit Profiles ----------

def generate_crime_types():
    # Each crime type includes details for location, time, and weapon.
    return {
        "Mall Robbery": {"location": "Mall", "time": "evening", "weapon": "crowbar"},
        "Factory Arson": {"location": "Industrial Area", "time": "night", "weapon": "lighter"},
        "Suburban Burglary": {"location": "Suburbs", "time": "afternoon", "weapon": "screwdriver"}
    }

# A list of all possible occupations for suspects.
possible_occupations = ["Security Guard", "Electrician", "Delivery Driver", "Janitor", "Shop Owner"]

# Define a culprit profile for each crime type.
culprit_profiles = {
    "Mall Robbery": {
         "occupation": "Security Guard",
         "uniform": "navy blue uniform",
         "accessory": "a security badge and cap",
         "clue": "Witnesses noted someone in a navy blue uniform with a cap and a security badge, carrying a crowbar."
    },
    "Factory Arson": {
         "occupation": "Janitor",
         "uniform": "gray work overalls",
         "accessory": "a cigarette lighter visibly tucked in the pocket",
         "smoker": True,
         "clue": "A local reported seeing a figure in gray overalls, puffing on a cigarette near a lighter."
    },
    "Suburban Burglary": {
         "occupation": "Delivery Driver",
         "uniform": "bright orange delivery jacket",
         "accessory": "a casual cap and a bulky package",
         "clue": "Someone in a bright orange jacket was seen carrying a large, nondescript box."
    }
}

# ---------- Case Generation ----------

@st.cache_data()
def generate_case():
    crime_types = generate_crime_types()
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {
        "evening": "6:00 PM - 8:00 PM",
        "night": "10:00 PM - 12:00 AM",
        "afternoon": "2:00 PM - 4:00 PM"
    }
    
    # Create a list of suspect names.
    suspect_names = ["Alex", "Sam", "Jordan", "Taylor", "Casey"]
    random.shuffle(suspect_names)
    
    # Generate suspect data with random occupations.
    suspects = {}
    for name in suspect_names:
        suspects[name] = {
            "occupation": random.choice(possible_occupations),
            "alibi": random.choice([
                'Was alone during the incident (weak alibi)',
                'Claims to be running errands',
                'Says they were helping a friend',
                'Mentions being stuck in traffic (weak alibi)'
            ]),
            # Extra attributes default to None; they may be overridden for the culprit.
            "uniform": None,
            "accessory": None,
            "smoker": False
        }
    
    # Enforce the culprit profile based on the crime.
    profile = culprit_profiles[crime_name]
    # Choose one suspect at random to be the culprit.
    culprit = random.choice(suspect_names)
    # Override that suspect's details with the fixed profile.
    suspects[culprit]["occupation"] = profile["occupation"]
    suspects[culprit]["uniform"] = profile["uniform"]
    suspects[culprit]["accessory"] = profile["accessory"]
    if "smoker" in profile:
        suspects[culprit]["smoker"] = profile["smoker"]
    
    # Adjust evidence clues to hint at the culprit's profile.
    evidence = {
        "Security Footage": f"Fuzzy footage shows a figure wearing {profile['uniform'] if profile.get('uniform') else 'a generic outfit'}.",
        "Tool Markings": f"Marks indicate use of a {details['weapon']}.",
        "Witness Account": profile["clue"],
        "Digital Records": f"Unauthorized access occurred during {details['time']} hours."
    }
    
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": time_window[details["time"]],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence,
        "crime_details": details  # For further use in probability calculations.
    }

# Initialize or reset game case.
if "case" not in st.session_state or st.button("🔄 New Case"):
    st.session_state.case = generate_case()
case = st.session_state.case

# ---------- Calculate Match Probabilities ----------

def calculate_probabilities(case):
    suspects = case["suspects"]
    details = case["crime_details"]
    # Base probability bonus if suspect's occupation matches the culprit profile for the crime.
    profile = culprit_profiles[case["crime"]]
    
    for name, info in suspects.items():
        probability = 0
        # Occupation match bonus.
        if info["occupation"] == profile["occupation"]:
            probability += 30
        # Extra bonus if the suspect has the uniform or accessory that matches the profile.
        if info["uniform"] == profile.get("uniform"):
            probability += 20
        if info["accessory"] == profile.get("accessory"):
            probability += 20
        # Weak alibi bonus.
        if "weak" in info.get("alibi", ""):
            probability += 10
        # For Factory Arson, being a smoker increases the likelihood.
        if case["crime"] == "Factory Arson" and info.get("smoker", False):
            probability += 10
        
        suspects[name]["probability"] = min(probability, 100)
    
    return suspects

case["suspects"] = calculate_probabilities(case)

# ---------- Display Game Statistics ----------
st.sidebar.header("📊 Game Statistics")
stats = st.session_state.stats
st.sidebar.write(f"Games Played: {stats['games_played']}")
st.sidebar.write(f"Wins: {stats['wins']}")
st.sidebar.write(f"Losses: {stats['losses']}")

# ---------- Display Case Information ----------
st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")

st.subheader("👥 Persons of Interest")
suspect_names = list(case["suspects"].keys())
cols = st.columns(len(suspect_names))

for i, name in enumerate(suspect_names):
    info = case["suspects"][name]
    with cols[i]:
        st.write(f"### {name}")
        st.write(f"**Occupation:** {info['occupation']}")
        if info["uniform"]:
            st.write(f"**Uniform:** {info['uniform']}")
        if info["accessory"]:
            st.write(f"**Accessory:** {info['accessory']}")
        with st.expander("Alibi"):
            st.write(info['alibi'])
        st.write(f"**Match Probability:** {info['probability']}%")

st.subheader("🔎 Compromised Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Could match multiple suspects)")

# ---------- Logical Analysis ----------
st.subheader("🕵️ Logical Analysis")
user_guess = st.selectbox("Select the culprit:", suspect_names)

if st.button("🔒 Submit Final Answer"):
    st.session_state.stats["games_played"] += 1
    correct = user_guess == case["true_culprit"]
    profile = culprit_profiles[case["crime"]]
    
    if correct:
        st.session_state.stats["wins"] += 1
        st.success("🎉 Perfect deduction! You identified the hidden patterns!")
        st.balloons()
    else:
        st.session_state.stats["losses"] += 1
        st.error(f"❌ Incorrect. The culprit was **{case['true_culprit']}**. The game is now over.")
    
    # Option to start a new game.
    if st.button("Play Again"):
        st.session_state.case = generate_case()
        st.experimental_rerun()
