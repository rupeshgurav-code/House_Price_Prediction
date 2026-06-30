import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# LOAD REAL DATASET
# =========================
DATA_PATH = "data.csv"   # <-- your CSV file

df = pd.read_csv(DATA_PATH)

print("\n📊 Dataset Loaded")
print(df.head())

# =========================
# SPLIT FEATURES & TARGET
# =========================
X = df.drop("price", axis=1)
y = df["price"]

feature_names = X.columns.tolist()

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODEL
# =========================
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =========================
# PREDICTION
# =========================
y_pred = model.predict(X_test)

# =========================
# METRICS
# =========================
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n📊 MODEL PERFORMANCE")
print("-------------------")
print(f"MAE  : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R2   : {r2:.4f}")

# =========================
# SAVE MODEL
# =========================
os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/house_model.pkl")
joblib.dump(feature_names, "model/features.pkl")

print("\n✅ Model trained on REAL data and saved!")