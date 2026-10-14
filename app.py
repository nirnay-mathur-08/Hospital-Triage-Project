import streamlit as pd
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Load the saved AI Model and column configuration
model = joblib.load('triage_rf_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# 2. Design the Webpage Header
st.set_page_config(page_title="AI Hospital Triage", layout="centered")
st.title("🏥 Smart AI Hospital Triage Dashboard")
st.write("Input patient demographics and physiological vital signs to check immediate clinical risk.")
st.markdown("---")

# 3. Create Input Forms on the Interface
st.subheader("📋 Patient Information & Vitals")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 1, 100, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    symptom = st.selectbox("Primary Symptom", ["Chest Pain", "Fever", "Cough", "Shortness of Breath", "Abdominal Pain", "Headache"])
    heart_rate = st.slider("Heart Rate (BPM)", 40, 160, 75)

with col2:
    systolic_bp = st.slider("Systolic BP (mmHg)", 70, 200, 120)
    diastolic_bp = st.slider("Diastolic BP (mmHg)", 40, 130, 80)
    temp = st.slider("Temperature (°F)", 95.0, 105.0, 98.6, step=0.1)
    spo2 = st.slider("Oxygen Saturation (SpO2 %)", 80, 100, 98)

# 4. Process Inputs When User Clicks the Predict Button
if st.button("Calculate Triage Risk Score", type="primary"):
    
    # Structure inputs to match the exactly encoded training matrix layout
    input_data = {col: 0 for col in model_columns}
    
    # Assign baseline numbers
    input_data['Age'] = age
    input_data['Gender'] = 1 if gender == "Male" else 0
    input_data['HeartRate'] = heart_rate
    input_data['SystolicBP'] = systolic_bp
    input_data['DiastolicBP'] = diastolic_bp
    input_data['Temperature'] = temp
    input_data['SpO2'] = spo2
    input_data['RespiratoryRate'] = 16 # Baseline constant default fallback
    
    # Turn on the specific encoded symptom feature column
    symptom_column = f"Symptom_{symptom}"
    if symptom_column in input_data:
        input_data[symptom_column] = 1
        
    # Convert data into data frame for inference engine
    input_df = pd.DataFrame([input_data])
    
    # Make live prediction
    predicted_score = model.predict(input_df)[0]
    
    # 5. Display Beautiful Output Results
    st.markdown("---")
    st.subheader("🎯 AI Inference Analysis Result")
    
    # Color code according to risk severity tiers
    if predicted_score >= 7.0:
        st.error(f"⚠️ **CRITICAL RISK** | Calculated Score: {predicted_score:.1f} / 10.0")
        st.write("🔴 **Action Recommended:** Direct immediate emergency room intervention route.")
    elif predicted_score >= 4.0:
        st.warning(f"⚡ **MODERATE/URGENT RISK** | Calculated Score: {predicted_score:.1f} / 10.0")
        st.write("🟡 **Action Recommended:** Priority clinical assessment and targeted monitoring.")
    else:
        st.success(f"✅ **LOW RISK** | Calculated Score: {predicted_score:.1f} / 10.0")
        st.write("🟢 **Action Recommended:** Standard waiting queue or general OPD assignment routing.")