import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import os
import random
import warnings

warnings.filterwarnings('ignore')

MODELS_DIR = 'trained_models/'
ASSET_PATH = os.path.join(MODELS_DIR, 'all_loan_prediction_assets.pkl')


# =========================
# LOAD ASSETS
# =========================
def load_assets():
    assets = joblib.load(ASSET_PATH)

    models = assets['models']
    encoder = assets['encoder']
    scaler = assets['scaler']
    metadata = assets['metadata']

    return models, encoder, scaler, metadata


# =========================
# RANDOM DATA
# =========================
def generate_random_data():
    current_year = datetime.now().year

    return {
        'Date_of_Birth': datetime(
            random.randint(current_year - 75, current_year - 18),
            random.randint(1, 12),
            random.randint(1, 28)
        ).strftime('%Y-%m-%d'),

        'Gender': random.choice(['Male', 'Female']),
        'Marital_Status': random.choice(['Single', 'Married']),
        'Number_of_Dependents': random.randint(0, 10),
        'Monthly_Income': random.randint(15000, 1000000),
        'Sources_of_Income': random.choice(['Primary', 'Secondary', 'Multiple']),
        'Current_Loans': random.choice(['Yes', 'No']),
        'Debt_to_Income_Ratio': round(random.uniform(0.01, 0.9), 2),
        'Property_Ownership': random.choice(['Owned', 'Rented']),
        'Employment_Status': random.choice(['Salaried', 'Self-Employed']),
        'Job_Tenure_Work_Experience': random.randint(0, 40),
        'Credit_Score': random.randint(300, 900),
        'Loan_Amount_Requested': random.randint(25000, 5000000),
        'Loan_Purpose': random.choice(['Home', 'Business', 'Personal']),
        'Desired_Loan_Tenure': random.choice([12, 24, 36, 60]),
        'Rent_Payment_History': random.choice(['Good', 'Average', 'Poor']),
        'Utility_Bill_Payments': random.choice(['Good', 'Average', 'Poor']),
        'Spending_Patterns': random.choice(['Consistent', 'Erratic']),
        'BNPL_Payment_History': random.choice(['Good', 'Average', 'Poor']),
        'Gig_Economy_Income': random.choice(['Yes', 'No']),
        'Behavioral_Data': random.choice(['Positive', 'Neutral', 'Negative']),
    }


# =========================
# PREDICT
# =========================
def predict(user_data, encoder, scaler, metadata):
    categorical = metadata['categorical_features']
    numerical = metadata['numerical_features']
    all_features = metadata['all_features']

    df = pd.DataFrame([user_data])

    df['Age'] = (datetime.now() - pd.to_datetime(df['Date_of_Birth'])).dt.days / 365.25
    df = df.drop('Date_of_Birth', axis=1)

    cat = encoder.transform(df[categorical])
    cat_df = pd.DataFrame(cat, columns=encoder.get_feature_names_out(categorical))

    num = scaler.transform(df[numerical])
    num_df = pd.DataFrame(num, columns=numerical)

    final = pd.concat([cat_df, num_df], axis=1)

    # align features
    input_df = pd.DataFrame(0, index=final.index, columns=all_features)
    for col in final.columns:
        if col in input_df.columns:
            input_df[col] = final[col]

    # load BEST MODEL
    model = joblib.load(os.path.join(MODELS_DIR, "best_model.pkl"))

    proba = model.predict_proba(input_df)[0, 1]

    if proba > 0.85:
        decision = "APPROVE"
    elif proba > 0.6:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    print("\nDecision:", decision)
    print(f"Probability: {proba:.2%}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    models, encoder, scaler, metadata = load_assets()

    while True:
        data = generate_random_data()
        print("\nGenerated Data:", data)

        predict(data, encoder, scaler, metadata)

        if input("\nAgain? (yes/no): ") != "yes":
            break