def expert_system_inference(soil, ph, n_level, temp, rain, symptom):
    """
    Rule-based inference engine for Krishi Mitra expert system.
    Contains classical AI if-then rules for crop selection, fertilizer advice, and disease diagnosis.
    """
    recommendations = []
    fertilizer_advice = []
    diagnoses = []
    confidence_score = 85  # Base classical rule confidence

    # 1. Crop Selection Rules
    if soil == "Loamy" and 6.0 <= ph <= 7.5 and rain in ["Moderate", "High"]:
        recommendations.append("Rice or Wheat cultivation is ideal for this soil type and environment.")
        confidence_score += 10
    elif soil == "Sandy" and ph < 7.0:
        recommendations.append("Potatoes or Maize can be cultivated, as they thrive well in sandy soils.")
        confidence_score += 10
    elif soil == "Clay" and 5.5 <= ph <= 7.0:
        recommendations.append("Pulses (Lentils/Beans) or Mustard are suitable for this soil condition.")
        confidence_score += 10
    else:
        recommendations.append("General Recommendation: Cultivating seasonal vegetables or cucumbers is safe.")
        confidence_score -= 5

    # 2. Fertilizer Management Rules
    if n_level == "Low":
        fertilizer_advice.append("Nitrogen deficiency detected. Apply regulated amounts of Urea or organic compost.")
    elif n_level == "High":
        fertilizer_advice.append("Sufficient nitrogen present in the soil. Avoid additional fertilizer application.")
    else:
        fertilizer_advice.append("Nutrient levels are balanced. Maintain routine organic composting.")

    # 3. Disease Diagnosis & Treatment Rules
    if symptom == "Brown Spots":
        diagnoses.append("Condition: Fungal Leaf Spot / Blast Disease.")
        diagnoses.append("Treatment: Spray approved fungicides (e.g., Carbendazim) and ensure proper field drainage.")
    elif symptom == "Yellowing Leaves":
        diagnoses.append("Possible Cause: Nitrogen deficiency or waterlogging.")
        diagnoses.append("Treatment: Test soil for nitrogen levels and clear stagnant water from the field.")
    elif symptom == "Marginal Scorching":
        diagnoses.append("Possible Cause: Potassium deficiency or drought stress.")
        diagnoses.append("Treatment: Apply balanced Muriate of Potash (MOP) fertilizer and ensure regular irrigation.")
    else:
        diagnoses.append("Crops appear healthy. Continue regular field maintenance and monitoring.")

    return recommendations, fertilizer_advice, diagnoses, min(confidence_score, 98)


def get_market_forecast(crop_choice):
    """Rule-based market demand and price trend generator."""
    trends = {
        "Rice": {"demand": "High", "estimated_price": "$350 / ton", "trend": "Stable 📈"},
        "Wheat": {"demand": "Moderate", "estimated_price": "$310 / ton", "trend": "Rising 🚀"},
        "Potatoes": {"demand": "High", "estimated_price": "$220 / ton", "trend": "Fluctuating 📊"},
        "Maize": {"demand": "Moderate", "estimated_price": "$240 / ton", "trend": "Stable 📈"},
        "Pulses": {"demand": "High", "estimated_price": "$600 / ton", "trend": "Rising 🚀"},
        "Mustard": {"demand": "Moderate", "estimated_price": "$500 / ton", "trend": "Stable 📈"},
        "Seasonal Vegetables": {"demand": "Very High", "estimated_price": "Variable", "trend": "High Demand 🔥"}
    }
    return trends.get(crop_choice, {"demand": "Moderate", "estimated_price": "Standard", "trend": "Stable 📈"})