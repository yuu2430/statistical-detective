# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 3  # Default attempts
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "new_game" not in st.session_state:
    st.session_state.new_game = True
if "hints_revealed" not in st.session_state:
    st.session_state.hints_revealed = 0  # Track how many hints have been revealed

# Difficulty settings
difficulty_levels = {"Easy": 3, "Hard": 2, "Expert": 1}
difficulty = st.selectbox("Select Difficulty Level", list(difficulty_levels.keys()), key="difficulty")

# Update attempts dynamically based on difficulty
if "current_difficulty" not in st.session_state or st.session_state.current_difficulty != difficulty:
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.current_difficulty = difficulty

# Generate crime data (cached for performance)
@st.cache_data
def generate_crime_data():
    crime_types = ["Theft", "Robbery", "Assault", "Burglary", "Fraud", "Kidnapping"]
    locations = ["Manjalpur", "Fatehgunj", "Gorwa", "Makarpura"]
    data = []
    for _ in range(10):  # Generate 10 cases
        crime_time_minutes = random.randint(0, 1439)
        formatted_time = datetime.strptime(f"{crime_time_minutes // 60}:{crime_time_minutes % 60}", "%H:%M").strftime("%I:%M %p")
        crime_type = random.choice(crime_types)
        # Dynamically assign weapon based on crime type
        if crime_type == "Theft":
            weapon = random.choice(["None", "Knife"])
        elif crime_type == "Robbery":
            weapon = random.choice(["Gun", "Knife"])
        elif crime_type == "Assault":
            weapon = random.choice(["Knife", "Blunt Object"])
        elif crime_type == "Burglary":
            weapon = random.choice(["None", "Crowbar"])
        elif crime_type == "Fraud":
            weapon = "None"
        elif crime_type == "Kidnapping":
            weapon = random.choice(["None", "Gun"])
        data.append({
            "Time": formatted_time,
            "Location": random.choice(locations),
            "Crime_Type": crime_type,
            "Suspect_Age": random.randint(18, 50),
            "Suspect_Gender": random.choice(["Male", "Female", "Other"]),
            "Weapon_Used": weapon,
            "Outcome": random.choice(["Unsolved", "Solved"]),
            "Time_Minutes": crime_time_minutes
        })
    return pd.DataFrame(data)

df = generate_crime_data()

# Select a case for the player
if st.session_state.selected_case is None or st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0  # Reset hints for new case

selected_case = st.session_state.selected_case

# Investigation inputs
col1, col2, col3 = st.columns(3)
with col1:
    guessed_location = st.selectbox("Crime Location", list(location_map.keys()), key="crime_location")
with col2:
    guessed_age = st.slider("Suspect Age", 18, 50, 30, key="suspect_age")
with col3:
    guessed_gender = st.radio("Suspect Gender", ["Male", "Female", "Other"], key="suspect_gender")

guessed_gender = 0 if guessed_gender == "Male" else 1 if guessed_gender == "Female" else 2

# Submit investigation
if st.button("Submit Findings", type="primary"):
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Case Solved! You've identified the suspect! You win a sweet treat :)")
        st.balloons()
        st.session_state.score += 1  # Increase score
        st.session_state.new_game = True  # Reset the game after solving the case
    else:
        st.session_state.attempts -= 1  # Reduce attempts
        feedback = []
        if not correct_location:
            feedback.append("📍 Location doesn't match.")
        if abs(guessed_age - selected_case["Suspect_Age"]) > 5:
            feedback.append("📈 Age estimate significantly off.")
        elif guessed_age != selected_case["Suspect_Age"]:
            feedback.append("📈 Age estimate close but not exact.")
        if guessed_gender != selected_case["Suspect_Gender"]:
            feedback.append("👤 Gender mismatch.")
        
        if st.session_state.attempts > 0:
            st.error(f"🚨 Investigation Issues: {' • '.join(feedback)}")
            st.session_state.hints_revealed += 1  # Reveal more hints
        else:
            # Reveal correct answers only after attempts are exhausted
            st.error("❌ Case Closed. No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"🔢 Age: {selected_case['Suspect_Age']}")
            st.write(f"👤 Gender: {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female' if selected_case['Suspect_Gender'] == 1 else 'Other'}")
            st.session_state.new_game = True  # Reset the game after running out of attempts
            st.session_state.attempts = difficulty_levels[difficulty]  # Reset attempts for the next game

    # Rerun the app to update the state
    st.rerun()

# Reset the game if new_game is True
if st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0  # Reset hints for new case
    st.rerun()

# Manual restart button (for debugging or resetting the game)
if st.button("🔄 Restart Game (Manual Reset)"):
    st.session_state.new_game = True
    st.rerun()

# Status bar
st.caption(f"🔑 Difficulty: {difficulty} • 🔍 Attempts Left: {st.session_state.attempts}")
