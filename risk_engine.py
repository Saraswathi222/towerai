import math


# -----------------------------
# LSI CALCULATION
# -----------------------------
def calculate_LSI(pH, TDS, temp, calcium, alkalinity):

    A = (math.log10(TDS) - 1) / 10
    B = -13.12 * math.log10(temp + 273) + 34.55
    C = math.log10(calcium) - 0.4
    D = math.log10(alkalinity)

    pHs = (9.3 + A + B) - (C + D)

    return pH - pHs


# -----------------------------
# LARSON INDEX
# -----------------------------
def larson_index(chloride, sulfate, alkalinity):

    return (chloride + sulfate) / alkalinity


# -----------------------------
# RISK DETECTION
# -----------------------------
def detect_risk(data):

    risks = []
    causes = []

    LSI = data["LSI"]
    larson = data["Larson"]

    # Scaling condition
    if LSI > 0.3:
        risks.append("Scaling")
        causes.append("High calcium hardness and alkalinity causing scale formation")

    # Corrosion condition
    elif LSI < -0.3:
        risks.append("Corrosion")
        causes.append("Low alkalinity and aggressive water causing corrosion")

    # Balanced water
    else:
        risks.append("Normal")
        causes.append("Water chemistry balanced")

    # Chloride corrosion risk
    if larson > 1.2:
        risks.append("Chloride corrosion risk")
        causes.append("High chloride and sulfate concentration")

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

    solutions = []

    LSI = data["LSI"]
    larson = data["Larson"]

    # Scaling treatment
    if LSI > 0.3:

        dose = LSI * 6

        solutions.append({
            "problem": "Scaling",
            "chemical": "Scale Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Increase blowdown and control hardness"
        })

    # Corrosion treatment
    elif LSI < -0.3:

        dose = abs(LSI) * 5

        solutions.append({
            "problem": "Corrosion",
            "chemical": "Corrosion Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Increase alkalinity and corrosion protection"
        })

    # Chloride corrosion
    if larson > 1.2:

        solutions.append({
            "problem": "Chloride corrosion",
            "chemical": "Operational control",
            "dosage_ppm": 0,
            "action": "Reduce cycles of concentration via blowdown"
        })

    # Stable system
    if not solutions:

        solutions.append({
            "problem": "Stable system",
            "chemical": "None",
            "dosage_ppm": 0,
            "action": "Maintain current treatment"
        })

    return solutions