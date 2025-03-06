import streamlit as st
import random
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def get_waste_item():
    """Returns a random waste item and its correct category."""
    waste_items = {
        "Plastic Bottle": "Recycling",
        "Banana Peel": "Composting",
        "Aluminum Can": "Recycling",
        "Glass Jar": "Recycling",
        "Pizza Box (Greasy)": "Composting",
        "Paper Cup": "Composting",
        "Styrofoam Container": "Landfill",
        "Metal Spoon": "Recycling",
        "Tea Bag": "Composting",
        "Chip Bag": "Landfill",
        "Cardboard Box": "Recycling",
        "Cotton Cloth": "Organic Waste",
        "Plastic Straw": "Landfill",
        "Egg Shells": "Composting",
        "Old Newspaper": "Recycling",
        "Expired Medication": "Hazardous Waste",
        "Wooden Chopsticks": "Composting",
        "Broken Mirror": "Landfill",
        "Milk Carton": "Recycling"
    }
    item = random.choice(list(waste_items.keys()))
    return item, waste_items[item]

def save_data(waste_item, user_choice, correct_category):
    """Save the game data to a CSV file in the current working directory."""
    file_name = "waste_sorting_data.csv"
    data = pd.DataFrame([[waste_item, user_choice, correct_category, user_choice == correct_category]], 
                         columns=["Waste Item", "User Choice", "Correct Category", "Correct"])
    
    if os.path.exists(file_name):
        data.to_csv(file_name, mode='a', header=False, index=False)
    else:
        data.to_csv(file_name, mode='w', header=True, index=False)

def show_statistics():
    """Display player performance statistics from the CSV file."""
    file_name = "waste_sorting_data.csv"
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        accuracy = df.groupby("Waste Item")["Correct"].mean() * 100
        
        st.write("### Player Performance Stats:")
        st.bar_chart(accuracy)

st.title("Waste Sorting Challenge")

st.write("Sort the waste item into the correct category: Recycling, Composting, Landfill, Hazardous Waste, or Organic Waste.")

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'current_item' not in st.session_state:
    st.session_state.current_item, st.session_state.correct_category = get_waste_item()
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

if not st.session_state.game_over:
    st.subheader(f"Waste Item: {st.session_state.current_item}")
    user_choice = st.radio("Choose the correct category:", ["Recycling", "Composting", "Landfill", "Hazardous Waste", "Organic Waste"], key=st.session_state.attempts)
    
    if st.button("Submit") and not st.session_state.game_over:
        save_data(st.session_state.current_item, user_choice, st.session_state.correct_category)
        
        if user_choice == st.session_state.correct_category:
            st.success("Correct! Well done.")
            st.session_state.score += 1
            st.session_state.attempts += 1
            
            if st.session_state.score < 5:
                st.session_state.current_item, st.session_state.correct_category = get_waste_item()
            else:
                st.session_state.game_over = True
        else:
            st.error(f"Incorrect. The correct category is {st.session_state.correct_category}.")
            st.session_state.game_over = True
        
        st.rerun()
    
st.write(f"Score: {st.session_state.score}/5")

if st.session_state.game_over:
    if st.session_state.score == 5:
        st.success("Amazing! You got all 5 correct! You win a toffee! hooray! yayy >v</")
    else:
        st.warning("Game Over! The correct category was: " + st.session_state.correct_category)
    st.write("Thanks for playing! :)")
    show_statistics()
    if st.button("New Game"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.current_item, st.session_state.correct_category = get_waste_item()
        st.rerun()
