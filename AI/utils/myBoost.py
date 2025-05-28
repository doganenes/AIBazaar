import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# 1. DATA CREATION
data = {
    "Brand": [
        "Samsung",
        "Apple",
        "Xiaomi",
        "Samsung",
        "Apple",
        "Xiaomi",
        "Samsung",
        "Apple",
        "Xiaomi",
        "Samsung",
    ],
    "RAM": [8, 6, 8, 12, 4, 6, 16, 8, 12, 8],
    "Storage": [128, 64, 128, 256, 64, 128, 512, 256, 256, 128],
    "Camera": [48, 12, 64, 108, 12, 48, 200, 48, 108, 64],
    "Battery": [4000, 3000, 4500, 5000, 2800, 4000, 5000, 3500, 4500, 4200],
    "Processor": [
        "Snapdragon",
        "A14",
        "Snapdragon",
        "Exynos",
        "A13",
        "Snapdragon",
        "Exynos",
        "A15",
        "Snapdragon",
        "Exynos",
    ],
    "Price": [700, 999, 400, 850, 799, 350, 1200, 1099, 500, 750],
}

df = pd.DataFrame(data)
print("Original Dataset:")
print(df)
print("\n" + "=" * 50 + "\n")

# 2. DATA PREPROCESSING
print("Data Preprocessing...")
df_encoded = pd.get_dummies(df)
print("Encoded Dataset:")
print(df_encoded.head())
print(f"\nDataset shape: {df_encoded.shape}")
print(f"Feature columns: {list(df_encoded.columns)}")
print("\n" + "=" * 50 + "\n")

# Separate features and target
X = df_encoded.drop("Price", axis=1)
y = df_encoded["Price"]

print("Features (X):")
print(X.head())
print(f"\nTarget (y): {list(y.values)}")
print("\n" + "=" * 50 + "\n")

# 3. TRAIN-TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
print(f"Training set size: {len(X_train)}")
print(f"Testing set size: {len(X_test)}")
print("\n" + "=" * 50 + "\n")

# 4. MODEL TRAINING
print("Training XGBoost Model...")
model = xgb.XGBRegressor(
    objective="reg:squarederror",
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
)

model.fit(X_train, y_train)
print("Model training completed!")
print("\n" + "=" * 50 + "\n")

# 5. MODEL EVALUATION
print("Model Evaluation:")
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: ${mae:.2f}")
print(f"Mean Squared Error: ${mse:.2f}")
print(f"Root Mean Squared Error: ${rmse:.2f}")
print(f"R² Score: {r2:.3f}")
print("\n" + "=" * 50 + "\n")

# 6. FEATURE IMPORTANCE
print("Feature Importance:")
feature_importance = pd.DataFrame(
    {"feature": X.columns, "importance": model.feature_importances_}
).sort_values("importance", ascending=False)

print(feature_importance)
print("\n" + "=" * 50 + "\n")


# 7. PREDICTION FUNCTION
def predict_phone_price(ram, storage, camera, battery, brand, processor):
    """
    Predict phone price based on specifications

    Parameters:
    ram (int): RAM in GB
    storage (int): Storage in GB
    camera (int): Camera megapixels
    battery (int): Battery capacity in mAh
    brand (str): Brand name (Samsung, Apple, Xiaomi)
    processor (str): Processor type (Snapdragon, A13, A14, A15, Exynos)
    """
    # Create base dictionary with all features set to 0
    new_phone = {col: 0 for col in X.columns}

    # Set numerical features
    new_phone["RAM"] = ram
    new_phone["Storage"] = storage
    new_phone["Camera"] = camera
    new_phone["Battery"] = battery

    # Set categorical features
    brand_col = f"Brand_{brand}"
    processor_col = f"Processor_{processor}"

    if brand_col in new_phone:
        new_phone[brand_col] = 1
    if processor_col in new_phone:
        new_phone[processor_col] = 1

    new_df = pd.DataFrame([new_phone])
    return model.predict(new_df)[0]


# 8. EXAMPLE PREDICTIONS
print("Example Predictions:")
print("-" * 50)

# Example 1: High-end Xiaomi
price1 = predict_phone_price(12, 256, 108, 5200, "Xiaomi", "Snapdragon")
print(
    f"High-end Xiaomi (12GB RAM, 256GB Storage, 108MP Camera, 5200mAh): ${price1:.2f}"
)

# Example 2: Mid-range Samsung
price2 = predict_phone_price(8, 128, 64, 4000, "Samsung", "Exynos")
print(
    f"Mid-range Samsung (8GB RAM, 128GB Storage, 64MP Camera, 4000mAh): ${price2:.2f}"
)

# Example 3: Premium Apple
price3 = predict_phone_price(8, 256, 48, 3500, "Apple", "A15")
print(f"Premium Apple (8GB RAM, 256GB Storage, 48MP Camera, 3500mAh): ${price3:.2f}")

# Example 4: Budget Xiaomi
price4 = predict_phone_price(6, 128, 48, 4000, "Xiaomi", "Snapdragon")
print(f"Budget Xiaomi (6GB RAM, 128GB Storage, 48MP Camera, 4000mAh): ${price4:.2f}")

print("\n" + "=" * 50 + "\n")

# 9. MANUAL PREDICTION (Your Original Method)
print("Manual Prediction (Your Original Method):")
new_phone_manual = {
    "RAM": 12,
    "Storage": 256,
    "Camera": 108,
    "Battery": 5200,
    "Brand_Apple": 0,
    "Brand_Samsung": 0,
    "Brand_Xiaomi": 1,
    "Processor_A13": 0,
    "Processor_A14": 0,
    "Processor_A15": 0,
    "Processor_Exynos": 0,
    "Processor_Snapdragon": 1,
}

new_df_manual = pd.DataFrame([new_phone_manual])

# Add missing columns and reorder
for col in X.columns:
    if col not in new_df_manual.columns:
        new_df_manual[col] = 0
new_df_manual = new_df_manual[X.columns]

predicted_price_manual = model.predict(new_df_manual)[0]
print(f"Manual method prediction: ${predicted_price_manual:.2f}")

print("\n" + "=" * 50 + "\n")
print("Analysis Complete!")
