import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report,
    confusion_matrix
)
import joblib
import os
import warnings

warnings.filterwarnings('ignore')


# =========================
# EVALUATION FUNCTION
# =========================
def evaluate_model(name, y_test, y_pred, y_proba):
    print(f"\n--- {name.upper()} ---")
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall   : {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score : {f1_score(y_test, y_pred):.4f}")
    print(f"AUC-ROC  : {roc_auc_score(y_test, y_proba):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))


# =========================
# MAIN FUNCTION
# =========================
def train_and_save_models(data_filepath='loan_data.csv', models_dir='ml-model/trained_models/', threshold=0.5):

    # LOAD DATA
    try:
        df = pd.read_csv(data_filepath)
        print(f"Data loaded from '{data_filepath}'")
    except FileNotFoundError:
        print("Dataset not found!")
        return

    # FEATURE ENGINEERING
    df['Age'] = (datetime.now() - pd.to_datetime(df['Date_of_Birth'])).dt.days / 365.25
    df = df.drop('Date_of_Birth', axis=1)

    X = df.drop('Loan_Approved', axis=1)
    y = df['Loan_Approved']

    categorical_features = X.select_dtypes(include=['object']).columns
    numerical_features = X.select_dtypes(include=np.number).columns

    # SPLIT
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # PREPROCESSING
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    scaler = StandardScaler()

    # Categorical
    X_train_cat = encoder.fit_transform(X_train[categorical_features])
    X_test_cat = encoder.transform(X_test[categorical_features])

    cat_cols = encoder.get_feature_names_out(categorical_features)

    X_train_cat = pd.DataFrame(X_train_cat, columns=cat_cols, index=X_train.index)
    X_test_cat = pd.DataFrame(X_test_cat, columns=cat_cols, index=X_test.index)

    # Numerical
    X_train_num = scaler.fit_transform(X_train[numerical_features])
    X_test_num = scaler.transform(X_test[numerical_features])

    X_train_num = pd.DataFrame(X_train_num, columns=numerical_features, index=X_train.index)
    X_test_num = pd.DataFrame(X_test_num, columns=numerical_features, index=X_test.index)

    # Combine
    X_train_processed = pd.concat([X_train_cat, X_train_num], axis=1)
    X_test_processed = pd.concat([X_test_cat, X_test_num], axis=1)

    all_features = list(X_train_processed.columns)

    # MODELS
    models = {
        'logistic_regression': LogisticRegression(random_state=42, solver='liblinear'),
        'random_forest': RandomForestClassifier(random_state=42, n_estimators=100),
        'xgboost': XGBClassifier(random_state=42, eval_metric='logloss', n_estimators=100),
        'catboost': CatBoostClassifier(verbose=0, random_state=42, allow_writing_files=False)
    }

    os.makedirs(models_dir, exist_ok=True)

    print("\n========== INDIVIDUAL MODELS ==========")

    # TRAIN + SAVE
    for name, model in models.items():
        print(f"\nTraining {name}...")

        model.fit(X_train_processed, y_train)

        y_proba = model.predict_proba(X_test_processed)[:, 1]
        y_pred = (y_proba > threshold).astype(int)

        print(f"\nUsing Threshold: {threshold}")
        evaluate_model(name, y_test, y_pred, y_proba)

        joblib.dump(model, f"{models_dir}/{name}.pkl")

    # =========================
    # SAVE BEST MODEL (PRECISION BASED)
    # =========================
    best_model = None
    best_precision = 0
    best_name = ""

    for name, model in models.items():
        y_proba = model.predict_proba(X_test_processed)[:, 1]
        y_pred = (y_proba > threshold).astype(int)

        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        # Only consider models with acceptable recall
        if recall > 0.75 and precision > best_precision:
            best_precision = precision
            best_model = model
            best_name = name

    joblib.dump(best_model, f"{models_dir}/best_model.pkl")
    print(f"\nBest model (Precision + Recall constraint): {best_name} ({best_precision:.4f})")

    # SAVE PREPROCESSING
    joblib.dump(encoder, f"{models_dir}/encoder.pkl")
    joblib.dump(scaler, f"{models_dir}/scaler.pkl")

    metadata = {
        'categorical_features': list(categorical_features),
        'numerical_features': list(numerical_features),
        'all_features': all_features
    }

    joblib.dump(metadata, f"{models_dir}/metadata.pkl")

    print("\nIndividual models saved successfully!")

    # MASTER FILE
    print("\n========== CREATING MASTER PKL ==========")

    all_assets = {
        'models': {
            'logistic_regression': models['logistic_regression'],
            'random_forest': models['random_forest'],
            'xgboost': models['xgboost'],
            'catboost': models['catboost']
        },
        'encoder': encoder,
        'scaler': scaler,
        'metadata': metadata
    }

    joblib.dump(all_assets, f"{models_dir}/all_loan_prediction_assets.pkl")
    print("Master file saved!")

    # VALIDATE BY LOADING
    loaded_assets = joblib.load(f"{models_dir}/all_loan_prediction_assets.pkl")

    print("\n========== MASTER PKL EVALUATION ==========")

    for name, model in loaded_assets['models'].items():
        print(f"\nEvaluating {name} (from saved file)...")

        y_proba = model.predict_proba(X_test_processed)[:, 1]
        y_pred = (y_proba > threshold).astype(int)

        evaluate_model(f"{name} (MASTER)", y_test, y_pred, y_proba)


if __name__ == "__main__":
    train_and_save_models(threshold=0.6)