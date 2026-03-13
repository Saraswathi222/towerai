import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split

df = pd.read_csv("cooling_tower_history.csv")

X = df[["pH","conductivity","temperature"]]

y = df[[
"TDS","chloride","sulfate",
"magnesium","calcium",
"alkalinity","hardness"
]]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = MultiOutputRegressor(RandomForestRegressor(n_estimators=200))

model.fit(X_train,y_train)

joblib.dump(model,"water_model.pkl")

print("Model trained and saved")