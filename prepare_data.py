import pandas as pd

# 1. Load the data
df = pd.read_csv("hospital_triage_data.csv")

# 2. Convert Gender to numbers (Male = 1, Female = 0)
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})

# 3. Convert Symptoms into numeric columns (One-Hot Encoding)
df = pd.get_dummies(df, columns=['Symptom'], dtype=int)

# 4. Separate your Inputs (Features) from your Outputs (Targets)
# Our inputs will be everything except the targets we want to predict
X = df.drop(columns=['RiskScore', 'EmergencyCategory', 'Department'])

# Let's see how our inputs look now!
print("--- PREPROCESSED INPUT FEATURES (FIRST 3 ROWS) ---")
print(X.head(3))
print("\nAvailable input features for the AI:", list(X.columns))