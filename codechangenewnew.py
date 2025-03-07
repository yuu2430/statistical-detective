@st.cache_data
def generate_crime_data():
    # Create logical patterns
    patterns = {
        "Burglary": {
            "locations": ["Residential Area", "Old Town"],
            "time_range": (20, 6),  # 8PM-6AM
            "age_range": (25, 45),
            "gender_bias": {"Male": 0.8, "Female": 0.2}
        },
        "Fraud": {
            "locations": ["Financial District", "Old Town"],
            "time_range": (9, 17),  # 9AM-5PM
            "age_range": (35, 55),
            "gender_bias": {"Male": 0.4, "Female": 0.6}
        },
        "Assault": {
            "locations": ["Industrial Zone", "Old Town"],
            "time_range": (18, 23),  # 6PM-11PM
            "age_range": (20, 40),
            "gender_bias": {"Male": 0.85, "Female": 0.15}
        },
        "Cyber Crime": {
            "locations": ["Financial District", "Residential Area"],
            "time_range": (12, 4),  # 12PM-4AM
            "age_range": (18, 35),
            "gender_bias": {"Male": 0.7, "Female": 0.3}
        }
    }

    cases = []
    for case_id in range(1, 11):
        crime_type = random.choice(list(patterns.keys()))
        pattern = patterns[crime_type]
        
        # Generate logically connected data
        location = random.choice(pattern["locations"])
        
        # Time generation based on pattern
        start_hour, end_hour = pattern["time_range"]
        hour = random.randint(start_hour, end_hour) % 24
        minute = random.choice(["00", "15", "30", "45"])
        time = f"{hour:02d}:{minute}"
        
        # Age generation with pattern-based distribution
        age = int(np.clip(np.random.normal(
            sum(pattern["age_range"])/2,  # Mean of range
            (pattern["age_range"][1] - pattern["age_range"][0])/6  # Std dev
        ), 18, 65))
        
        # Gender selection with pattern bias
        gender = random.choices(
            list(pattern["gender_bias"].keys()),
            weights=list(pattern["gender_bias"].values())
        )[0]

        cases.append({
            "Case_ID": case_id,
            "Date": (datetime(2024, 1, 1) + 
                    timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            "Location": location,
            "Crime_Type": crime_type,
            "Time": time,
            "Suspect_Age": age,
            "Suspect_Gender": gender
        })

    return pd.DataFrame(cases)
