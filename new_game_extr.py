import streamlit as st
import random
import numpy as np
import scipy.stats as stats
import re

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🔍 Mystery Solver: Logical Deduction Challenge")
st.write("Step into the shoes of a detective and unravel the mystery! Follow the clues, interrogate suspects, and crack the case using logic and statistical reasoning.")

# ---------- Crime Data Generation ----------
crime_types = {
    "Mall Robbery": {"location": "Mall", "time": "evening", "weapon": "crowbar"},
    "Factory Arson": {"location": "Industrial Area", "time": "night", "weapon": "lighter"},
    "Suburban Burglary": {"location": "Suburbs", "time": "afternoon", "weapon": "screwdriver"}
}

def generate_witness_statement():
    templates = [
        "I saw someone wearing a {color} jacket near the {location}, but I couldn't see their face.",
        "There was a {height} person lurking around the {location} before the crime happened.",
        "I heard a loud noise and noticed a {feature} person running away from the scene.",
        "Someone with a {item} was acting suspicious near the {location} that night."
    ]
    colors = ["red", "blue", "black", "gray"]
    heights = ["tall", "short", "average-height"]
    features = ["limping", "hooded", "gloved"]
    items = ["backpack", "toolbox", "briefcase"]
    
    statement = random.choice(templates).format(
        color=random.choice(colors),
        location=random.choice(["mall", "factory", "house"]),
        height=random.choice(heights),
        feature=random.choice(features),
        item=random.choice(items)
    )
    return statement

def generate_case():
    crime_name, details = random.choice(list(crime_types.items()))
    time_window = {
        "evening": "6:00 PM - 8:00 PM",
        "night": "10:00 PM - 12:00 AM",
        "afternoon": "2:00 PM - 4:00 PM"
    }
    
    suspects = {
        "Alex": {"occupation": "Security Guard", "connection": "Previously caught stealing at crime scene"},
        "Sam": {"occupation": "Electrician", "connection": "Owed money to a shop owner in the area"},
        "Jordan": {"occupation": "Delivery Driver", "connection": "Fired after a dispute with a victim"},
        "Taylor": {"occupation": "Janitor", "connection": "Known for arguments with site manager"},
        "Casey": {"occupation": "Shop Owner", "connection": "Fraud investigation linked to location"}
    }
    
    culprit = random.choice(list(suspects.keys()))
    
    evidence = {
        "Security Footage": f"Blurry figure seen leaving crime scene at {random.choice(['5:50 PM', '7:30 PM', '11:00 PM'])}",
        "Tool Markings": f"Marks found that match a {details['weapon']} but also resemble common repair tools",
        "Witness Account": generate_witness_statement(),
        "Digital Records": f"Suspicious activity logged, but logs seem tampered with"
    }
    
    alibis = {
        "Alex": random.choice(["Claims to have been on duty but no logs exist", "Says they were taking a break alone"]),
        "Sam": random.choice(["Claims to be at home, but phone was tracked near the scene", "Alibi provided by a close friend"]),
        "Jordan": random.choice(["Mentions being on a call but no record exists", "Was seen near the area but insists it was a coincidence"]),
        "Taylor": random.choice(["Says they left early, but logs say otherwise", "Claims to be running errands but receipt timestamps don't match"]),
        "Casey": random.choice(["Claims store cameras were off", "Says they were dealing with a supplier, but supplier denies it"])
    }
    
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": time_window[details["time"]],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence,
        "alibis": alibis,
        "attempts": 0
    }

def chi_square_test():
    observed = np.array([random.randint(5, 15) for _ in range(5)])
    expected = np.array([10, 10, 10, 10, 10])
    chi2, p = stats.chisquare(observed, expected)
    return p < 0.05  # If True, evidence is significantly linked to a suspect

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
st.subheader("👥 Persons of Interest")
cols = st.columns(len(case["suspects"]))
for i, (name, info) in enumerate(case["suspects"].items()):
    with cols[i]:
        st.write(f"### {name}")
        st.write(f"**Occupation**: {info['occupation']}")
        st.write(f"**Connection**: {info['connection']}")
        with st.expander("Alibi"):
            st.write(case["alibis"][name])

# ---------- Evidence Board ----------
st.subheader("🔎 Compromised Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Some details may be misleading)")

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

# ---------- New Case Button ----------
if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.rerun()
