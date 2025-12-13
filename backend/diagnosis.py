from utils import open_image_to_array, yellow_ratio, brown_spot_ratio

def diagnose_from_image(path):
    """Return a list of probable issues and simple confidence scores."""
    img, arr = open_image_to_array(path)
    y = yellow_ratio(arr)
    b = brown_spot_ratio(arr)

    results = []
    if y > 0.08:
        results.append({
            'issue': 'Yellow leaves or chlorosis',
            'probability': min(0.95, 0.4 + y * 4),
            'advice': [
                'Check for overwatering or nutrient deficiency',
                'Ensure plant gets enough sunlight but not scorching sun',
                'Consider balanced liquid fertilizer once every 3-4 weeks'
            ]
        })

    if b > 0.02:
        results.append({
            'issue': 'Leaf spots or pest damage',
            'probability': min(0.95, 0.3 + b * 8),
            'advice': [
                'Inspect underside of leaves for pests',
                'Remove heavily infected leaves',
                'Treat with neem oil spray or mild insecticidal soap'
            ]
        })

    if not results:
        results.append({
            'issue': 'Healthy-looking or unclear image',
            'probability': 0.6,
            'advice': [
                'Image did not show strong signs of problems',
                'Try another photo with closer framing of effected leaves',
                'Or describe symptoms in text for symptom-based diagnosis'
            ]
        })

    return results

# Symptom-based rules
def diagnose_from_text(symptom_text):
    s = symptom_text.lower()
    results = []
    if 'yellow' in s or 'chlorosis' in s:
        results.append({
            'issue': 'Yellow leaves or nutrient deficiency',
            'probability': 0.8,
            'advice': [
                'Check watering schedule and soil moisture',
                'Fertilize with balanced NPK lightly',
            ]
        })
    if 'spots' in s or 'brown' in s or 'holes' in s:
        results.append({
            'issue': 'Leaf spots or pest damage',
            'probability': 0.8,
            'advice': [
                'Inspect leaves and treat for pests',
                'Remove badly infected leaves'    
            ]
        })
    if 'droop' in s or 'wilting' in s:
        results.append({
            'issue': 'Underwatering or root problems',
            'probability': 0.8,
            'advice': [
                'Check soil moisture',
                'Water deeply but allow drainage'    
            ]
        })
    if not results:
        results.append({
            'issue': 'Unclear. Ask for more details',
            'probability': 0.5,
            'advice': ['Provide more details such as watering frequency, recent changes, and a close photo']
        })
    return results
