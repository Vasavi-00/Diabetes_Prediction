import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("diabetes.csv")

# Replace zeros with NaN for specific columns
data[['Glucose','BloodPressure','BMI']] = data[['Glucose','BloodPressure','BMI']].replace(0, pd.NA)
data.fillna(data.mean(), inplace=True)

# Split data
X = data.drop('Outcome', axis=1)
y = data['Outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model

from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

model = VotingClassifier(estimators=[
    ('rf', RandomForestClassifier(n_estimators=100)),
    ('lr', LogisticRegression()),
    ('svc', SVC(probability=True))
], voting='soft')

model.fit(X_train, y_train)
# Import required metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Predict on test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy of the model:", accuracy)

# Optional: Confusion matrix and classification report
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model to a file
with open("diabetes_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Optionally, save the scaler too
with open("scaler.pkl", "wb") as file:
    pickle.dump(scaler, file)

print("Model and scaler saved successfully!")

# Load the model
with open("diabetes_model.pkl", "rb") as file:
    loaded_model = pickle.load(file)

# Load the scaler
with open("scaler.pkl", "rb") as file:
    loaded_scaler = pickle.load(file)

# Example: predict on new data
import numpy as np
new_data = np.array([[2, 120, 70, 30, 100, 25.5, 0.5, 30]])  # sample input
new_data_scaled = loaded_scaler.transform(new_data)
prediction = loaded_model.predict(new_data_scaled)

print("Prediction (1 = diabetic, 0 = non-diabetic):", prediction[0])