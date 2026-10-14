import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)
num_records = 10000

# 1. Generate Demographics & Symptoms
ages = np.random.randint(1, 90, size=num_records)
genders = np.random.choice(['Male', 'Female'], size=num_records)
symptoms = np.random.choice(['Chest Pain', 'Fever', 'Cough', 'Shortness of Breath', 'Abdominal Pain', 'Headache'], size=num_records)

# 2. Generate Vitals (Heart Rate, Blood Pressure, Temp, SpO2, Respiratory Rate)
heart_rates = np.random.normal(loc=78, scale=12, size=num_records).astype(int)
bp_systolic = np.random.normal(loc=120, scale=15, size=num_records).astype(int)
bp_diastolic = np.random.normal(loc=80, scale=10, size=num_records).astype(int)
temperatures = np.round(np.random.normal(loc=98.6, scale=1.2, size=num_records), 1)
spo2_levels = np.random.randint(88, 101, size=num_records)
resp_rates = np.random.normal(loc=16, scale=3, size=num_records).astype(int)

# Create DataFrame
df = pd.DataFrame({
    'Age': ages, 'Gender': genders, 'Symptom': symptoms,
    'HeartRate': heart_rates, 'SystolicBP': bp_systolic, 'DiastolicBP': bp_diastolic,
    'Temperature': temperatures, 'SpO2': spo2_levels, 'RespiratoryRate': resp_rates
})

# 3. Apply Clinical Logic to create Targets
def assign_triage(row):
    score = 0
    if row['SpO2'] < 92: score += 4
    if row['HeartRate'] > 100 or row['HeartRate'] < 55: score += 2
    if row['Temperature'] > 101.5: score += 2
    if row['SystolicBP'] > 140 or row['SystolicBP'] < 90: score += 2
    if row['Symptom'] in ['Chest Pain', 'Shortness of Breath']: score += 3
    
    # Risk & Category
    risk_score = min(max(score, 1), 10)
    category = 'Immediate' if risk_score >= 7 else ('Urgent' if risk_score >= 4 else 'Non-Urgent')
    
    # Department
    if row['Symptom'] == 'Chest Pain': dept = 'Cardiology'
    elif row['Symptom'] == 'Shortness of Breath': dept = 'Pulmonology'
    elif row['Age'] <= 12: dept = 'Pediatrics'
    else: dept = 'General Medicine'
        
    return pd.Series([risk_score, category, dept])

df[['RiskScore', 'EmergencyCategory', 'Department']] = df.apply(assign_triage, axis=1)

# Save to CSV
df.to_csv('hospital_triage_data.csv', index=False)
print("Dataset created successfully as 'hospital_triage_data.csv'!")