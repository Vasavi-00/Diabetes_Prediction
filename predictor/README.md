# Diabetes Prediction — Django Backend

A Django web application that loads a trained Random Forest model and
provides a form-based interface for diabetes prediction.

---

## Project Structure

```
diabetes_project/
│
├── manage.py                          # Django CLI entry point
│
├── models_ml/                         # ← Place your model files here
│   ├── diabetes_model.pkl             # Trained Random Forest model (required)
│   └── scaler.pkl                     # Feature scaler (optional)
│
├── diabetes_project/                  # Django project package
│   ├── __init__.py
│   ├── settings.py                    # Project settings
│   ├── urls.py                        # Root URL config
│   └── wsgi.py                        # WSGI entry point
│
└── predictor/                         # Django app for predictions
    ├── __init__.py
    ├── urls.py                        # App URL config
    ├── views.py                       # Prediction logic
    └── templates/
        └── predictor/
            └── home.html              # Form + result template
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install django numpy scikit-learn pandas
```

> `pickle` is part of the Python standard library — no install needed.

### 2. Add your model files

Copy your trained model files into the `models_ml/` directory:

```
models_ml/
├── diabetes_model.pkl   ← required
└── scaler.pkl           ← optional (include if you used StandardScaler during training)
```

### 3. Run the development server

```bash
cd diabetes_project
python manage.py runserver
```

### 4. Open in browser

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Prediction form |
| `http://127.0.0.1:8000/health/` | Health check |

---

## How It Works

1. User fills in the 8 health metric fields and clicks **Predict**.
2. The view parses and validates each field.
3. Biologically impossible `0` values (Glucose, BloodPressure, etc.) are
   replaced with dataset means from the Pima Indians Diabetes dataset.
4. If a scaler is loaded, features are scaled with `scaler.transform()`.
5. The model predicts `0` (non-diabetic) or `1` (diabetic).
6. The result is displayed on the same page — no page reload.

---

## Input Fields

| Field | Type | Description |
|-------|------|-------------|
| Pregnancies | int | Number of times pregnant |
| Glucose | int | Plasma glucose (mg/dL) |
| BloodPressure | int | Diastolic blood pressure (mmHg) |
| SkinThickness | int | Triceps skin fold thickness (mm) |
| Insulin | int | 2-hour serum insulin (μU/mL) |
| BMI | float | Body mass index (kg/m²) |
| DiabetesPedigreeFunction | float | Diabetes pedigree score |
| Age | int | Age in years |

---

## Notes

- This app is for **educational purposes only** and not a medical diagnostic tool.
- The `SECRET_KEY` in `settings.py` must be changed before any production deployment.
- Set `DEBUG = False` and restrict `ALLOWED_HOSTS` in production.