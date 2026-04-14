import pandas as pd
from datetime import datetime
import joblib
import os
import warnings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

warnings.filterwarnings('ignore')

app = FastAPI()

MODELS_DIR = 'trained_models/'
ASSET_PATH = os.path.join(MODELS_DIR, 'all_loan_prediction_assets.pkl')

# Load models and preprocessing tools during app startup
try:
    assets = joblib.load(ASSET_PATH)
    models = assets['models']
    encoder = assets['encoder']
    scaler = assets['scaler']
    metadata = assets['metadata']
    print("ML Models and assets loaded successfully.")
except Exception as e:
    print(f"Failed to load ML assets: {e}")
    models = {}
    encoder = None
    scaler = None
    metadata = None


class ModelOutput(BaseModel):
    probability: float
    decision: int

class PredictionResponse(BaseModel):
    logistic_regression: ModelOutput
    random_forest: ModelOutput
    xgboost: ModelOutput
    catboost: ModelOutput

@app.post("/predict", response_model=PredictionResponse)
def predict_loan(data: dict):
    if not models or not encoder or not scaler or not metadata:
        raise HTTPException(status_code=500, detail="ML Models not loaded properly.")

    try:
        categorical = metadata['categorical_features']
        numerical = metadata['numerical_features']
        all_features = metadata['all_features']

        df = pd.DataFrame([data])

        # Replace 'Date_of_Birth' with 'Age'
        if 'Date_of_Birth' in df.columns:
            df['Age'] = (datetime.now() - pd.to_datetime(df['Date_of_Birth'])).dt.days / 365.25
            df = df.drop('Date_of_Birth', axis=1)

        # Separate categorical and numerical data as per expected features
        cat = encoder.transform(df[categorical])
        cat_df = pd.DataFrame(cat, columns=encoder.get_feature_names_out(categorical))

        num = scaler.transform(df[numerical])
        num_df = pd.DataFrame(num, columns=numerical)

        final = pd.concat([cat_df, num_df], axis=1)

        # Construct input df aligned with all_features
        input_df = pd.DataFrame(0, index=final.index, columns=all_features)
        for col in final.columns:
            if col in input_df.columns:
                input_df[col] = final[col]

        # Get probabilities
        results = {}
        for name, model in models.items():
            proba = float(model.predict_proba(input_df)[0, 1])
            # Threshold matches train.py (0.6)
            decision = 1 if proba > 0.6 else 0
            results[name] = {"probability": proba, "decision": decision}

        return PredictionResponse(
            logistic_regression=results.get('logistic_regression', {"probability": 0, "decision": 0}),
            random_forest=results.get('random_forest', {"probability": 0, "decision": 0}),
            xgboost=results.get('xgboost', {"probability": 0, "decision": 0}),
            catboost=results.get('catboost', {"probability": 0, "decision": 0})
        )
    except Exception as e:
        print("Prediction error:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
