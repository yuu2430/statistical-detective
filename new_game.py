import streamlit as st
import random

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🔍 Mystery Solver: Logical Deduction Challenge")
st.write("Analyze subtle patterns and hidden connections. One clear truth emerges from multiple lies...")

# ---------- Crime Data Generation ----------
crime_types = {
    "Mall Robbery": {"location": "Mall", "time": "evening", "weapon": "crowbar"},
    "Factory Arson": {"location": "Industrial Area", "time": "night", "weapon": "lighter"},
    "Suburban Burglary": {"location": "Suburbs", "time": "afternoon", "weapon": "screwdriver"}
}

@st.cache_data
def generate_case():
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {
        "evening": "6:00 PM - 8:00 PM",
        "night": "10:00 PM - 12:00 AM",
        "afternoon": "2:00 PM - 4:00 PM"
    }
    
    suspects = {
        "Alex": {"occupation": "Security Guard", "connection": "Works at crime scene"},
        "Sam": {"occupation": "Electrician", "connection": "Recently fired from site"},
        "Jordan": {"occupation": "Delivery Driver", "connection": "Regular route nearby"},
        "Taylor": {"occupation": "Janitor", "connection": "Night shift worker"},
        "Casey": {"occupation": "Shop Owner", "connection": "Financial troubles"}
    }
    
    culprit = random.choice(list(suspects.keys()))
    
    # Create subtle evidence patterns
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
        "evidence": evidence
    }

# Initialize session state
if "case" not in st.session_state:
    st.session_state.case = generate_case()
if "score" not in st.session_state:
    st.session_state.score = 0  # Track player score

case = st.session_state.case

# ---------- Calculate Probabilities ----------
def calculate_probabilities(case):
    suspects = case["suspects"]
    weapon = crime_types[case["crime"]]["weapon"]
    time_period = crime_types[case["crime"]]["time"]
    
    for name, info in suspects.items():
        probability = 0
        
        # Occupation-Weapon Match (30% weight)
        if occupation_weapon[info["occupation"]] == weapon:
            probability += 30
        
        # Time Consistency (20% weight)
        if info["occupation"] in time_consistency[time_period]:
            probability += 20
        
        # Randomize alibi strength (10% weight)
        if "weak" in info.get("alibi", ""):
            probability += 10
        
        suspects[name]["probability"] = min(probability, 100)  # Cap at 100%
    
    return suspects

# Hidden connection system
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

# Update suspect profiles with probabilities
case["suspects"] = calculate_probabilities(case)

# ---------- Game Interface ----------
st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")

# ---------- Suspect Profiles in Columns ----------
st.subheader("👥 Persons of Interest")
cols = st.columns(len(case["suspects"]))  # Create columns for each suspect

for i, (name, info) in enumerate(case["suspects"].items()):
    with cols[i]:
        st.write(f"### {name}")
        st.write(f"**Occupation**: {info['occupation']}")
        st.write(f"**Connection**: {info['connection']}")
        st.write(f"**Probability of Guilt**: {info['probability']}%")
        with st.expander("Alibi"):
            st.write(random.choice([
                'Was alone during the incident (weak alibi)',
                'Claims to be running errands',
                'Says they were helping a friend',
                'Mentions being stuck in traffic (weak alibi)'
            ]))

# ---------- Evidence Board ----------
st.subheader("🔎 Compromised Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Could match multiple suspects)")

# ---------- Deduction Mechanics ----------
st.subheader("🕵️ Logical Analysis")

# ---------- Solution Check ----------
user_guess = st.selectbox("Select the culprit:", list(case["suspects"].keys()))
if st.button("🔒 Submit Final Answer"):
    correct = user_guess == case["true_culprit"]
    
    # Verify logical consistency
    crime_name = case["crime"]
    if crime_name not in crime_types:
        st.error("Invalid crime type. Please restart the game.")
    else:
        weapon = crime_types[crime_name]["weapon"]
        occupation = case["suspects"][case["true_culprit"]]["occupation"]
        time_period = crime_types[crime_name]["time"]
        
        occupation_match = occupation_weapon[occupation] == weapon
        time_match = occupation in time_consistency[time_period]

        if correct and occupation_match and time_match:
            st.success("🎉 Perfect deduction! You identified the hidden patterns!")
            st.session_state.score += 1  # Increase score
            st.balloons()
        elif correct:
            st.warning("✅ Correct suspect, but did you catch the full pattern? (Occupation + Time + Weapon)")
            st.session_state.score += 0.5  # Partial score
        else:
            st.error("❌ Incorrect. The truth hides in: Occupation-Weapon match + Typical schedule")
    
    st.write(f"🏆 Your current score: {st.session_state.score}")

# ---------- Restart ----------
if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
