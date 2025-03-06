import streamlit as st
import random

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🔍 Sustainability Crime Solver")
st.write("Step into the role of an investigator tackling crimes against sustainability! Use logical reasoning and statistical insights to uncover the truth.")

# ---------- Crime Data Generation ----------
crime_types = {
    "Illegal Waste Dumping": {"location": "Riverside", "time": "night", "weapon": "industrial truck"},
    "Greenwashing Fraud": {"location": "Corporate Office", "time": "afternoon", "weapon": "forged documents"},
    "Energy Theft": {"location": "Suburban Area", "time": "evening", "weapon": "modified meter"}
}

def generate_case():
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {
        "evening": "6:00 PM - 8:00 PM",
        "night": "10:00 PM - 12:00 AM",
        "afternoon": "2:00 PM - 4:00 PM"
    }
    
    suspects = {
        "Alex": {"occupation": "Factory Owner", "connection": "Previously fined for environmental violations"},
        "Sam": {"occupation": "Corporate Executive", "connection": "Recently launched a 'sustainable' campaign under scrutiny"},
        "Jordan": {"occupation": "Truck Driver", "connection": "Known to transport unverified industrial waste"},
        "Taylor": {"occupation": "Electrician", "connection": "Worked on smart meters in the affected area"},
        "Casey": {"occupation": "Land Developer", "connection": "Owns property near the contaminated site"}
    }
    
    culprit = random.choice(list(suspects.keys()))
    
    evidence = {
        "Security Footage": f"Blurry figure seen at {details['location']} around {random.choice(['10:30 PM', '7:15 PM', '3:45 PM'])}",
        "Financial Records": f"Suspicious transactions related to {random.choice(['waste disposal', 'energy meter tampering', 'corporate greenwashing'])}",
        "Witness Account": f"A local resident reported seeing {random.choice(['a truck unloading waste', 'a person manipulating a meter', 'a document shredding session'])}, but details are unclear.",
        "Digital Records": f"Logs indicate unauthorized activity during {details['time']} hours"
    }
    
    alibis = {
        "Alex": random.choice(["Claims to have been at a business meeting, but records are missing", "Says they were at home, but no verification"]),
        "Sam": random.choice(["Was in a board meeting, but logs show an early exit", "Claims to be traveling, but flight records don't match"]),
        "Jordan": random.choice(["Truck logs were erased that night", "Insists another driver was using the vehicle"]),
        "Taylor": random.choice(["Mentions a repair job, but no work orders exist", "Claims they left early, but GPS shows otherwise"]),
        "Casey": random.choice(["Says they were meeting investors, but no meeting logs", "Claims they were home, but security cameras show an empty house"])
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
st.subheader("🕵️ Logical Analysis")

# ---------- Solution Check ----------
user_guess = st.selectbox("Select the culprit:", list(case["suspects"].keys()))
if st.button("🔒 Submit Final Answer"):
    correct = user_guess == case["true_culprit"]
    if correct:
        st.success("🎉 Correct deduction! You win a sweet treat! Yay! 🍬")
        st.session_state.score += 1
        st.balloons()
    else:
        st.session_state.case["attempts"] += 1
        if st.session_state.case["attempts"] >= 2:
            st.error("❌ Game Over! You've used both attempts.")
        else:
            st.warning(f"❌ Incorrect! You have {2 - st.session_state.case['attempts']} attempt(s) left.")
    
    st.write(f"🏆 Your current score: {st.session_state.score}")

# ---------- New Case Button (Always Visible) ----------
if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.rerun()
