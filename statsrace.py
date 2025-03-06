import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

def roll_die():
    return random.randint(1, 6)

def initialize_game():
    st.session_state.positions = [0] * st.session_state.num_cars
    st.session_state.energy_used = {i: 0 for i in range(st.session_state.num_cars)}
    st.session_state.dice_rolls = {i: [] for i in range(st.session_state.num_cars)}
    st.session_state.game_over = False
    st.session_state.winner = None

def roll_and_update():
    if not st.session_state.game_over:
        for i in range(st.session_state.num_cars):
            roll = roll_die()
            st.session_state.positions[i] += roll
            st.session_state.dice_rolls[i].append(roll)
            st.session_state.energy_used[i] += roll * st.session_state.car_efficiency[st.session_state.car_types[i]]
            
            if st.session_state.positions[i] >= st.session_state.finish_line:
                st.session_state.game_over = True
                st.session_state.winner = f"Car {i+1} ({st.session_state.car_types[i]})"  
                break

def visualize_race():
    fig, ax = plt.subplots()
    ax.barh(range(st.session_state.num_cars), st.session_state.positions, color='blue')
    ax.set_yticks(range(st.session_state.num_cars))
    ax.set_yticklabels([f"Car {i+1}" for i in range(st.session_state.num_cars)])
    ax.set_xlabel("Position")
    ax.set_title("Race Progress")
    st.pyplot(fig)

def visualize_stats():
    if not any(st.session_state.dice_rolls.values()):
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    # Dice Roll Distribution
    all_rolls = [roll for rolls in st.session_state.dice_rolls.values() for roll in rolls]
    axes[0].hist(all_rolls, bins=range(1, 8), align='left', rwidth=0.8, color='blue')
    axes[0].set_xticks(range(1, 7))
    axes[0].set_xlabel("Dice Roll Outcome")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Dice Roll Distribution")
    
    # Energy Consumption
    axes[1].bar(range(st.session_state.num_cars), st.session_state.energy_used.values(), tick_label=[f"Car {i+1}" for i in st.session_state.energy_used.keys()], color='green')
    axes[1].set_xlabel("Car Number")
    axes[1].set_ylabel("Total Energy Used")
    axes[1].set_title("Energy Consumption by Car Type")
    
    plt.tight_layout()
    st.pyplot(fig)

def reset_game():
    st.session_state.clear()
    st.rerun()

def main():
    st.title("Sustainable Car Racing Game")
    
    if "setup_complete" not in st.session_state:
        st.session_state.num_cars = st.number_input("Enter number of cars:", min_value=2, max_value=10, value=3, step=1)
        st.session_state.finish_line = st.number_input("Enter finish line position:", min_value=10, max_value=100, value=30, step=5)
        
        car_types = []
        for i in range(st.session_state.num_cars):
            car_types.append(st.selectbox(f"Choose type for Car {i+1}", ["electric", "petrol", "diesel"], key=f"car_{i}"))
        
        if st.button("Start Game"):
            st.session_state.car_types = car_types
            st.session_state.car_efficiency = {"electric": 0.5, "petrol": 1.5, "diesel": 2.0}
            initialize_game()
            st.session_state.setup_complete = True
            st.rerun()
    else:
        st.subheader("Race Progress")
        visualize_race()
        
        if st.button("Roll Dice & Move!") and not st.session_state.game_over:
            roll_and_update()
        
        if st.session_state.game_over:
            st.success(f"{st.session_state.winner} wins the race!")
            visualize_stats()
        
        if st.button("New Game"):
            reset_game()
    
if __name__ == "__main__":
    main()
