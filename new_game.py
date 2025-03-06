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
    
    shuffled_occupations = random.sample(possible_occupations, len(possible_occupations))
    shuffled_connections = random.sample(possible_connections, len(possible_connections))
    shuffled_suspect_names = random.sample(["Alex", "Sam", "Jordan", "Taylor", "Casey"], 5)
    
    suspects = {
        shuffled_suspect_names[i]: {
            "occupation": shuffled_occupations[i],
            "connection": shuffled_connections[i]
        } for i in range(5)
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
        "time_window": details["time"],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence
    }

if "case" not in st.session_state or "restart" in st.session_state:
    st.session_state.case = generate_case()
    st.session_state.pop("restart", None)  # Reset restart flag
    st.rerun()

case = st.session_state.case

st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")

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
    if correct:
        st.success("🎉 Correct! You identified the culprit!")
        st.balloons()
    else:
        st.error(f"❌ Incorrect! The culprit was {case['true_culprit']}")

if st.button("🔄 New Case"):
    st.session_state.restart = True
    st.rerun()
