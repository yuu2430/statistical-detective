if st.button("Submit Guess", key="submit_guess"):
    correct_location = guessed_location == selected_case["Location"]
    correct_age = guessed_age == selected_case["Suspect_Age"]
    correct_gender = guessed_gender == selected_case["Suspect_Gender"]
    
    if correct_location and correct_age and correct_gender:
        st.success(f"\U0001F389 Correct! You've solved the case. Reward: You win a sweet treat! yay!")
    else:
        st.session_state.attempts -= 1
        feedback = []
        if not correct_location:
            feedback.append("The location probability suggests another area...")
        if not correct_age:
            feedback.append("The age probability doesn't align with the data...")
        if not correct_gender:
            feedback.append("Gender statistics indicate a different suspect...")
        
        if st.session_state.attempts > 0:
            st.error("\U0001F480 Not quite! " + " ".join(feedback) + f" Attempts left: {st.session_state.attempts}")
        else:
            # Reveal the correct answer when attempts are exhausted
            st.error("\U0001F480 No attempts left! The correct answer was:")
            st.write(f"📍 Location: {selected_case['Location']}")
            st.write(f"\U0001F575 Age: {selected_case['Suspect_Age']}")
            st.write(f"👤 Gender: {'Male' if selected_case['Suspect_Gender'] == 0 else 'Female'}")
