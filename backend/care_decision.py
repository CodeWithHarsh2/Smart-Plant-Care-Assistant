def watering_decision(
    temperature,
    humidity,
    days_since_watered
):
    if humidity > 75 and temperature < 25:
        return {
            "action": "Delay watering",
            "reason": "High humidity and low evaporation"
        }

    if days_since_watered > 6:
        return {
            "action": "Water today",
            "reason": "Soil likely dry"
        }

    return {
        "action": "Monitor",
        "reason": "Conditions stable"
    }
