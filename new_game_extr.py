import streamlit as st
import random

st.set_page_config(layout="wide")

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
    suspects = {
        "Ravi": {"occupation": "Factory Owner", "connection": "Previously fined for illegal dumping"},
        "Priya": {"occupation": "Corporate Executive", "connection": "Launched a 'green' campaign under investigation"},
        "Arjun": {"occupation": "Truck Driver", "connection": "Frequently seen near illegal waste sites"},
        "Neha": {"occupation": "Electrician", "connection": "Worked on meters in the affected area"},
        "Vikram": {"occupation": "Real Estate Developer", "connection": "Owns land near contaminated sites"}
    }
    culprit = random.choice(list(suspects.keys()))
    evidence = {
        "Security Footage": f"A blurry figure was spotted near {details['location']} at {random.choice(['10:30 PM', '7:15 PM', '3:45 PM'])}",
        "Financial Records": f"Suspicious payments linked to {random.choice(['waste disposal', 'meter tampering', 'corporate fraud'])}",
        "Witness Statement": f"Someone saw {random.choice(['a truck unloading waste', 'a person adjusting a meter', 'documents being shredded'])}, but their memory is unclear.",
        "Digital Logs": f"Unauthorized activity detected at {details['time']} hours"
    }
    alibis = {
        suspect: random.choice([
            "Claims to have been elsewhere, but no records exist", 
            "Alibi contradicts evidence",
            "Was in the area but denies involvement"
        ]) for suspect in suspects
    }
    return {
        "crime": crime_name,
        "location": details["location"],
        "time_window": details["time"],
        "true_culprit": culprit,
        "suspects": suspects,
        "evidence": evidence,
        "alibis": alibis,
        "attempts": 0
    }

if "case" not in st.session_state:
    st.session_state.case = generate_case()
if "score" not in st.session_state:
    st.session_state.score = 0

case = st.session_state.case

st.subheader(f"🚨 Case: {case['crime']} at {case['location']}")
st.write(f"⏰ Time Window: {case['time_window']}")

st.subheader("👥 Suspects")
for name, info in case["suspects"].items():
    st.write(f"### {name}")
    st.write(f"**Occupation**: {info['occupation']}")
    st.write(f"**Connection**: {info['connection']}")
    with st.expander("Alibi"):
        st.write(case["alibis"][name])

st.subheader("🔎 Evidence")
for title, detail in case["evidence"].items():
    with st.expander(title):
        st.write(detail + " (Some details may be misleading)")

st.subheader("🕵️ Investigate and Solve")
user_guess = st.selectbox("Who is the culprit?", list(case["suspects"].keys()))
if st.button("🔒 Submit Final Answer"):
    correct = user_guess == case["true_culprit"]
    if correct:
        st.success("🎉 Correct! You solved the case and won a treat! 🍬")
        st.session_state.score += 1
        st.balloons()
    else:
        case["attempts"] += 1
        if case["attempts"] == 2:
            st.warning("❌ Incorrect! Showing probability hints.")
            # Compute probabilities based on evidence strength
            probabilities = {suspect: random.uniform(10, 80) for suspect in case["suspects"].keys()}
            probabilities[case["true_culprit"]] = random.uniform(80, 100)  # Make the actual culprit more likely
            total = sum(probabilities.values())
            probabilities = {k: round(v / total * 100, 2) for k, v in probabilities.items()}
            sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
            st.subheader("📊 Probability of Guilt")
            for suspect, prob in sorted_probs:
                st.write(f"🔹 {suspect}: {prob}%")
        elif case["attempts"] >= 3:
            st.error(f"❌ Game Over! The correct answer was {case['true_culprit']}")
        else:
            st.warning(f"❌ Incorrect! You have {3 - case['attempts']} attempt(s) left.")
    st.write(f"🏆 Your Score: {st.session_state.score}")

if st.button("🔄 New Case"):
    st.session_state.case = generate_case()
    st.rerun()
