import numpy as np
import joblib

# Load trained model
model = joblib.load("water_model.pkl")

def predict_parameters(pH, conductivity, temperature):
    """
    Predicts water chemistry parameters using hybrid approach:
    - 90% formula-based
    - 10% ML-corrected
    Also calculates ORP for microbial/fouling risk evaluation
    """
    # -----------------------------
    # FORMULA BASE VALUES
    # -----------------------------
    TDS = conductivity * 0.65
    chloride = TDS * 0.12
    sulfate = TDS * 0.10
    magnesium = TDS * 0.09
    calcium = TDS * 0.25
    alkalinity = TDS * 0.47
    hardness = calcium + magnesium

    formula = {
        "TDS": TDS,
        "chloride": chloride,
        "sulfate": sulfate,
        "magnesium": magnesium,
        "calcium": calcium,
        "alkalinity": alkalinity,
        "hardness": hardness
    }

    # -----------------------------
    # ML PREDICTION
    # -----------------------------
    X = np.array([[pH, conductivity, temperature]])
    pred = model.predict(X)[0]

    ml = {
        "TDS": pred[0],
        "chloride": pred[1],
        "sulfate": pred[2],
        "magnesium": pred[3],
        "calcium": pred[4],
        "alkalinity": pred[5],
        "hardness": pred[6]
    }

    # -----------------------------
    # CORRECTED HYBRID OUTPUT
    # -----------------------------
    # 90% formula + 10% ML correction
    result = {}
    for key in formula:
        corrected = (0.9 * formula[key]) + (0.1 * ml[key])
        result[key] = round(corrected, 2)

    # -----------------------------
    # ORP CALCULATION (mV)
    # -----------------------------
    # Using formula: ORP = 700 - ((temp-25)*5) - ((TDS-500)*0.05) - ((pH-7)*3)
    result["ORP"] = round(
        700 - ((temperature - 25) * 5) - ((result["TDS"] - 500) * 0.05) - ((pH - 7.0) * 3),
        2
    )

    return result