def predict_risk(context_insights):
    if "Possible overwatering" in context_insights and "High humidity stress" in context_insights:
        return "High risk of root rot in 7–10 days"
    if "Possible underwatering" in context_insights:
        return "Risk of wilting in 3–5 days"
    return "No immediate critical risk"
