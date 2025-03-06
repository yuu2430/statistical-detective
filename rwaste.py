import streamlit as st
import random
import pandas as pd
import os

def get_waste_item():
    """Returns a random waste item and its correct category."""
    waste_items = {
        "Plastic Bottle": "Recyclable",
        "Banana Peel": "Compostable",
        "Aluminum Can": "Recyclable",
        "Glass Jar": "Recyclable",
        "Pizza Box (Greasy)": "Compostable",
        "Paper Cup": "Compostable",
        "Styrofoam Container": "Non-Recyclable",
        "Metal Spoon": "Recyclable",
        "Tea Bag": "Compostable",
        "Chip Bag": "Non-Recyclable",
        "Cardboard Box": "Recyclable",
        "Cotton Cloth": "Compostable",
        "Plastic Straw": "Non-Recyclable",
        "Egg Shells": "Compostable",
        "Old Newspaper": "Recyclable",
        "Expired Medication": "Non-Recyclable",
        "Wooden Chopsticks": "Compostable",
        "Broken Mirror": "Non-Recyclable",
        "Milk Carton": "Recyclable"
    }
    item = random.choice(list(waste_items.keys()))
    return item, waste_items[item]

def save_data(waste_item, user_choice, correct_category):
    """Save the game data to a CSV file."""
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
        for item, acc in accuracy.items():
            st.write(f"{item}: {acc:.2f}% correct")

def show_leaderboard():
    """Display percentile ranking of players."""
    file_name = "waste_sorting_data.csv"
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        total_games = df.groupby("User Choice")["Correct"].count()
        correct_games = df.groupby("User Choice")["Correct"].sum()
        accuracy = (correct_games / total_games * 100).fillna(0)
        percentile_rank = accuracy.rank(pct=True) * 100
        st.write("### Leaderboard - Accuracy Percentile:")
        for player, rank in percentile_rank.items():
            st.write(f"{player}: {rank:.2f} percentile")

st.title("Statistical Waste Sorting Challenge")

st.write("Sort the waste item into the correct category: Recyclable, Compostable, or Non-Recyclable.")

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
    user_choice = st.radio("Choose the correct category:", ["Recyclable", "Compostable", "Non-Recyclable"], key=st.session_state.attempts)
    
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
        st.success("Amazing! You got all 5 correct! Want to play again?")
    else:
        st.warning("Game Over! The correct category was: " + st.session_state.correct_category)
    st.write("Thanks for playing! :)")
    show_statistics()
    show_leaderboard()
    if st.button("New Game"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.current_item, st.session_state.correct_category = get_waste_item()
        st.rerun()
