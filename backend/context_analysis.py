from plant_rules import PLANT_RULES

def analyze_context(plant_type, temperature, humidity, days_since_watered):
    insights = []
    plant = PLANT_RULES.get(plant_type.lower())

    if not plant:
        return insights

    min_t, max_t = plant["ideal_temp"]
    min_h, max_h = plant["humidity_range"]

    if temperature < min_t:
        insights.append("Cold stress likely")
    if temperature > max_t:
        insights.append("Heat stress likely")
    if humidity < min_h:
        insights.append("Low humidity stress")
    if humidity > max_h:
        insights.append("High humidity stress")

    if days_since_watered < plant["watering_days"] - 1:
        insights.append("Possible overwatering")
    if days_since_watered > plant["watering_days"] + 2:
        insights.append("Possible underwatering")

    return insights
