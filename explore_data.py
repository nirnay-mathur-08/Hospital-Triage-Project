import pandas as pd

# 1. Load the dataset
df = pd.read_csv("hospital_triage_data.csv")

# 2. View the first 5 rows of your data
print("--- FIRST 5 PATIENT RECORDS ---")
print(df.head())

# 3. View the structure and column types
print("\n--- DATASET SUMMARY ---")
print(df.info())