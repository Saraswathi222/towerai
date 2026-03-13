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
    - Silica scaling
    - Microbial growth
    - Fouling (Turbidity)
    """
    risks = []
    causes = []

    LSI = data.get("LSI", 0)
    larson = data.get("Larson", 0)
    silica = data.get("silica", 0)      # ppm
    ORP = data.get("ORP", 700)         # mV
    turbidity = data.get("turbidity", 1) # NTU

    # -----------------------------
    # Scaling
    # -----------------------------
    if LSI > 1.5:
        risks.append("Severe Scaling")
        causes.append("High calcium and alkalinity causing heavy scale formation")
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
    # Silica scaling
    # -----------------------------
    if silica > 150:
        risks.append("Severe Silica Scaling")
        causes.append("Excessive silica in water may form silica scale")
    elif silica > 120:
        risks.append("Moderate Silica Scaling")
        causes.append("Slightly high silica may cause scaling on heat transfer surfaces")

    # -----------------------------
    # Microbial growth
    # -----------------------------
    if ORP < 550:
        risks.append("Severe Microbial Growth")
        causes.append("Low oxidizing potential; high risk of bacteria & algae")
    elif ORP < 650:
        risks.append("Moderate Microbial Growth")
        causes.append("Slightly low ORP; microbial growth possible")

    # -----------------------------
    # Fouling / Turbidity
    # -----------------------------
    if turbidity > 6:
        risks.append("Severe Fouling")
        causes.append("High turbidity; suspended solids may cause fouling")
    elif turbidity > 3:
        risks.append("Moderate Fouling")
        causes.append("Moderate turbidity; partial fouling possible")

    # -----------------------------
    # Balanced / Normal
    # -----------------------------
    if not risks:
        risks.append("Normal")
        causes.append("Water chemistry is balanced and safe")

    return risks, causes

# -----------------------------
# CHEMICAL SOLUTION ENGINE
# -----------------------------
def suggest_solution(data):
    """
    Suggests chemical dosing and operational actions
    based on calculated water chemistry risks
    """
    solutions = []

    LSI = data.get("LSI", 0)
    larson = data.get("Larson", 0)
    silica = data.get("silica", 0)
    ORP = data.get("ORP", 700)
    turbidity = data.get("turbidity", 1)

    # -----------------------------
    # Scaling treatment
    # -----------------------------
    if LSI > 1.5:
        dose = 10 + (LSI - 1.5) * 6
        solutions.append({
            "problem": "Severe Scaling",
            "chemical": "Scale Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Increase blowdown, reduce hardness, add strong scale inhibitors"
        })
    elif LSI > 0.8:
        dose = 6 + (LSI - 0.8) * 5
        solutions.append({
            "problem": "Moderate Scaling",
            "chemical": "Scale Inhibitor",
            "dosage_ppm": round(dose, 2),
            "action": "Control hardness, adjust blowdown, monitor deposits"
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
            "action": "Reduce cycles of concentration via blowdown, monitor chloride/sulfate"
        })
    elif larson > 1.5:
        solutions.append({
            "problem": "Moderate Chloride Corrosion",
            "chemical": "Operational Control",
            "dosage_ppm": 0,
            "action": "Slightly reduce cycles, monitor chloride/sulfate levels"
        })

    # -----------------------------
    # Silica scaling treatment
    # -----------------------------
    if silica > 150:
        solutions.append({
            "problem": "Severe Silica Scaling",
            "chemical": "Operational Control",
            "dosage_ppm": 0,
            "action": "Increase blowdown, control silica to reduce scaling"
        })
    elif silica > 120:
        solutions.append({
            "problem": "Moderate Silica Scaling",
            "chemical": "Operational Control",
            "dosage_ppm": 0,
            "action": "Adjust blowdown to control silica levels"
        })

    # -----------------------------
    # Microbial growth treatment
    # -----------------------------
    if ORP < 500:
        dose = 20 + (500 - ORP) * 0.1
        solutions.append({
            "problem": "Severe Microbial Growth",
            "chemical": "Oxidizing Biocide",
            "dosage_ppm": round(dose, 2),
            "action": "Increase disinfectant feed, clean system thoroughly"
        })
    elif ORP < 575:
        dose = 15 + (575 - ORP) * 0.1
        solutions.append({
            "problem": "Moderate Microbial Growth",
            "chemical": "Oxidizing Biocide",
            "dosage_ppm": round(dose, 2),
            "action": "Increase disinfectant feed, monitor microbial activity"
        })
    elif ORP < 650:
        dose = 10 + (650 - ORP) * 0.1
        solutions.append({
            "problem": "Slight Microbial Growth",
            "chemical": "Oxidizing Biocide",
            "dosage_ppm": round(dose, 2),
            "action": "Check ORP, maintain mild biocide feed"
        })

    # -----------------------------
    # Fouling / Turbidity treatment
    # -----------------------------
    if turbidity > 6:
        dose = 8 + (turbidity - 6) * 1.5
        solutions.append({
            "problem": "Severe Fouling",
            "chemical": "Dispersant",
            "dosage_ppm": round(dose, 2),
            "action": "Improve filtration, clean heat exchangers, control solids"
        })
    elif turbidity > 3:
        dose = 5 + (turbidity - 3) * 1.0
        solutions.append({
            "problem": "Moderate Fouling",
            "chemical": "Dispersant",
            "dosage_ppm": round(dose, 2),
            "action": "Check filtration, reduce suspended solids"
        })

    # -----------------------------
    # Stable system
    # -----------------------------
    if not solutions:
        solutions.append({
            "problem": "Stable System",
            "chemical": "None",
            "dosage_ppm": 0,
            "action": "Maintain current treatment program, monitor regularly"
        })

    return solutions