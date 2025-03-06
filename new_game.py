import streamlit as st
import random

st.set_page_config(layout="wide")

# ---------- Initialize Statistics ----------
if "stats" not in st.session_state:
    st.session_state.stats = {"games_played": 0, "wins": 0, "losses": 0}

# ---------- Game Setup ----------
st.title("🔍 Mystery Solver: Deduce the Culprit")
st.write("Examine the ambiguous clues and subtle hints. Not everything is as it seems...")

# ---------- Crime and Clue Data ----------

def generate_crime_types():
    # Each crime type includes details for location, time, and a crime-specific tool.
    return {
        "Mall Robbery": {"location": "Mall", "time": "evening", "weapon": "crowbar"},
        "Factory Arson": {"location": "Industrial Area", "time": "night", "weapon": "lighter"},
        "Suburban Burglary": {"location": "Suburbs", "time": "afternoon", "weapon": "screwdriver"}
    }

# Possible suspect occupations, uniform colors, and accessories.
possible_occupations = ["Security Guard", "Electrician", "Delivery Driver", "Janitor", "Shop Owner"]
possible_uniforms = ["navy blue", "bright orange", "gray", "black", "green"]
possible_accessories = ["cap", "scarf", "watch", "bag", "none"]

# Hidden logical criteria for culprit determination for each crime type.
# For example, for Mall Robbery, a Security Guard who might be using a crowbar.
hidden_culprit_criteria = {
    "Mall Robbery": {
         "occupation": "Security Guard",
         "weapon": "crowbar"
    },
    "Factory Arson": {
         "occupation": "Janitor",
         "weapon": "lighter"
    },
    "Suburban Burglary": {
         "occupation": "Delivery Driver",
         "weapon": "screwdriver"
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
    
    # Create suspect names.
    suspect_names = ["Alex", "Sam", "Jordan", "Taylor", "Casey"]
    random.shuffle(suspect_names)
    
    # Generate suspect details randomly.
    suspects = {}
    for name in suspect_names:
        suspects[name] = {
            "occupation": random.choice(possible_occupations),
            "uniform": random.choice(possible_uniforms),
            "accessory": random.choice(possible_accessories),
            "alibi": random.choice([
                'Was alone during the incident (vague alibi)',
                'Claims to have been running errands',
                'Says they were helping a friend',
                'Mentions being stuck in traffic (vague alibi)'
            ])
        }
    
    # Hidden logic: Check which suspects meet the hidden criteria.
    criteria = hidden_culprit_criteria[crime_name]
    potential_culprits = [
        name for name, info in suspects.items()
        if info["occupation"] == criteria["occupation"]
    ]
    # If more than one meets the criteria, choose one randomly; else pick at random.
    if potential_culprits:
        culprit = random.choice(potential_culprits)
    else:
        culprit = random.choice(suspect_names)
    
    # Generate ambiguous evidence hints.
    evidence = {
        "Surveillance Footage": f"Fuzzy video shows a person in a {random.choice(possible_uniforms)} uniform, but the face is blurred.",
        "Tool Markings": f"Traces of tool usage indicate a {details['weapon']} was involved, yet the marks are inconclusive.",
        "Witness Statement": "A witness mentioned seeing someone with a noticeable accessory near the scene, but details were hazy.",
        "Digital Records": f"Activity logs show unauthorized access during {details['time']} hours."
    }
    
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": time_window[details["time"]],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence,
        "crime_details": details  # Save details for later use.
    }

# Initialize or reset game case.
if "case" not in st.session_state or st.button("🔄 New Case"):
    st.session_state.case = generate_case()
case = st.session_state.case

# ---------- Calculate Ambiguous Probabilities ----------

def calculate_probabilities(case):
    suspects = case["suspects"]
    details = case["crime_details"]
    criteria = hidden_culprit_criteria[case["crime"]]
    
    for name, info in suspects.items():
        probability = 0
        # Increase probability if occupation matches the hidden criterion.
        if info["occupation"] == criteria["occupation"]:
            probability += 30
        # Slight bonus for certain uniform colors (but this is not definitive).
        if info["uniform"] in ["navy blue", "gray", "bright orange"]:
            probability += 10
        # If accessory is not "none", add a small bonus.
        if info["accessory"] != "none":
            probability += 10
        # A vague alibi gives a bonus.
        if "vague" in info.get("alibi", ""):
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
        st.write(f"**Uniform Color:** {info['uniform']}")
        st.write(f"**Accessory:** {info['accessory']}")
        with st.expander("Alibi"):
            st.write(info['alibi'])
        st.write(f"**Match Probability:** {info['probability']}%")

st.subheader("🔎 Compromised Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (The clues are open to interpretation.)")

# ---------- Logical Analysis ----------
st.subheader("🕵️ Who is the Culprit?")
user_guess = st.selectbox("Select the culprit:", suspect_names)

if st.button("🔒 Submit Final Answer"):
    st.session_state.stats["games_played"] += 1
    correct = user_guess == case["true_culprit"]
    
    if correct:
        st.session_state.stats["wins"] += 1
        st.success("🎉 Your deduction is correct! The mystery deepens no more.")
        st.balloons()
    else:
        st.session_state.stats["losses"] += 1
        st.error(f"❌ Incorrect. The culprit was **{case['true_culprit']}**. Better luck next time!")
    
    # Option to start a new game.
    if st.button("Play Again"):
        st.session_state.case = generate_case()
        st.experimental_rerun()
