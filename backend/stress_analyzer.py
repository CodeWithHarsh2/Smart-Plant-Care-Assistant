def compute_stress_factors(
    visual_confidence,
    temperature,
    humidity,
    days_since_watered
):
    stress = {}

    # Water stress
    if days_since_watered < 2:
        stress["water"] = "High"
    elif days_since_watered > 7:
        stress["water"] = "Medium"
    else:
        stress["water"] = "Low"

    # Heat stress
    if temperature > 32:
        stress["heat"] = "High"
    elif temperature > 26:
        stress["heat"] = "Medium"
    else:
        stress["heat"] = "Low"

    # Humidity stress
    if humidity > 80 or humidity < 35:
        stress["humidity"] = "High"
    else:
        stress["humidity"] = "Low"

    # Disease risk (from image confidence)
    if visual_confidence < 0.6:
        stress["disease"] = "Medium"
    else:
        stress["disease"] = "Low"

    return stress
