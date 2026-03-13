import math

# -----------------------------
# LSI CALCULATION
# -----------------------------
def calculate_LSI(pH, TDS, temp, calcium, alkalinity):
    """
    Calculates Langelier Saturation Index (LSI)
    Positive LSI → Scaling, Negative LSI → Corrosion
    """
    A = (math.log10(TDS) - 1) / 10
    B = -13.12 * math.log10(temp + 273) + 34.55
    C = math.log10(calcium) - 0.4
    D = math.log10(alkalinity)
    pHs = (9.3 + A + B) - (C + D)
    return round(pH - pHs, 2)

# -----------------------------
# LARSON INDEX
# -----------------------------
def larson_index(chloride, sulfate, alkalinity):
    """
    Larson Index → Predicts corrosion risk from chloride & sulfate
    """
    return round((chloride + sulfate) / alkalinity, 2)

# -----------------------------
# RISK DETECTION
# -----------------------------
def detect_risk(data):
    """
    Evaluates water chemistry risks:
    - Scaling
    - Corrosion
    - Chloride corrosion
    """
    risks = []
    causes = []

    LSI = data["LSI"]
    larson = data["Larson"]

    # -----------------------------
    # Scaling
    # -----------------------------
    if LSI > 1.5:
        risks.append("Severe Scaling")
        causes.append("High calcium and alkalinity leading to heavy scale formation")
    elif LSI > 0.8:
        risks.append("Moderate Scaling")
        causes.append("Moderate hardness and alkalinity may cause scale")
    
    # -----------------------------
    # Corrosion
    # -----------------------------
    if LSI < -1.0:
        risks.append("Severe Corrosion")
        causes.append("Highly aggressive water, very low alkalinity")
    elif LSI < -0.5:
        risks.append("Moderate Corrosion")
        causes.append("Mildly aggressive water, low alkalinity")

    # -----------------------------
    # Chloride corrosion
    # -----------------------------
    if larson > 2.0:
        risks.append("Severe Chloride Corrosion")
        causes.append("High chloride & sulfate concentrations")
    elif larson > 1.5:
        risks.append("Moderate Chloride Corrosion")
        causes.append("Moderate chloride & sulfate levels")

    # -----------------------------
    # Balanced / Normal
    # -----------------------------
    if not risks:
        risks.append("Normal")
        causes.append("Water chemistry is balanced")

    return risks, causes

# -----------------------------
# DEVIATION CALCULATION
# -----------------------------
def calculate_deviation(actual, predicted):
    if actual == 0:
        return 0
    return abs(predicted - actual) / actual * 100

def calculate_all_deviations(actual_values, predicted_values):
    deviations = {}
    for key in actual_values:
        if key in predicted_values:
            deviations[key] = round(
                calculate_deviation(actual_values[key], predicted_values[key]), 2
            )
    return deviations

# -----------------------------
# CHEMICAL SOLUTION ENGINE
# -----------------------------
def suggest_solution(data):
    """
    Suggests chemical dosing and operational actions
    based on calculated LSI and Larson indices
    """
    solutions = []

    LSI = data["LSI"]
    larson = data["Larson"]

    # -----------------------------
    # Scaling treatment
    # -----------------------------
    if LSI > 1.5:
        dose = 10 + (LSI - 1.5) * 6
        solutions.append({
            "problem": "Severe Scaling",
            "chemical": "Scale Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Increase blowdown, reduce hardness, use strong scale inhibitors"
        })
    elif LSI > 0.8:
        dose = 6 + (LSI - 0.8) * 5
        solutions.append({
            "problem": "Moderate Scaling",
            "chemical": "Scale Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Control hardness, adjust blowdown, monitor scale deposits"
        })

    # -----------------------------
    # Corrosion treatment
    # -----------------------------
    if LSI < -1.0:
        dose = 10 + abs(LSI + 1) * 6
        solutions.append({
            "problem": "Severe Corrosion",
            "chemical": "Corrosion Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Increase alkalinity, add strong corrosion inhibitors, monitor metal loss"
        })
    elif LSI < -0.5:
        dose = 6 + abs(LSI + 0.5) * 5
        solutions.append({
            "problem": "Moderate Corrosion",
            "chemical": "Corrosion Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Increase alkalinity, maintain corrosion protection program"
        })

    # -----------------------------
    # Chloride corrosion treatment
    # -----------------------------
    if larson > 2.0:
        solutions.append({
            "problem": "Severe Chloride Corrosion",
            "chemical": "Operational Control",
            "dosage_ppm": 0,
            "action": "Reduce cycles of concentration via blowdown, monitor chloride/sulfate levels"
        })
    elif larson > 1.5:
        solutions.append({
            "problem": "Moderate Chloride Corrosion",
            "chemical": "Operational Control",
            "dosage_ppm": 0,
            "action": "Slightly reduce cycles of concentration, monitor chloride/sulfate levels"
        })

    # -----------------------------
    # Stable system
    # -----------------------------
    if not solutions:
        solutions.append({
            "problem": "Stable system",
            "chemical": "None",
            "dosage_ppm": 0,
            "action": "Maintain current treatment program and monitor water chemistry"
        })

    return solutions