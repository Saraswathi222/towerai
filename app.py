from flask import Flask, render_template, request
from predictor import predict_parameters
from risk_engine import calculate_LSI, larson_index, detect_risk, suggest_solution

app = Flask(__name__)


# deviation function
def deviation(actual, predicted):
    if actual == 0:
        return 0
    return round(abs(predicted - actual) / actual * 100, 2)


@app.route("/", methods=["GET","POST"])
def home():

    result=None

    if request.method == "POST":

        pH = float(request.form["ph"])
        conductivity = float(request.form["conductivity"])
        temperature = float(request.form["temperature"])

        # ML prediction
        chemistry = predict_parameters(pH,conductivity,temperature)

        # -----------------------------
        # ACTUAL (FORMULA BASED VALUES)
        # -----------------------------

        TDS_actual = conductivity * 0.65
        chloride_actual = TDS_actual * 0.12
        sulfate_actual = TDS_actual * 0.10
        magnesium_actual = TDS_actual * 0.09
        calcium_actual = TDS_actual * 0.25
        alkalinity_actual = TDS_actual * 0.47
        hardness_actual = calcium_actual + magnesium_actual

        actual_values = {
            "TDS": TDS_actual,
            "chloride": chloride_actual,
            "sulfate": sulfate_actual,
            "magnesium": magnesium_actual,
            "calcium": calcium_actual,
            "alkalinity": alkalinity_actual,
            "hardness": hardness_actual
        }

        # -----------------------------
        # DEVIATION CALCULATION
        # -----------------------------

        deviations = {
            "TDS": deviation(TDS_actual, chemistry["TDS"]),
            "chloride": deviation(chloride_actual, chemistry["chloride"]),
            "sulfate": deviation(sulfate_actual, chemistry["sulfate"]),
            "magnesium": deviation(magnesium_actual, chemistry["magnesium"]),
            "calcium": deviation(calcium_actual, chemistry["calcium"]),
            "alkalinity": deviation(alkalinity_actual, chemistry["alkalinity"]),
            "hardness": deviation(hardness_actual, chemistry["hardness"])
        }

        # -----------------------------
        # INDEX CALCULATIONS
        # -----------------------------

        LSI = calculate_LSI(
            pH,
            chemistry["TDS"],
            temperature,
            chemistry["calcium"],
            chemistry["alkalinity"]
        )

        Larson = larson_index(
            chemistry["chloride"],
            chemistry["sulfate"],
            chemistry["alkalinity"]
        )

        data = chemistry
        data["LSI"] = LSI
        data["Larson"] = Larson

        # -----------------------------
        # RISK ANALYSIS
        # -----------------------------

        risks,causes = detect_risk(data)
        solutions = suggest_solution(data)

        result={
            "chemistry":chemistry,
            "LSI":LSI,
            "Larson":Larson,
            "risks":risks,
            "causes":causes,
            "solutions":solutions,
            "actual":actual_values,
            "deviation":deviations
        }

    return render_template("index.html",result=result)


if __name__ == "__main__":
    app.run(debug=True)