from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize the API engine and load models
app = FastAPI()
model_score = joblib.load('triage_rf_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# 2. Define what the incoming data structure looks like
class PatientData(BaseModel):
    Age: int
    Gender: str  # "Male" or "Female"
    Symptom: str
    HeartRate: int
    SystolicBP: int
    DiastolicBP: int
    Temperature: float
    SpO2: int

# 3. Create the endpoint URL where the Android app will send data
@app.post("/predict")
def predict_triage(data: PatientData):
    # Prepare the input dictionary matching your model columns
    input_data = {col: 0 for col in model_columns}
    input_data['Age'] = data.Age
    input_data['Gender'] = 1 if data.Gender == "Male" else 0
    input_data['HeartRate'] = data.HeartRate
    input_data['SystolicBP'] = data.SystolicBP
    input_data['DiastolicBP'] = data.DiastolicBP
    input_data['Temperature'] = data.Temperature
    input_data['SpO2'] = data.SpO2
    input_data['RespiratoryRate'] = 16 # default fallback
    
    symptom_column = f"Symptom_{data.Symptom}"
    if symptom_column in input_data:
        input_data[symptom_column] = 1
        
    # Run the model
    input_df = pd.DataFrame([input_data])
    predicted_score = model_score.predict(input_df)[0]
    
    # Return the answer back to the Android App
    return {
        "risk_score": round(float(predicted_score), 2),
        "status": "Success"
    }