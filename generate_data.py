import numpy as np
import pandas as pd

np.random.seed(42)

n = 500

# =========================
# REALISTIC FEATURE GENERATION
# =========================

area = np.random.normal(1500, 600, n).astype(int)
area = np.clip(area, 400, 4000)

bedrooms = np.random.randint(1, 6, n)
bathrooms = np.random.randint(1, 4, n)
floor = np.random.randint(0, 20, n)
total_floors = np.random.randint(1, 25, n)

furnished = np.random.choice([0, 1, 2], n, p=[0.3, 0.4, 0.3])
balcony = np.random.randint(0, 4, n)
age_of_house = np.random.randint(0, 40, n)
parking = np.random.randint(0, 3, n)

near_school = np.random.choice([0, 1], n, p=[0.4, 0.6])
near_metro = np.random.choice([0, 1], n, p=[0.5, 0.5])

# =========================
# PRICE FORMULA (REALISTIC + NOISE)
# =========================

price = (
    area * 1800 +
    bedrooms * 55000 +
    bathrooms * 40000 +
    floor * 2000 +
    furnished * 60000 +
    balcony * 15000 +
    parking * 30000 +
    near_school * 50000 +
    near_metro * 70000 -
    age_of_house * 1200 +
    np.random.normal(0, 80000, n)
)

price = np.clip(price, 300000, None)

# =========================
# CREATE DATAFRAME
# =========================

df = pd.DataFrame({
    "area": area,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "floor": floor,
    "total_floors": total_floors,
    "furnished": furnished,
    "balcony": balcony,
    "age_of_house": age_of_house,
    "parking": parking,
    "near_school": near_school,
    "near_metro": near_metro,
    "price": price.astype(int)
})

# =========================
# SAVE CSV
# =========================

df.to_csv("data.csv", index=False)

print("✅ 500-row realistic dataset created: data.csv")
print(df.head())