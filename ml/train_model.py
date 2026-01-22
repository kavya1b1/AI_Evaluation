import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

# Dummy training data (simulated expert decisions)
X = np.array([
    [0.9, 0.8, 0.7, 0.6],
    [0.3, 0.4, 0.2, 0.9],
    [0.7, 0.6, 0.8, 0.5],
    [0.4, 0.3, 0.4, 0.8],
    [0.85, 0.9, 0.9, 0.4]
])

y = np.array([90, 55, 85, 60, 92])

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

joblib.dump(model, "ml/evaluator_model.pkl")
