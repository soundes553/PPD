import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)

rf = joblib.load(os.path.join(BASE_DIR, "ppd_project_model.joblib"))
scaler = joblib.load(os.path.join(BASE_DIR, "ppd_scaler.joblib"))

def predict_ppd_risk(input_data):
    # 1 ➤ Self-harm rule
    if input_data.get("epds_10", 0) > 0:
        return {"risk_score": 1.0, "risk_label": "Critical (self-harm)"}

    # 2 ➤ Créer DataFrame utilisateur
    user_df = pd.DataFrame([input_data])

    # 3 ➤ Récupérer les colonnes attendues par le scaler
    expected_cols = scaler.feature_names_in_

    # 4 ➤ Créer un vecteur complet
    full_df = pd.DataFrame(columns=expected_cols)

    # 5 ➤ Remplir les colonnes manquantes par 0
    for col in expected_cols:
        if col in user_df.columns:
            full_df[col] = user_df[col]
        else:
            full_df[col] = 0

    # 6 ➤ Transformer
    X_scaled = scaler.transform(full_df)

    # 7 ➤ Prediction
    risk = rf.predict_proba(X_scaled)[:, 1][0]

    if risk < 0.33:
        label = "Low"
    elif risk < 0.66:
        label = "Moderate"
        label = "Moderate"
    else:
        label = "High"

    return {"risk_score": float(risk), "risk_label": label}
