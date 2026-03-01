# predictor/views.py — Core prediction logic

import pickle
import numpy as np
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

# ---------------------------------------------------------------------------
# Load the ML model and scaler once at startup (module level for efficiency)
# ---------------------------------------------------------------------------

MODEL_PATH = os.path.join(settings.MODEL_DIR, 'diabetes_model.pkl')
SCALER_PATH = os.path.join(settings.MODEL_DIR, 'scaler.pkl')

# Feature names in the exact order the model was trained on
FEATURE_NAMES = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]

# Typical mean values from the Pima Indians Diabetes dataset
# Used to replace biologically impossible 0 values for certain features
FEATURE_MEANS = {
    'Glucose': 121.7,
    'BloodPressure': 72.4,
    'SkinThickness': 29.1,
    'Insulin': 155.5,
    'BMI': 32.5,
}

def _load_pickle(path, label):
    """Helper: load a pickle file and return the object, or None on failure."""
    try:
        with open(path, 'rb') as f:
            obj = pickle.load(f)
        print(f"[INFO] {label} loaded from {path}")
        return obj
    except FileNotFoundError:
        print(f"[WARNING] {label} not found at {path}")
        return None
    except Exception as e:
        print(f"[ERROR] Could not load {label}: {e}")
        return None

model = _load_pickle(MODEL_PATH, 'Model')
scaler = _load_pickle(SCALER_PATH, 'Scaler')


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def health(request):
    """Simple health check — GET /health/"""
    return HttpResponse("Backend is running.", content_type="text/plain")


def home(request):
    """
    GET  /  → Render the empty prediction form.
    POST /  → Process form data, run prediction, return result on same page.
    """
    context = {}  # Data passed to the template

    if request.method == 'POST':
        try:
            # ----------------------------------------------------------------
            # Step 1: Parse and validate all form inputs
            # ----------------------------------------------------------------
            raw_values = {}
            for field in FEATURE_NAMES:
                value = request.POST.get(field, '').strip()
                if value == '':
                    raise ValueError(f"'{field}' is required.")
                raw_values[field] = float(value)

            # ----------------------------------------------------------------
            # Step 2: Replace biologically impossible 0s with dataset means
            #         (Only for features where 0 is medically impossible)
            # ----------------------------------------------------------------
            for field, mean_val in FEATURE_MEANS.items():
                if raw_values[field] == 0:
                    raw_values[field] = mean_val

            # ----------------------------------------------------------------
            # Step 3: Build the feature array in the correct column order
            # ----------------------------------------------------------------
            features = np.array([[raw_values[f] for f in FEATURE_NAMES]])

            # ----------------------------------------------------------------
            # Step 4: Scale features (if a scaler was loaded)
            # ----------------------------------------------------------------
            if scaler is not None:
                features = scaler.transform(features)

            # ----------------------------------------------------------------
            # Step 5: Run prediction
            # ----------------------------------------------------------------
            if model is None:
                raise RuntimeError(
                    "Model file not found. Place 'diabetes_model.pkl' inside the 'models_ml/' directory."
                )

            prediction = model.predict(features)[0]  # 0 = non-diabetic, 1 = diabetic

            # Optionally get prediction probability if the model supports it
            try:
                proba = model.predict_proba(features)[0]
                confidence = round(max(proba) * 100, 1)
                context['confidence'] = confidence
            except AttributeError:
                pass  # Model doesn't support predict_proba — that's fine

            # ----------------------------------------------------------------
            # Step 6: Prepare result message
            # ----------------------------------------------------------------
            if prediction == 1:
                context['result'] = "⚠️ The person is likely Diabetic."
                context['result_class'] = 'diabetic'
            else:
                context['result'] = "✅ The person is likely Non-Diabetic."
                context['result_class'] = 'non-diabetic'

            # Pass back the submitted values so the form stays filled
            context['form_data'] = raw_values

        except ValueError as e:
            # Missing field or non-numeric input
            context['error'] = f"Input error: {e}"
        except RuntimeError as e:
            # Model not loaded
            context['error'] = str(e)
        except Exception as e:
            # Catch-all for unexpected errors
            context['error'] = f"Unexpected error: {e}"

    return render(request, 'predictor/home.html', context)