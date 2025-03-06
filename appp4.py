import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

st.set_page_config(layout='wide')

# ---------- Game Setup ----------
st.title('🕵️ Detective Game: AI & Puzzles Edition')
st.write('Welcome to the ultimate detective challenge! Interrogate suspects, analyze clues, and solve puzzles to catch the culprit.')

# ---------- Crime Report Setup ----------
crime_reports = [
    '🔍 A robbery was reported at a mall. The suspect was last seen near the food court.',
    '🔥 A mysterious arson case occurred in an industrial area at midnight. Witnesses reported a shadowy figure.',
    '💰 A burglary took place in the suburbs. The suspect fled on foot before police arrived.',
    '📞 A fraud case was reported downtown. The victim lost thousands due to an online scam.',
]

# ---------- Generate Crime Data ----------
@st.cache_data
def generate_crime_data():
    locations = ['Downtown', 'City Park', 'Suburbs', 'Industrial Area', 'Mall']
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 2, 1)
    for i in range(1, 6):
        crime_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f'{crime_time_minutes // 60}:{crime_time_minutes % 60}', '%H:%M').strftime('%I:%M %p')
        data.append({
            'Case_ID': i,
            'Crime_Report': random.choice(crime_reports),
            'Date': crime_date.strftime('%Y-%m-%d'),
            'Time': formatted_time,
            'Location': random.choice(locations),
            'Suspect_Name': random.choice(['John', 'Sarah', 'Mike', 'Emma', 'David']),
            'Suspect_Age': random.randint(18, 50),
            'Suspect_Gender': random.choice(['Male', 'Female']),
            'Weapon_Used': random.choice(['Knife', 'Gun', 'None']),
            'Outcome': random.choice(['Unsolved', 'Solved']),
        })
    return pd.DataFrame(data)

# Generate the crime data
df = generate_crime_data()

# ---------- Select a Random Case ----------
if 'selected_case' not in st.session_state:
    st.session_state.selected_case = df.sample(1).iloc[0]
selected_case = st.session_state.selected_case

st.subheader('📜 Crime Report:')
st.write(selected_case['Crime_Report'])
st.write(f'📅 Date: {selected_case['Date']} | ⏰ Time: {selected_case['Time']} | 📍 Location: {selected_case['Location']}')

# ---------- Multi-Layered Suspect Profiles ----------
def generate_suspects(case):
    """Generate detailed suspect profiles with multiple layers of background and motives."""
    background_info = {
        'John': 'Has a history of petty theft but no major crimes.',
        'Sarah': 'Worked as a security guard at a local mall.',
        'Mike': 'Recently lost his job and has mounting financial troubles.',
        'Emma': 'A quiet person with few friends; often keeps to herself.',
        'David': 'Well-known in the community for charity work.'
    }
    motives = {
        'John': 'Recently accused of a theft incident near the crime scene.',
        'Sarah': 'Had a dispute with her employer the day before the crime.',
        'Mike': 'Financial desperation could be a motive for burglary.',
        'Emma': 'Suspicious absence from work on the day of the crime.',
        'David': 'Caught in a legal battle over property ownership.'
    }
    alibis = {
        'John': 'Claimed to have been at a local diner around the time of the crime.',
        'Sarah': 'Stated she was on a late shift at the mall.',
        'Mike': 'Said he was visiting a friend in a nearby town.',
        'Emma': 'Insisted she was at home, reading all evening.',
        'David': 'Mentioned he was out running errands.'
    }

    culprit_name = case['Suspect_Name']
    culprit = {
        'Name': culprit_name,
        'Age': case['Suspect_Age'],
        'Gender': case['Suspect_Gender'],
        'Role': 'Culprit',
        'Background': background_info.get(culprit_name, 'No background information available.'),
        'Motive': motives.get(culprit_name, 'Unknown motive.'),
        'Alibi': alibis.get(culprit_name, 'No alibi provided.'),
    }

    all_names = list(background_info.keys())
    decoy_names = [name for name in all_names if name != culprit_name]
    random.shuffle(decoy_names)  # Randomize order

    decoys = []
    for i in range(3):  # More decoys for complexity
        name = decoy_names[i]
        decoys.append({
            'Name': name,
            'Age': random.randint(18, 50),
            'Gender': random.choice(['Male', 'Female']),
            'Role': 'Decoy',
            'Background': background_info.get(name, 'No background information available.'),
            'Motive': motives.get(name, 'Unknown motive.'),
            'Alibi': alibis.get(name, 'No alibi provided.'),
        })

    return [culprit] + decoys

if 'suspects' not in st.session_state:
    st.session_state.suspects = generate_suspects(selected_case)

st.subheader('👥 Suspect Profiles')
for suspect in st.session_state.suspects:
    st.write(f'**{suspect['Name']}** | Age: {suspect['Age']} | Gender: {suspect['Gender']}')
    st.write(f'_Background_: {suspect['Background']}')
    st.write(f'_Motive_: {suspect['Motive']}')
    st.write(f'_Alibi_: {suspect['Alibi']}')
    st.markdown('---')

# ---------- Interactive Evidence Board with Red Herrings ----------
st.subheader('🔎 Evidence Board')
# Define clues and add extra layers of complexity
ambiguous_clues = [
    {'title': 'Fingerprint Analysis', 'detail': 'Multiple fingerprint matches at the scene.'},
    {'title': 'DNA Sample', 'detail': 'DNA found, but it overlaps with several suspects.'},
    {'title': 'CCTV Footage', 'detail': 'Blurry footage of a figure, unclear identity.'},
    {'title': 'Forensic Report', 'detail': 'Unusual traces found at the scene, possibly related to chemical substances.'},
    {'title': 'Time-stamped Call', 'detail': 'Suspicious call made near the crime scene, but caller’s voice is distorted.'},
    {'title': 'Mysterious Note', 'detail': 'A cryptic note left behind. Could be a clue or a misdirection.'},
]
random.shuffle(ambiguous_clues)
for item in ambiguous_clues:
    with st.expander(item['title']):
        st.write(item['detail'])

# ---------- Timeline of Events ----------
st.subheader('🕰️ Timeline of Events')
timeline = [
    {'time': selected_case['Time'], 'event': 'Crime reported.'},
    {'time': '11:30 PM', 'event': 'Suspicious call reported near the area.'},
    {'time': '11:45 PM', 'event': 'CCTV captures multiple figures near the area.'},
    {'time': '12:15 AM', 'event': 'Forensics team arrives, traces found.'},
    {'time': '12:30 AM', 'event': 'Passerby reports a figure near the scene.'},  # Red herring event
]
timeline = sorted(timeline, key=lambda x: x['time'])
for event in timeline:
    st.write(f'**{event['time']}**: {event['event']}')

# ---------- Enhanced Interrogation Mechanics ----------
st.subheader('🗣️ Interrogate Suspects')
questions = [
    'Where were you last night?',
    'Do you know the victim?',
    'What were you doing at the crime scene?',
    'Can anyone verify your alibi?', 
