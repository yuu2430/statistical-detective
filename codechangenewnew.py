# Submit investigation
if st.button("Submit Findings", type="primary"):
    st.session_state.attempts -= 1
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success("🎉 Case Solved! You've identified the suspect! You win a sweet treat :)")
        st.balloons()
        st.session_state.score += 1  # Increase score
        st.session_state.new_game = True  # Reset the game after solving the case
    else:
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

# Reset the game if new_game is True
if st.session_state.new_game:
    st.session_state.selected_case = df.sample(1).iloc[0]
    st.session_state.attempts = difficulty_levels[difficulty]
    st.session_state.new_game = False
    st.session_state.hints_revealed = 0  # Reset hints for new case
    st.rerun()
