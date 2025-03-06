import streamlit as st
import random

st.set_page_config(layout="wide")

# ---------- Initialize Statistics ----------
if "stats" not in st.session_state:
    st.session_state.stats = {"games_played": 0, "wins": 0, "losses": 0}

# ---------- Game Setup ----------
st.title("🔍 Mystery Solver: Deduce the Culprit")
st.write("Review the ambiguous CCTV footage and decide who the culprit is. The evidence is minimal—use your intuition!")

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
# For example, for Mall Robbery, a Security Guard is favored.
hidden_culprit_criteria = {
    "Mall Robbery": {"occupation": "Security Guard"},
    "Factory Arson": {"occupation": "Janitor"},
    "Suburban Burglary": {"occupation": "Delivery Driver"}
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
                'Claims to have been alone',
                'Says they were running errands',
                'Mentions helping a friend',
                'Notes being stuck in traffic'
            ])
        }
    
    # Hidden logic: Select a culprit based on the hidden criterion.
    criteria = hidden_culprit_criteria[crime_name]
    potential_culprits = [
        name for name, info in suspects.items()
        if info["occupation"] == criteria["occupation"]
    ]
    if potential_culprits:
        culprit = random.choice(potential_culprits)
    else:
        culprit = random.choice(suspect_names)
    
    # The only public hint is the CCTV footage. Its description is ambiguous.
    cctv_hint = f"Fuzzy CCTV footage shows a person wearing a {random.choice(possible_uniforms)} uniform. " \
                "The face is blurred and details are scarce."
    
    evidence = {
        "CCTV Footage": cctv_hint,
        "Tool Markings": f"Traces indicate a {details['weapon']} was used, though the evidence is inconclusive.",
        "Digital Records": f"Access occurred during {details['time']} hours."
    }
    
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": time_window[details["time"]],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence,
        "crime_details": details
    }

# Initialize or reset game case.
if "case" not in st.session_state or st.button("🔄 New Case"):
    st.session_state.case = generate_case()
case = st.session_state.case

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
# Only display the suspect names.
suspect_names = list(case["suspects"].keys())
cols = st.columns(len(suspect_names))
for i, name in enumerate(suspect_names):
    with cols[i]:
        st.write(f"### {name}")
        # Details like occupation, uniform, or alibi are hidden from the player.

st.subheader("🔎 Evidence")
# Only the CCTV footage is intended as a clue, along with some generic evidence.
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail)

# ---------- Logical Analysis ----------
st.subheader("🕵️ Who is the Culprit?")
user_guess = st.selectbox("Select the culprit:", suspect_names)

if st.button("🔒 Submit Final Answer"):
    st.session_state.stats["games_played"] += 1
    correct = user_guess == case["true_culprit"]
    
    if correct:
        st.session_state.stats["wins"] += 1
        st.success("🎉 Your deduction is correct!")
        st.balloons()
    else:
        st.session_state.stats["losses"] += 1
        st.error(f"❌ Incorrect. The culprit was **{case['true_culprit']}**.")
    
    if st.button("Play Again"):
        st.session_state.case = generate_case()
        st.experimental_rerun()
