import streamlit as st
import random

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
        st.success("Amazing! You got all 5 correct!")
    else:
        st.warning("Game Over! The correct category was: " + st.session_state.correct_category)
    st.write("Thanks for playing! :)")
    if st.button("New Game"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.current_item, st.session_state.correct_category = get_waste_item()
        st.rerun()
