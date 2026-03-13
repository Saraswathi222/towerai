from flask import Flask, render_template, request
from predictor import predict_parameters
from risk_engine import calculate_LSI, larson_index, detect_risk, suggest_solution

app = Flask(__name__)

# -----------------------------
# deviation function
# -----------------------------
def deviation(actual, predicted):
    if actual == 0:
        return 0
    return round(abs(predicted - actual) / actual * 100, 2)

# -----------------------------
# Home route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":

        # -----------------------------
        # Input from user
        # -----------------------------
        pH = float(request.form["ph"])
        conductivity = float(request.form["conductivity"])
        temperature = float(request.form["temperature"])

        # -----------------------------
        # Predicted chemistry using ML + formula
        # -----------------------------
        chemistry = predict_parameters(pH, conductivity, temperature)

        # -----------------------------
        # Actual (formula-based) values
        # -----------------------------
        TDS_actual = conductivity * 0.65
        chloride_actual = TDS_actual * 0.12
        sulfate_actual = TDS_actual * 0.10
        magnesium_actual = TDS_actual * 0.09
        calcium_actual = TDS_actual * 0.25
        alkalinity_actual = TDS_actual * 0.47
        hardness_actual = calcium_actual + magnesium_actual

        # ORP formula (example)
        ORP_actual = 700 - ((temperature - 25) * 5) - ((TDS_actual - 500) * 0.05) - ((pH - 7.0) * 3)

        actual_values = {
            "TDS": TDS_actual,
            "chloride": chloride_actual,
            "sulfate": sulfate_actual,
            "magnesium": magnesium_actual,
            "calcium": calcium_actual,
            "alkalinity": alkalinity_actual,
            "hardness": hardness_actual,
            "ORP": ORP_actual
        }

        # -----------------------------
        # Deviation calculation
        # -----------------------------
        deviations = {key: deviation(actual_values[key], chemistry.get(key, actual_values[key]))
                      for key in actual_values}

        # -----------------------------
        # Index calculations
        # -----------------------------
        LSI = calculate_LSI(
            pH,
            chemistry.get("TDS", TDS_actual),
            temperature,
            chemistry.get("calcium", calcium_actual),
            chemistry.get("alkalinity", alkalinity_actual)
        )

        Larson = larson_index(
            chemistry.get("chloride", chloride_actual),
            chemistry.get("sulfate", sulfate_actual),
            chemistry.get("alkalinity", alkalinity_actual)
        )

        # -----------------------------
        # Prepare data for risk engine
        # -----------------------------
        data = chemistry.copy()
        data["LSI"] = LSI
        data["Larson"] = Larson
        # Include silica, turbidity if available
        data["silica"] = chemistry.get("silica", 75)   # default example
        data["turbidity"] = chemistry.get("turbidity", 2)
        data["ORP"] = chemistry.get("ORP", ORP_actual)

        # -----------------------------
        # Risk analysis and solution suggestions
        # -----------------------------
        risks, causes = detect_risk(data)
        solutions = suggest_solution(data)

        result = {
            "chemistry": chemistry,
            "LSI": LSI,
            "Larson": Larson,
            "risks": risks,
            "causes": causes,
            "solutions": solutions,
            "actual": actual_values,
            "deviation": deviations
        }

    return render_template("index.html", result=result)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port, debug=False)  # Must use host 0.0.0.0