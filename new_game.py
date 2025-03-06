import streamlit as st
import random

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🔍 Sustainability Crime Solver")
st.write("Step into the role of an investigator solving environmental crimes! Use logic and clues to find the culprit.")

# ---------- Crime Data Generation ----------
crime_types = {
    "Illegal Waste Dumping": {"location": "Riverside", "time": "night", "weapon": "industrial truck"},
    "Greenwashing Fraud": {"location": "Corporate Office", "time": "afternoon", "weapon": "forged documents"},
    "Energy Theft": {"location": "Residential Area", "time": "evening", "weapon": "tampered meter"}
}

def generate_case():
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {
        "evening": "6:00 PM - 8:00 PM",
        "night": "10:00 PM - 12:00 AM",
        "afternoon": "2:00 PM - 4:00 PM"
    }
    
    suspects = {
        "Alex": {"occupation": "Factory Owner", "connection": "Previously fined for illegal dumping"},
        "Sam": {"occupation": "Corporate Executive", "connection": "Launched a 'green' campaign under investigation"},
        "Jordan": {"occupation": "Truck Driver", "connection": "Frequently seen near illegal waste sites"},
        "Taylor": {"occupation": "Electrician", "connection": "Worked on meters in the affected area"},
        "Casey": {"occupation": "Real Estate Developer", "connection": "Owns land near contaminated sites"}
    }
    
    culprit = random.choice(list(suspects.keys()))
    
    evidence = {
        "Security Footage": f"A blurry figure was spotted near {details['location']} at {random.choice(['10:30 PM', '7:15 PM', '3:45 PM'])}",
        "Financial Records": f"Suspicious payments linked to {random.choice(['waste disposal', 'meter tampering', 'corporate fraud'])}",
        "Witness Statement": f"Someone saw {random.choice(['a truck unloading waste', 'a person adjusting a meter', 'documents being shredded'])}, but their memory is unclear.",
        "Digital Logs": f"Unauthorized activity detected at {details['time']} hours"
    }
    
    alibis = {
        "Alex": random.choice(["Claims to have been at a meeting, but no records exist", "Says he was at home, but no proof"]),
        "Sam": random.choice(["Was in a board meeting, but left early", "Claims to be traveling, but flight records don’t match"]),
        "Jordan": random.choice(["Truck logs were deleted that night", "Says another driver borrowed his truck"]),
        "Taylor": random.choice(["Mentions a repair job, but no records exist", "Claims she left early, but GPS says otherwise"]),
        "Casey": random.choice(["Says he was meeting investors, but no records exist", "Claims he was home, but security cameras say otherwise"])
    }
    
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": time_window[details["time"]],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence,
        "alibis": alibis,
        "attempts": 0  # Track incorrect attempts
    }

# Initialize session state
if "case" not in st.session_state:
    st.session_state.case = generate_case()
if "score" not in st.session_state:
    st.session_state.score = 0

case = st.session_state.case

# ---------- Game Interface ----------
st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")

# ---------- Suspect Profiles ----------
st.subheader("👥 Suspects")
cols = st.columns(len(case["suspects"]))
for i, (name, info) in enumerate(case["suspects"].items()):
    with cols[i]:
        st.write(f"### {name}")
        st.write(f"**Occupation**: {info['occupation']}")
        st.write(f"**Connection**: {info['connection']}")
        with st.expander("Alibi"):
            st.write(case["alibis"][name])

# ---------- Evidence Board ----------
st.subheader("🔎 Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Some details may be misleading)")

# ---------- Deduction Mechanics ----------
st.subheader("🕵️ Investigate and Solve")

# ---------- Solution Check ----------
user_guess = st.selectbox("Who is the culprit?", list(case["suspects"].keys()))
if st.button("🔒 Submit Final Answer"):
    correct = user_guess == case["true_culprit"]
    if correct:
        st.success("🎉 Correct! You solved the case and won a treat! 🍬")
        st.session_state.score += 1
        st.balloons()
    else:
        st.session_state.case["attempts"] += 1
        if st.session_state.case["attempts"] >= 2:
            st.error("❌ Game Over! You used both attempts.")
        else:
            st.warning(f"❌ Incorrect! You have {2 - st.session_state.case['attempts']} attempt(s) left.")
    
    st.write(f"🏆 Your Score: {st.session_state.score}")

# ---------- New Case Button (Always Visible) ----------
if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.rerun()
