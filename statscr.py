import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")

# ---------- Game Setup ----------
st.title("🕵️ Statistical Detective: AI to the Rescue")
st.write("Solve the crime by analyzing clues, interrogating multiple suspects, and using AI insights!")

# ---------- Crime Report Setup ----------
crime_reports = [
    "🔍 A robbery was reported at a mall. The suspect was last seen near the food court.",
    "🔥 A mysterious arson case occurred in an industrial area at midnight. Witnesses saw a shadowy figure.",
    "💰 A burglary took place in the suburbs. The suspect fled on foot before police arrived.",
    "📞 A fraud case was reported downtown. The victim lost thousands due to an online scam.",
]

# ---------- Generate Crime Data ----------
@st.cache_data
def generate_crime_data():
    crime_types = ["Robbery", "Assault", "Burglary", "Fraud", "Arson"]
    locations = ["Downtown", "City Park", "Suburbs", "Industrial Area", "Mall"]
    data = []
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    
    for i in range(1, 6):
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        
        data.append({
            "Case_ID": i,
            "Crime_Report": random.choice(crime_reports),
            "Date": crime_date.strftime('%Y-%m-%d'),
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Suspect_Name": random.choice(["John", "Sarah", "Mike", "Emma", "David"]),
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female"]),
            "Weapon_Used": random.choice(["Knife", "Gun", "None"]),
            "Outcome": random.choice(["Unsolved", "Solved"]),
        })
    
    return pd.DataFrame(data)

df = generate_crime_data()

# ---------- Select a Random Case ----------
if "selected_case" not in st.session_state:
    st.session_state.selected_case = df.sample(1).iloc[0]
selected_case = st.session_state.selected_case

st.subheader("📜 Crime Report:")
st.write(selected_case["Crime_Report"])
st.write(f"📅 Date: {selected_case['Date']} | ⏰ Time: {selected_case['Time']} | 📍 Location: {selected_case['Location']}")

# ---------- Enriched Suspect Profiles ----------
def generate_suspects(case):
    """Generate a list of suspect profiles with detailed backgrounds and alibis."""
    background_info = {
        "John": "Has a history of petty theft but no major crimes.",
        "Sarah": "Worked as a security guard at a local mall.",
        "Mike": "Recently lost his job and has financial troubles.",
        "Emma": "A quiet person with few friends; often keeps to herself.",
        "David": "Well-known in the community for charity work."
    }
    alibis = {
        "John": "Claimed to have been at a local diner around the time of the crime.",
        "Sarah": "Stated she was on a late shift at the mall.",
        "Mike": "Said he was visiting a friend in a nearby town.",
        "Emma": "Insisted she was at home, reading all evening.",
        "David": "Mentioned he was out running errands."
    }

    culprit_name = case["Suspect_Name"]
    culprit = {
        "Name": culprit_name,
        "Age": case["Suspect_Age"],
        "Gender": case["Suspect_Gender"],
        "Role": "Culprit",
        "Background": background_info.get(culprit_name, "No background information available."),
        "Alibi": alibis.get(culprit_name, "No alibi provided."),
    }

    all_names = list(background_info.keys())
    decoy_names = [name for name in all_names if name != culprit_name]
    random.shuffle(decoy_names)  # Randomize order

    decoys = []
    for i in range(2):
        name = decoy_names[i]
        decoys.append({
            "Name": name,
            "Age": random.randint(18, 50),
            "Gender": random.choice(["Male", "Female"]),
            "Role": "Decoy",
            "Background": background_info.get(name, "No background information available."),
            "Alibi": alibis.get(name, "No alibi provided."),
        })

    return [culprit] + decoys

if "suspects" not in st.session_state:
    st.session_state.suspects = generate_suspects(selected_case)

st.subheader("👥 Suspect List")
for suspect in st.session_state.suspects:
    st.write(f"**{suspect['Name']}** | Age: {suspect['Age']} | Gender: {suspect['Gender']}")
    st.write(f"_Background_: {suspect['Background']}")
    st.write(f"_Alibi_: {suspect['Alibi']}")
    st.markdown("---")

# ---------- Interactive Evidence Board ----------
st.subheader("🔎 Evidence Board")
# Evidence items include forensic clues and timeline hints.
evidence_items = [
    {"title": "Fingerprint Analysis", "detail": "The fingerprints found on the crime scene match a known profile."},
    {"title": "DNA Sample", "detail": "A partial DNA match was found, suggesting the suspect has been at the scene before."},
    {"title": "CCTV Footage", "detail": f"Footage shows a figure resembling {st.session_state.suspects[0]['Name']} near the location."},
    {"title": "Time-stamped Call", "detail": "A call was placed at the time of the crime, possibly linking a suspect."},
]

for item in evidence_items:
    with st.expander(item["title"]):
        st.write(item["detail"])

# ---------- Timeline of Events ----------
st.subheader("🕰️ Timeline of Events")
timeline = [
    {"time": selected_case["Time"], "event": "Crime reported at the scene."},
    {"time": "11:30 PM", "event": "A suspicious call was made."},
    {"time": "11:45 PM", "event": "CCTV captures a potential suspect near the area."},
    {"time": "12:15 AM", "event": "Forensic team arrives at the scene."},
]
for event in timeline:
    st.write(f"**{event['time']}**: {event['event']}")

# ---------- Enhanced Interrogation Mechanics ----------
st.subheader("🗣️ Interrogate Suspects")
question_list = [
    "Where were you last night?",
    "Do you know the victim?",
    "What were you doing at the crime scene?"
]

responses = {
    "Where were you last night?": {
        "Culprit": {"answer": "I was at home... though I did step out for a bit.", "cue": "😬 (Avoiding eye contact)"},
        "Decoy": {"answer": "I was home with my family all night.", "cue": "🙂 (Confident)"},
    },
    "Do you know the victim?": {
        "Culprit": {"answer": "I barely knew the victim.", "cue": "😶 (Hesitant)"},
        "Decoy": {"answer": "Yes, we used to work together.", "cue": "😊 (Relaxed)"},
    },
    "What were you doing at the crime scene?": {
        "Culprit": {"answer": "I was just passing by, nothing more.", "cue": "😕 (Uncertain)"},
        "Decoy": {"answer": "I wasn't anywhere near that area.", "cue": "😎 (Calm)"},
    }
}

suspect_names = [s["Name"] for s in st.session_state.suspects]
selected_suspect_name = st.selectbox("Select a suspect to interrogate:", suspect_names, key="suspect_select")
selected_suspect = next(s for s in st.session_state.suspects if s["Name"] == selected_suspect_name)
selected_question = st.selectbox("Select a question to ask:", question_list, key="question_select")

if st.button("🎙️ Ask Question"):
    role = selected_suspect["Role"]
    reply = responses[selected_question][role]
    st.write(f"🕵️ {selected_suspect['Name']} answers: {reply['answer']} {reply['cue']}")

# ---------- AI-Assisted Crime Pattern Detection ----------
st.subheader("📊 AI Crime Analysis")
location_map = {"Downtown": 0, "City Park": 1, "Suburbs": 2, "Industrial Area": 3, "Mall": 4}
df["Location_Code"] = df["Location"].map(location_map)

weapon_map = {"Knife": 0, "Gun": 1, "None": 2}
df["Weapon_Code"] = df["Weapon_Used"].map(weapon_map)

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df['Cluster'] = kmeans.fit_predict(df[["Location_Code", "Weapon_Code"]])
df['Cluster_Location'] = df['Cluster'].map({0: "Hotspot A", 1: "Hotspot B", 2: "Hotspot C"})

zone_hint = df[df['Location'] == selected_case['Location']]['Cluster_Location'].values[0]
st.write(f"📍 Crime Zone: {zone_hint}")
st.write("📈 AI analysis indicates this area has a high probability of recurring crimes.")

# ---------- Make the Final Guess ----------
st.subheader("🕵️‍♂️ Make Your Final Guess")
final_guess = st.selectbox("Who is the culprit?", suspect_names, key="final_guess")
if st.button("🚔 Submit Arrest Warrant"):
    culprit = next(s for s in st.session_state.suspects if s["Role"] == "Culprit")
    if final_guess == culprit["Name"]:
        st.success(f"🎉 You solved the case! {culprit['Name']} has been arrested.")
    else:
        st.error("❌ Wrong suspect! The real culprit is still at large. Re-examine the clues and interrogations.")

# ---------- Restart Game ----------
if st.button("🔄 New Case"):
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.suspects = generate_suspects(st.session_state.selected_case)
    st.experimental_rerun()
