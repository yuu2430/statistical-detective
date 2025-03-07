import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

# --------------------------
# Game Configuration
# --------------------------
CASES = 10  # Fixed dataset size
DIFFICULTY_LEVELS = {
    "Easy": {"attempts": 3, "hints": 3, "visual": True},
    "Hard": {"attempts": 2, "hints": 2, "visual": False},
    "Expert": {"attempts": 1, "hints": 1, "visual": False}
}

# --------------------------
# Visual Mapping
# --------------------------
ICON_MAP = {
    "Male": "👨", "Female": "👩",
    "Night": "🌙", "Day": "☀️",
    "Burglary": "🔓", "Fraud": "💳",
    "Assault": "👊", "Cyber Crime": "💻"
}

COLOR_MAP = {
    "Old Town": "#FFD700", 
    "Financial District": "#32CD32",
    "Industrial Zone": "#FF4500",
    "Residential Area": "#1E90FF"
}

# --------------------------
# Data Generation
# --------------------------
@st.cache_data
def generate_crime_data():
    base_date = datetime(2024, 1, 1)
    data = {
        "Case ID": range(1, CASES+1),
        "Date": [base_date + timedelta(days=np.random.randint(0, 365)) for _ in range(CASES)],
        "Location": np.random.choice(["Old Town", "Financial District", "Industrial Zone", "Residential Area"], CASES),
        "Crime Type": np.random.choice(["Burglary", "Fraud", "Assault", "Cyber Crime"], CASES),
        "Time": [f"{h:02d}:{m:02d}" for h,m in zip(np.random.randint(0,24,CASES), np.random.randint(0,60,CASES))],
        "Suspect Age": np.clip(np.random.normal(35, 8, CASES), 18, 65).astype(int),
        "Suspect Gender": np.random.choice(["Male", "Female"], CASES, p=[0.7, 0.3])
    }
    return pd.DataFrame(data)

# --------------------------
# Interface Components
# --------------------------
def visual_data_display(df):
    st.markdown("### 🔍 Crime Map (Pattern Highlights)")
    
    # Time Category Calculation
    df['Time Category'] = df['Time'].apply(lambda x: "Night" if 20 <= int(x.split(':')[0]) < 6 else "Day")
    
    # Create visual cards
    cols = st.columns(4)
    for idx, row in df.iterrows():
        with cols[idx%4]:
            st.markdown(f"""
                <div style="border:1px solid #ddd; padding:10px; margin:5px; border-radius:8px;
                    background-color:{COLOR_MAP[row['Location']]}20;">
                    <h4>Case #{row['Case ID']}</h4>
                    <p>{ICON_MAP[row['Crime Type']]} {row['Crime Type']}</p>
                    <p>{ICON_MAP[row['Time Category']]} {row['Time']}</p>
                    <p>{ICON_MAP[row['Suspect Gender']]} {row['Suspect Age']}</p>
                </div>
            """, unsafe_allow_html=True)

def raw_data_display(df):
    st.dataframe(df.style.applymap(lambda x: f"background-color: {COLOR_MAP[x]}" if x in COLOR_MAP else "", 
                subset=['Location']), 
                use_container_width=True)

# --------------------------
# Game Core
# --------------------------
def main():
    st.set_page_config(layout="wide")
    
    # Initialize session state
    if 'game' not in st.session_state:
        st.session_state.game = {
            'target': None,
            'attempts': None,
            'hints_used': 0
        }
    
    # Difficulty Selection
    difficulty = st.sidebar.selectbox("Difficulty Level", list(DIFFICULTY_LEVELS.keys()))
    config = DIFFICULTY_LEVELS[difficulty]
    
    # Generate/Refresh Data
    df = generate_crime_data()
    if st.session_state.game['target'] is None:
        st.session_state.game.update({
            'target': df.sample(1).iloc[0],
            'attempts': config['attempts'],
            'hints_used': 0
        })
    
    # Display Interface
    st.title("🔍 Crime Solver Network")
    
    if config['visual']:
        visual_data_display(df)
        st.sidebar.markdown("### 🕵️ Pattern Assistant")
        st.sidebar.write(f"🔻 Most common location: {df['Location'].mode()[0]}")
        st.sidebar.write(f"🔻 Frequent crime time: {stats.mode(pd.to_datetime(df['Time']).dt.hour)[0][0]}:00")
    else:
        raw_data_display(df)
    
    # Game Controls
    # ... (maintain previous game logic for hints/guesses) ...

if __name__ == "__main__":
    main()
