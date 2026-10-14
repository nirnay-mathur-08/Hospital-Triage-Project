import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load the data
df = pd.read_csv("hospital_triage_data.csv")

# 2. Basic Preprocessing
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
df = pd.get_dummies(df, columns=['Symptom'], dtype=int)

# 3. Define Inputs (X) and Target (y)
X = df.drop(columns=['RiskScore', 'EmergencyCategory', 'Department'])
y = df['RiskScore'] # We want to predict the continuous Risk Score

# 4. Split into Train (80%) and Test (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Studying with {len(X_train)} patient records...")
print(f"Holding back {len(X_test)} records for the final exam...\n")

# 5. Initialize and Train the Random Forest Model
# Think of this as creating an empty brain and hit 'fit' to make it learn
model = RandomForestRegressor(n_estimators=100, random_state=42)
print("Training the Random Forest model... (This might take a few seconds)")
model.fit(X_train, y_train)
print("Training complete! 🎉\n")

# 6. Test the AI on hidden test data
predictions = model.predict(X_test)

# 7. Evaluate the results
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("--- MODEL EXAM RESULTS ---")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Model Accuracy (R² Score): {r2 * 100:.2f}%")


# 8. Save the model and the layout structure for later use
import joblib

# Save the trained AI model
joblib.dump(model, 'triage_rf_model.pkl')

# Save the column names so our web app knows exactly what input boxes to show
model_columns = list(X.columns)
joblib.dump(model_columns, 'model_columns.pkl')

print("\nModel saved permanently as 'triage_rf_model.pkl'! 💾")