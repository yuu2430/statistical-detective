import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from scipy import stats

# Initialize Streamlit configuration first
st.set_page_config(
    page_title="🔍 Vadodara Crime Solver",
    page_icon="🕵️",
    layout="wide"
)

os.environ["OMP_NUM_THREADS"] = "1"

# Updated Nature-inspired Color Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f0e6;
        color: #4f2022;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #9a816b !important;
        color: #ffffff !important;
        border-radius: 5px !important;
    }
    .stSlider div[data-testid="stThumbValue"] {
        color: #4f2022 !important;
    }
    .stSlider div[data-baseweb="slider"] {
        background-color: #acdb0130;
    }
    .stRadio div[role="radiogroup"] {
        background-color: #ffffff !important;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #9a816b;
    }
    .stButton>button {
        background-color: #65b1df !important;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 10px 24px;
        border: 2px solid #4f2022;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4f2022 !important;
        transform: scale(1.05);
    }
    .stSuccess {
        background-color: #acdb01 !important;
        color: #4f2022 !important;
        border: 1px solid #9a816b;
    }
    .stError {
        background-color: #9a816b !important;
        color: #ffffff !important;
        border: 1px solid #4f2022;
    }
    .dataframe {
        background-color: #ffffff !important;
        border: 2px solid #9a816b !important;
    }
    .dataframe th {
        background-color: #acdb01 !important;
        color: #4f2022 !important;
    }
    .dataframe td {
        background-color: #ffffff !important;
        color: #4f2022 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ... [Keep ALL the rest of the code EXACTLY AS IS from previous version] ...
# ... [All game mechanics, data generation, and logic remain unchanged] ...
# ... [Maintain EXACT SAME code from previous implementation below this line] ...
