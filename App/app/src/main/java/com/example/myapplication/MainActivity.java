package com.example.myapplication;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import com.example.myapplication.R;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    private EditText etAge, etHeartRate, etSystolic, etDiastolic, etTemp, etSpO2;
    private Spinner spGender, spSymptom;
    private Button btnPredict;
    private TextView tvRiskResult;
    private RequestQueue requestQueue;

    // IMPORTANT: Replace this IP with your laptop's actual local IPv4 network address!
    // Do not use "127.0.0.1" inside an Android Emulator, use your shared Wi-Fi IPv4 address.
    // 10.0.2.2 redirects the Android Virtual Device right to your laptop's localhost
    private static final String PREDICT_URL = "http://10.0.2.2:8000/predict";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Bind layout entities to Java objects
        etAge = findViewById(R.id.etAge);
        spGender = findViewById(R.id.spGender);
        spSymptom = findViewById(R.id.spSymptom);
        etHeartRate = findViewById(R.id.etHeartRate);
        etSystolic = findViewById(R.id.etSystolic);
        etDiastolic = findViewById(R.id.etDiastolic);
        etTemp = findViewById(R.id.etTemp);
        etSpO2 = findViewById(R.id.etSpO2);
        btnPredict = findViewById(R.id.btnPredict);
        tvRiskResult = findViewById(R.id.tvRiskResult);

        // Initialize Volley network thread pool pipeline
        requestQueue = Volley.newRequestQueue(this);

        btnPredict.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendTriageRequest();
            }
        });
    }

    private void sendTriageRequest() {
        // Validate inputs are filled
        if (etAge.getText().toString().isEmpty() || etHeartRate.getText().toString().isEmpty() ||
                etSystolic.getText().toString().isEmpty() || etDiastolic.getText().toString().isEmpty() ||
                etTemp.getText().toString().isEmpty() || etSpO2.getText().toString().isEmpty()) {
            Toast.makeText(this, "Please fill in all medical parameters!", Toast.LENGTH_SHORT).show();
            return;
        }

        // 1. Build JSON Object Payload exactly mapping to FastAPI Pydantic schema
        JSONObject postData = new JSONObject();
        try {
            postData.put("Age", Integer.parseInt(etAge.getText().toString()));
            postData.put("Gender", spGender.getSelectedItem().toString());
            postData.put("Symptom", spSymptom.getSelectedItem().toString());
            postData.put("HeartRate", Integer.parseInt(etHeartRate.getText().toString()));
            postData.put("SystolicBP", Integer.parseInt(etSystolic.getText().toString()));
            postData.put("DiastolicBP", Integer.parseInt(etDiastolic.getText().toString()));
            postData.put("Temperature", Double.parseDouble(etTemp.getText().toString()));
            postData.put("SpO2", Integer.parseInt(etSpO2.getText().toString()));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // 2. Formulate Async Network Request Task
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.POST,
                PREDICT_URL,
                postData,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            // 3. Extract calculated mathematical metric results from response JSON
                            double score = response.getDouble("risk_score");

                            // 4. Update UI context presentation views dynamically
                            tvRiskResult.setText("Calculated Score: " + score + " / 10.0");
                            if (score >= 7.0) {
                                tvRiskResult.setTextColor(0xFFFF2222); // Red
                            } else if (score >= 4.0) {
                                tvRiskResult.setTextColor(0xFFFFA500); // Orange
                            } else {
                                tvRiskResult.setTextColor(0xFF008800); // Green
                            }
                        } catch (JSONException e) {
                            tvRiskResult.setText("Error reading server message array.");
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e("VOLLEY_NET", "Connection Failure: " + error.toString());
                        tvRiskResult.setText("Server connection timed out or unreachable.");
                        Toast.makeText(MainActivity.this, "Network Connection Failed!", Toast.LENGTH_SHORT).show();
                    }
                }
        );

        // Add task configuration to queue for operational execution
        requestQueue.add(jsonObjectRequest);
    }
}