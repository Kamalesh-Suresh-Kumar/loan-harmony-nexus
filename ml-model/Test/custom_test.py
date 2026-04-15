import pandas as pd
from datetime import datetime
import joblib
import os
import warnings

warnings.filterwarnings('ignore')

MODELS_DIR = 'ml-model/trained_models/'
ASSET_PATH = os.path.join(MODELS_DIR, 'all_loan_prediction_assets.pkl')


# =========================
# LOAD ASSETS
# =========================
def load_assets():
    assets = joblib.load(ASSET_PATH)

    encoder = assets['encoder']
    scaler = assets['scaler']
    metadata = assets['metadata']

    return encoder, scaler, metadata


# =========================
# USER INPUT
# =========================
def get_input():
    return {
        'Date_of_Birth': input("DOB (YYYY-MM-DD): "),
        'Gender': input("Gender: "),
        'Marital_Status': input("Marital Status: "),
        'Number_of_Dependents': int(input("Dependents: ")),
        'Monthly_Income': int(input("Income: ")),
        'Sources_of_Income': input("Income Source: "),
        'Current_Loans': input("Current Loans: "),
        'Debt_to_Income_Ratio': float(input("DTI: ")),
        'Property_Ownership': input("Property: "),
        'Employment_Status': input("Employment: "),
        'Job_Tenure_Work_Experience': int(input("Experience: ")),
        'Credit_Score': int(input("Credit Score: ")),
        'Loan_Amount_Requested': int(input("Loan Amount: ")),
        'Loan_Purpose': input("Purpose: "),
        'Desired_Loan_Tenure': int(input("Tenure: ")),
        'Rent_Payment_History': input("Rent History: "),
        'Utility_Bill_Payments': input("Utility Bills: "),
        'Spending_Patterns': input("Spending: "),
        'BNPL_Payment_History': input("BNPL: "),
        'Gig_Economy_Income': input("Gig Income: "),
        'Behavioral_Data': input("Behavior: "),
    }


# =========================
# PREDICT
# =========================
def predict(data, encoder, scaler, metadata):
    categorical = metadata['categorical_features']
    numerical = metadata['numerical_features']
    all_features = metadata['all_features']

    df = pd.DataFrame([data])

    df['Age'] = (datetime.now() - pd.to_datetime(df['Date_of_Birth'])).dt.days / 365.25
    df = df.drop('Date_of_Birth', axis=1)

    cat = encoder.transform(df[categorical])
    cat_df = pd.DataFrame(cat, columns=encoder.get_feature_names_out(categorical))

    num = scaler.transform(df[numerical])
    num_df = pd.DataFrame(num, columns=numerical)

    final = pd.concat([cat_df, num_df], axis=1)

    input_df = pd.DataFrame(0, index=final.index, columns=all_features)
    for col in final.columns:
        if col in input_df.columns:
            input_df[col] = final[col]

    model = joblib.load(os.path.join(MODELS_DIR, "best_model.pkl"))

    proba = model.predict_proba(input_df)[0, 1]

    if proba > 0.75:
        decision = "APPROVE"
    elif proba > 0.5:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    print("\nFinal Decision:", decision)
    print(f"Approval Probability: {proba:.2%}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    encoder, scaler, metadata = load_assets()

    while True:
        data = get_input()
        predict(data, encoder, scaler, metadata)

        if input("\nAgain? (yes/no): ") != "yes":
            break