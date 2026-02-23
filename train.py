import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Create dummy data (Replace this with your real dataset)
np.random.seed(42)
n_samples = 1000

data = {
    'area': np.random.randint(500, 5000, n_samples),
    'bedrooms': np.random.randint(1, 6, n_samples),
    'bathrooms': np.random.randint(1, 5, n_samples),
    'floor': np.random.randint(0, 20, n_samples),
    'total_floors': np.random.randint(1, 30, n_samples),
    'furnished': np.random.randint(0, 3, n_samples),  # 0, 1, 2
    'balcony': np.random.randint(0, 4, n_samples),
    'age_of_house': np.random.randint(0, 50, n_samples),
    'parking': np.random.randint(0, 4, n_samples),
    'near_school': np.random.randint(0, 2, n_samples),  # 0 or 1
    'near_metro': np.random.randint(0, 2, n_samples),   # 0 or 1
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate price (dummy formula for demonstration)
# Price = (area * 1500) + (bedrooms * 50000) + ...
df['price'] = (
    df['area'] * 2000 +
    df['bedrooms'] * 50000 +
    df['bathrooms'] * 30000 +
    df['floor'] * 2000 +
    df['furnished'] * 50000 +
    df['balcony'] * 15000 +
    (50 - df['age_of_house']) * 1000 +
    df['parking'] * 20000 +
    df['near_school'] * 30000 +
    df['near_metro'] * 50000 +
    np.random.randint(-100000, 100000, n_samples)
)

# Features and Target
X = df.drop('price', axis=1)
y = df['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
accuracy = model.score(X_test_scaled, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Create folders if not exist
if not os.path.exists('model'):
    os.makedirs('model')

# Save model and scaler
joblib.dump(model, 'model/house_model.pkl')
joblib.dump(scaler, 'model/scaler.pkl')

print("Model and Scaler saved successfully!")