import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("cooling_tower_history.csv")

# -----------------------------
# Input features
# -----------------------------
X = df[["pH","conductivity","temperature"]]

# -----------------------------
# Output targets
# -----------------------------
# Include ORP as a target
y = df[[
    "TDS","chloride","sulfate",
    "magnesium","calcium",
    "alkalinity","hardness","ORP"
]]

# -----------------------------
# Train/test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -----------------------------
# Multi-output model
# -----------------------------
model = MultiOutputRegressor(RandomForestRegressor(n_estimators=200, random_state=42))

# Train model
model.fit(X_train, y_train)

# Save trained model
joblib.dump(model, "water_model.pkl")

print("Model trained and saved (including ORP prediction)")