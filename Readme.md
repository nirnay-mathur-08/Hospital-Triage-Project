::: {align="center"}
# 🏥 PulseTriage AI

### Intelligent Clinical Urgency Scoring & Distributed Decision Support

**A multi-platform triage prototype combining machine-learning
inference, a clinical analytics dashboard, a FastAPI service, and an
Android intake client.**

`<br/>`{=html}

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Android](https://img.shields.io/badge/Client-Android-3DDC84?logo=android&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

[Overview](#-overview) · [Architecture](#-architecture) ·
[Features](#-key-features) · [Getting Started](#-getting-started) ·
[API](#-api-reference) · [Troubleshooting](#-troubleshooting)
:::

------------------------------------------------------------------------

## 📌 Overview

**PulseTriage AI** is a technical prototype for exploring how machine
learning can support emergency-department intake and clinical urgency
assessment. It combines patient demographics, symptoms, and vital signs
to produce a **Clinical Urgency Index from 1.0 to 10.0**.

The project brings together three connected components:

-   **Streamlit dashboard** --- a physician-facing workspace for
    entering patient information and reviewing model output.
-   **FastAPI inference service** --- a REST API that validates requests
    and serves predictions.
-   **Android intake app** --- a mobile client designed to submit
    patient observations to the API.

The repository also includes scripts for generating synthetic data,
preparing model features, training a Random Forest regressor, and
exporting an offline lookup database.

> **Important:** PulseTriage AI is a software prototype, not a
> clinically validated or approved medical device. Its predictions must
> not be used as a substitute for professional medical judgment or
> emergency care.

## ✨ Key Features

  -----------------------------------------------------------------------
  Capability                          Description
  ----------------------------------- -----------------------------------
  🧠 ML-based scoring                 Random Forest regression over
                                      engineered patient features

  🩺 Vital-sign inputs                Heart rate, blood pressure,
                                      temperature, and SpO₂

  👤 Patient context                  Age, gender, and reported symptom

  ⚡ REST inference API               FastAPI endpoint for submitting
                                      triage inputs

  📊 Analytics interface              Streamlit dashboard for interactive
                                      review

  📱 Android client                   Native Android intake interface
                                      using Volley

  📴 Offline-mode exploration         SQLite export for precomputed
                                      inference lookup

  🧪 Reproducible pipeline            Separate scripts for data
                                      generation, preparation, and model
                                      training
  -----------------------------------------------------------------------

## 🏗️ Architecture

PulseTriage AI is organized around a model-training pipeline and two
inference-facing clients connected through an API service.

``` text
┌───────────────────────────────────────────────────────┐
│                 DATA & MODEL PIPELINE                  │
│                                                       │
│  Synthetic data → Feature preparation → Random Forest │
│                                           │           │
│                                  Serialized model     │
└───────────────────────────────────────────┬───────────┘
                                            │
                         ┌──────────────────┴──────────────────┐
                         │                                     │
                         ▼                                     ▼
┌────────────────────────────────┐       ┌─────────────────────────────┐
│       FastAPI Service          │       │    Streamlit Dashboard      │
│                                │       │                             │
│  Request validation            │       │  Interactive patient inputs │
│  Model inference                │       │  Results and risk review    │
│  JSON response                  │       │  Session-based interface     │
└───────────────┬────────────────┘       └─────────────────────────────┘
                │
                │ HTTP / JSON
                ▼
┌────────────────────────────────┐
│        Android Client          │
│                                │
│  Native intake interface       │
│  Volley network requests        │
│  SQLite-based offline support   │
└────────────────────────────────┘
```

### Request lifecycle

1.  Synthetic records are generated and transformed into model-ready
    features.
2.  The Random Forest regressor is trained and serialized.
3.  A client submits patient details and vital signs to the FastAPI
    service.
4.  The service validates the request and returns the model's score and
    associated response fields.
5.  The dashboard or Android client displays the result.

## 🧰 Technology Stack

-   **Python 3.11+** --- application and machine-learning pipeline
-   **Pandas & NumPy** --- dataset manipulation and numerical operations
-   **scikit-learn** --- feature processing and Random Forest regression
-   **Joblib** --- model and artifact serialization
-   **FastAPI & Uvicorn** --- REST service
-   **Pydantic** --- request-schema validation
-   **Streamlit** --- interactive dashboard
-   **Android / Java** --- native mobile client
-   **Volley** --- Android HTTP networking
-   **SQLite** --- local database support for offline lookup workflows

## 📂 Repository Structure

``` text
Hospital_triage_project/
├── .vscode/
│   └── launch.json
├── android_app/
│   └── app/src/main/
│       ├── AndroidManifest.xml
│       ├── java/.../MainActivity.java
│       └── res/
│           ├── layout/activity_main.xml
│           └── values/strings.xml
├── app.py                       # Streamlit dashboard
├── main.py                      # FastAPI application
├── generate_data.py             # Synthetic data generator
├── explore_data.py              # Data inspection and profiling
├── prepare_data.py              # Feature preparation and encoding
├── train_model.py               # Model training and serialization
├── triage_rf_model.pkl          # Serialized model artifact
├── model_columns.pkl            # Expected feature schema
├── export_to_sqlite.py          # Offline lookup database exporter
├── triage_knowledge_base.db     # SQLite lookup database
└── hospital_triage_data.csv     # Synthetic dataset
```

> The exact files available in a checkout may vary. Keep generated model
> and data artifacts aligned with the code and feature schema used by
> the application.

## 🚀 Getting Started

### Prerequisites

Install the following before running the project:

-   Python **3.11 or newer**
-   Java SDK **17 or newer** for Android development
-   Android Studio (Iguana, Jellyfish, or newer) for the mobile client
-   Git

### 1. Clone the repository

Replace the example repository address with the actual URL for your
project.

``` bash
git clone <YOUR_REPOSITORY_URL>
cd Hospital_triage_project
```

### 2. Create a virtual environment

**Windows PowerShell**

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

``` bash
python -m pip install --upgrade pip
pip install pandas numpy scikit-learn joblib fastapi uvicorn streamlit requests
```

If your repository includes a `requirements.txt`, prefer installing from
it so the environment matches the project's pinned dependencies:

``` bash
pip install -r requirements.txt
```

### 4. Generate data and train the model (optional)

If the required dataset and model artifacts are not already present, run
the pipeline in order:

``` bash
python generate_data.py
python prepare_data.py
python train_model.py
```

Run these scripts from the project root. Regenerating artifacts may
overwrite existing data or model files.

## ▶️ Run the Application

Open **separate terminals** for the dashboard and API. Activate the
virtual environment in each terminal.

### A. Start the FastAPI service

``` bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

-   API base URL: `http://127.0.0.1:8000`
-   Interactive API documentation: `http://127.0.0.1:8000/docs`

Use `--reload` for local development only. Do not expose a development
server directly to an untrusted network.

### B. Start the Streamlit dashboard

``` bash
python -m streamlit run app.py
```

Open the local address printed in the terminal, typically:

``` text
http://localhost:8501
```

> **Why not `python app.py`?** Streamlit apps should be started through
> the Streamlit runner so its server and session handling are
> initialized correctly.

### C. Run the Android app

1.  Open the `android_app` directory in Android Studio.
2.  Let Gradle sync and install the required Android SDK components.
3.  Configure the API base URL in `MainActivity.java`.
4.  Build and run the app on an emulator or a test device.

**Typical local API addresses**

  --------------------------------------------------------------------------
  Target                              API host
  ----------------------------------- --------------------------------------
  Android emulator                    `http://10.0.2.2:8000`

  Physical device on the same Wi-Fi   `http://<YOUR_COMPUTER_LAN_IP>:8000`
  network                             
  --------------------------------------------------------------------------

For a physical device, the computer and phone generally need network
connectivity to one another, and the computer's firewall must permit the
connection. The `0.0.0.0` bind address makes the service listen on
available interfaces; it is not itself the address clients should use.

The project notes a Gradle build command:

``` bash
./gradlew clean build
```

On Windows, use the wrapper available in the Android project (commonly
`gradlew.bat clean build`).

## 🔌 API Reference

### `POST /predict`

Submits patient details and vital signs for a model prediction.

**Example request**

``` json
{
  "Age": 58,
  "Gender": "Male",
  "Symptom": "Chest Pain",
  "HeartRate": 118,
  "SystolicBP": 165,
  "DiastolicBP": 102,
  "Temperature": 99.4,
  "SpO2": 89
}
```

**Example response**

``` json
{
  "risk_score": 8.76,
  "triage_category": "Resuscitation / High Urgency",
  "color_code": "#FF2222",
  "latency_ms": 8.42,
  "timestamp": "2026-10-14T10:46:00Z"
}
```

The response above illustrates the documented response shape; actual
values depend on the running implementation and input. Confirm the
accepted values, validation rules, response schema, and error handling
in `main.py` and the interactive documentation at `/docs`.

## 📈 Model & Reported Metrics

The project documentation reports training and evaluation on a
**synthetic dataset of 10,000 records**, with a **20% hold-out slice**
described as 2,000 records.

  ------------------------------------------------------------------------
  Metric                              Reported value Interpretation in the
                                                     project
  --------------------- ---------------------------- ---------------------
  Coefficient of                     0.9979 (99.79%) Agreement with the
  determination (R²)                                 synthetic triage
                                                     labels

  Mean Absolute Error                         0.0102 Average absolute
  (MAE)                                              prediction error

  Root Mean Squared                           0.0241 Error metric that
  Error (RMSE)                                       penalizes larger
                                                     residuals

  Cold-start P99                             11.4 ms Reported
  inference latency                                  high-percentile
                                                     inference latency

  Feature-space                          14 features Reported prepared
  cardinality                                        feature count
  ------------------------------------------------------------------------

**How to interpret these numbers:** These are project-reported results,
not independent clinical validation. Strong performance against
synthetic labels indicates how closely the model reproduces the
synthetic labeling process; it does **not** establish real-world
diagnostic accuracy, patient safety, or improved clinical outcomes.

## 📴 Offline Mode

The repository includes `export_to_sqlite.py` and
`triage_knowledge_base.db` for an offline lookup workflow. The intended
approach is to prepare a local SQLite database containing precomputed
mappings so that an edge client can consult local data without making a
live cloud request.

To regenerate the database, inspect and run the exporter:

``` bash
python export_to_sqlite.py
```

The precise coverage of the lookup matrix, fallback behavior for unseen
combinations, and parity with live model inference should be verified in
the implementation before relying on offline results.

## 🛠️ Troubleshooting

### Streamlit exits when I run `python app.py`

Start it using the Streamlit runner:

``` bash
python -m streamlit run app.py
```

### The Android app cannot connect to FastAPI

-   Ensure the API is running and responds at
    `http://127.0.0.1:8000/docs` on the development computer.
-   For an emulator, use `10.0.2.2` to reach the host computer.
-   For a physical phone, use the computer's LAN IPv4 address rather
    than `127.0.0.1`.
-   Confirm that both devices can reach each other and that the firewall
    allows the connection.
-   Check the configured endpoint and Android network-security settings.

### Model or feature-column errors

-   Run the data-preparation and training scripts in the documented
    order.
-   Confirm `triage_rf_model.pkl` and `model_columns.pkl` were generated
    from the same feature pipeline.
-   Check that the input schema and categorical values match the model's
    expected features.

### `ModuleNotFoundError` or missing packages

Activate the intended virtual environment, then install the
dependencies:

``` bash
python -m pip install pandas numpy scikit-learn joblib fastapi uvicorn streamlit requests
```

## 🔐 Security & Privacy Notes

Clinical information is highly sensitive. Before any real-world or
networked deployment:

-   Use only synthetic or appropriately de-identified data during
    development.
-   Do not expose the development API publicly.
-   Add appropriate authentication, authorization, access logging, and
    input controls.
-   Use TLS for network traffic; use mutual TLS where required by the
    deployment's security model.
-   Restrict access to model files, databases, logs, and backups.
-   Review the actual Android and server configuration for cleartext
    HTTP behavior.
-   Validate the system through formal clinical, security, privacy, and
    regulatory review before any clinical use.

The project documentation describes local or air-gapped deployment as a
design goal. **Air-gapped operation, encrypted transport, and
production-grade security depend on the actual deployment and
configuration**; they should not be assumed from the presence of these
components alone.

## ⚕️ Medical & Regulatory Disclaimer

PulseTriage AI is intended for **educational, prototyping, and technical
demonstration purposes only**. It has not been established here as
cleared or approved by the FDA, CE medical-device frameworks, CDSCO, or
another regulatory authority. It is not intended to diagnose, treat,
cure, or prevent any disease, and must not be used to make decisions
about patient care.

**Never delay emergency care or override a qualified clinician based on
this prototype's output.**

## 📄 License

The project documentation identifies the license as **MIT**. Include the
corresponding `LICENSE` file in the repository and verify that it
contains the intended license text before distribution.

------------------------------------------------------------------------

::: {align="center"}
**Built to explore the intersection of machine learning, clinical
workflows, and edge computing.**

*PulseTriage AI --- a prototype for decision support, not a replacement
for clinical judgment.*
:::
