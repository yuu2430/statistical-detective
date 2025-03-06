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

possible_occupations = ["Security Guard", "Electrician", "Delivery Driver", "Janitor", "Shop Owner"]
possible_connections = [
    "Works at crime scene", "Recently fired from site", "Regular route nearby", 
    "Night shift worker", "Financial troubles"
]

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

@st.cache_data
def generate_case():
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {"evening": "6:00 PM - 8:00 PM", "night": "10:00 PM - 12:00 AM", "afternoon": "2:00 PM - 4:00 PM"}
    
    shuffled_occupations = random.sample(possible_occupations, len(possible_occupations))
    shuffled_connections = random.sample(possible_connections, len(possible_connections))
    
    suspects = {
        name: {"occupation": shuffled_occupations[i], "connection": shuffled_connections[i]}
        for i, name in enumerate(random.sample(["Alex", "Sam", "Jordan", "Taylor", "Casey"], 5))
    }
    
    culprit = random.choice(list(suspects.keys()))
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

# Reset case on refresh or button press
if "case" not in st.session_state or st.session_state.get("new_case", False):
    st.session_state.case = generate_case()
    st.session_state.new_case = False

case = st.session_state.case

def calculate_probabilities(case):
    suspects = case["suspects"]
    weapon = crime_types[case["crime"]]["weapon"]
    time_period = crime_types[case["crime"]]["time"]
    
    for name, info in suspects.items():
        probability = 0
        if occupation_weapon[info["occupation"]] == weapon:
            probability += 30
        if info["occupation"] in time_consistency[time_period]:
            probability += 20
        suspects[name]["probability"] = min(probability, 100)
    
    return suspects

case["suspects"] = calculate_probabilities(case)

st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")

st.subheader("👥 Persons of Interest")
shuffled_suspect_names = random.sample(list(case["suspects"].keys()), len(case["suspects"]))
cols = st.columns(len(shuffled_suspect_names))

for i, name in enumerate(shuffled_suspect_names):
    info = case["suspects"][name]
    with cols[i]:
        st.write(f"### {name}")
        st.write(f"**Occupation**: {info['occupation']}")
        st.write(f"**Connection**: {info['connection']}")
        with st.expander("Alibi"):
            st.write(random.choice([
                'Was alone during the incident (weak alibi)',
                'Claims to be running errands',
                'Says they were helping a friend',
                'Mentions being stuck in traffic (weak alibi)'
            ]))

st.subheader("🔎 Compromised Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Could match multiple suspects)")

st.subheader("🕵️ Logical Analysis")
user_guess = st.selectbox("Select the culprit:", list(case["suspects"].keys()))

if st.button("🔒 Submit Final Answer"):
    correct = user_guess == case["true_culprit"]
    occupation_match = occupation_weapon[case["suspects"][case["true_culprit"]]["occupation"]] == crime_types[case["crime"]]["weapon"]
    time_match = case["suspects"][case["true_culprit"]]["occupation"] in time_consistency[crime_types[case["crime"]]["time"]]
    
    if correct and occupation_match and time_match:
        st.success("🎉 Perfect deduction! You identified the hidden patterns!")
        st.balloons()
    elif correct:
        st.warning("✅ Correct suspect, but did you catch the full pattern? (Occupation + Time + Weapon)")
    else:
        st.error("❌ Incorrect. The truth hides in: Occupation-Weapon match + Typical schedule")

if st.button("🔄 New Case"):
    st.session_state.new_case = True
    st.rerun()
