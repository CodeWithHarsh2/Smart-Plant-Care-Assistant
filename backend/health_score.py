def clamp(val, minv=0, maxv=100):
    return max(min(val, maxv), minv)

def compute_health_score(
    visual_confidence,
    watering_score,
    weather_score,
    plant_match_score
):
    score = (
        0.35 * visual_confidence +
        0.25 * watering_score +
        0.25 * weather_score +
        0.15 * plant_match_score
    ) * 100

    return clamp(round(score))
