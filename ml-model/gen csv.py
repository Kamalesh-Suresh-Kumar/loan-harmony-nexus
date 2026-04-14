import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def generate_synthetic_loan_data(num_samples=10000, filename='loan_data.csv'): # Increased samples for better training
    """
    Generates a synthetic dataset for loan approval prediction and saves it to a CSV.
    Includes vastly expanded ranges and more complex eligibility logic to simulate
    "unimaginable" real-world diversity.
    """
    data = {
        'Date_of_Birth': [],
        'Gender': [],
        'Marital_Status': [],
        'Number_of_Dependents': [],
        'Monthly_Income': [],
        'Sources_of_Income': [],
        'Current_Loans': [],
        'Debt_to_Income_Ratio': [],
        'Property_Ownership': [],
        'Employment_Status': [],
        'Job_Tenure_Work_Experience': [],
        'Credit_Score': [],
        'Loan_Amount_Requested': [],
        'Loan_Purpose': [],
        'Desired_Loan_Tenure': [],
        'Rent_Payment_History': [],
        'Utility_Bill_Payments': [],
        'Spending_Patterns': [],
        'BNPL_Payment_History': [],
        'Gig_Economy_Income': [],
        'Behavioral_Data': [],
        'Loan_Approved': []
    }

    today = datetime.now() 

    for _ in range(num_samples):
        # --- Expanded Data Generation Ranges and Categories ---
        dob_year = random.randint(today.year - 75, today.year - 18) # Age 18-75
        dob_month = random.randint(1, 12)
        dob_day = random.randint(1, 28) 
        
        dob_date = datetime(dob_year, dob_month, dob_day)
        age = (today - dob_date).days / 365.25
        
        data['Date_of_Birth'].append(dob_date.strftime('%Y-%m-%d'))
        data['Gender'].append(random.choice(['Male', 'Female']))
        data['Marital_Status'].append(random.choice(['Single', 'Married']))
        data['Number_of_Dependents'].append(random.randint(0, 10)) # More dependents
        
        income = random.randint(15000, 1000000) # Much wider income range (15k to 1M INR)
        data['Monthly_Income'].append(income)
        data['Sources_of_Income'].append(random.choice(['Primary', 'Secondary', 'Multiple', 'Pension', 'Investments', 'Rental_Income'])) # More income sources
        data['Current_Loans'].append(random.choice(['Yes', 'No', 'Multiple'])) # Added 'Multiple'
        
        dti = round(random.uniform(0.01, 0.90), 2) # Wider DTI range (1% to 90%)
        data['Debt_to_Income_Ratio'].append(dti)
        
        data['Property_Ownership'].append(random.choice(['Owned', 'Rented', 'Joint_Ownership', 'Commercial_Owned', 'Commercial_Rented'])) # More property types
        
        employment_status = random.choice(['Salaried', 'Self-Employed', 'Unemployed', 'Government', 'Retired', 'Student']) # More employment statuses
        data['Employment_Status'].append(employment_status)
        
        job_tenure = random.randint(0, 40) # Longer job tenures
        if employment_status in ['Unemployed', 'Student', 'Retired']:
            job_tenure = 0 
        data['Job_Tenure_Work_Experience'].append(job_tenure)
        
        credit_score = random.randint(300, 900)
        data['Credit_Score'].append(credit_score)
        
        loan_amount = random.randint(25000, 50000000) # Much wider loan amount range (25k to 50M INR)
        data['Loan_Amount_Requested'].append(loan_amount)
        
        loan_purpose = random.choice(['Home', 'Education', 'Business', 'Personal', 'Vehicle', 'Medical', 'Travel', 'Debt_Consolidation', 'Wedding']) # More loan purposes
        data['Loan_Purpose'].append(loan_purpose)
        
        data['Desired_Loan_Tenure'].append(random.choice([12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 180, 240, 300, 360])) # Longer tenure options
        
        data['Rent_Payment_History'].append(random.choice(['Good', 'Average', 'Poor', 'N/A'])) # Added N/A
        data['Utility_Bill_Payments'].append(random.choice(['Good', 'Average', 'Poor', 'N/A']))
        data['Spending_Patterns'].append(random.choice(['Consistent', 'Erratic', 'Impulsive', 'Cautious', 'Aggressive'])) # More spending patterns
        data['BNPL_Payment_History'].append(random.choice(['Good', 'Average', 'Poor', 'N/A']))
        data['Gig_Economy_Income'].append(random.choice(['Yes', 'No']))
        data['Behavioral_Data'].append(random.choice(['Positive', 'Neutral', 'Negative', 'Very_Positive', 'Very_Negative'])) # More behavioral data

        # --- More Complex Loan Approval Logic ---
        approved = 0 # Default to rejected

        # Age Constraint Check (Primary filter - slightly adjusted for wider age range)
        min_age_met = True
        if loan_purpose == 'Education':
            if age < 18: min_age_met = False # Education loans often 18+ for legal contracts
        elif loan_purpose in ['Home', 'Business', 'Debt_Consolidation']:
            if age < 21: min_age_met = False
        else: # Personal, Vehicle, Medical, Travel, Wedding etc.
            if age < 20: min_age_met = False # Slightly different minimum for personal loans
        
        if age > 65 and employment_status not in ['Retired', 'Government', 'Investments']: # Older applicants need stable post-retirement income
            min_age_met = False

        if not min_age_met:
            data['Loan_Approved'].append(0) 
            continue 

        # Base Score based on positive factors (more nuanced weighting)
        if credit_score >= 750: approved += 3 # Very good credit
        elif credit_score >= 680: approved += 2 # Good credit
        elif credit_score >= 600: approved += 1 # Average credit
        else: approved -= 2 # Poor credit

        if income >= 150000: approved += 3 # High income
        elif income >= 75000: approved += 2 # Mid-high income
        elif income >= 30000: approved += 1 # Average income
        else: approved -= 1 # Low income

        if dti <= 0.20: approved += 3 # Excellent DTI
        elif dti <= 0.35: approved += 2 # Good DTI
        elif dti <= 0.50: approved += 1 # Acceptable DTI
        else: approved -= 2 # High DTI

        if employment_status == 'Government': approved += 3 # Very stable
        elif employment_status == 'Salaried' and job_tenure >= 3: approved += 2 # Stable salaried
        elif employment_status == 'Self-Employed' and job_tenure >= 5: approved += 2 # Stable self-employed
        elif employment_status == 'Retired' and 'Pension' in data['Sources_of_Income'][-1]: approved += 1 # Stable pension
        elif employment_status == 'Unemployed': approved -= 5 # Strong penalty
        elif employment_status == 'Student' and loan_purpose != 'Education': approved -= 3 # Student for non-education loan

        if data['Property_Ownership'][-1] == 'Owned': approved += 1
        if data['Property_Ownership'][-1] == 'Commercial_Owned': approved += 2 # Higher value asset

        if data['Rent_Payment_History'][-1] == 'Good': approved += 1
        if data['Utility_Bill_Payments'][-1] == 'Good': approved += 1
        if data['BNPL_Payment_History'][-1] == 'Good': approved += 1

        if data['Behavioral_Data'][-1] == 'Very_Positive': approved += 2
        elif data['Behavioral_Data'][-1] == 'Positive': approved += 1
        elif data['Behavioral_Data'][-1] == 'Negative': approved -= 1
        elif data['Behavioral_Data'][-1] == 'Very_Negative': approved -= 2

        # Loan Amount to Income Ratio Impact (more granular)
        loan_income_ratio = loan_amount / income
        if loan_income_ratio > 100: approved -= 4 # Extremely high ratio
        elif loan_income_ratio > 70 and credit_score < 700: approved -= 2
        elif loan_income_ratio > 50 and credit_score < 650: approved -= 1
        elif loan_income_ratio < 10 and income > 100000: approved += 1 # Small loan for high earner

        # Purpose-specific adjustments
        if loan_purpose == 'Education' and employment_status == 'Student' and credit_score >= 650: approved += 1
        if loan_purpose == 'Debt_Consolidation' and dti > 0.40: approved += 1 # Lenders might approve to help consolidate debt
        if loan_purpose == 'Business' and data['Property_Ownership'][-1] == 'Commercial_Owned': approved += 2

        # Introduce some randomness to simulate uncaptured factors / human discretion
        approved += random.choice([-1, 0, 0, 0, 1]) 

        # "Minimal Level" Guarantee (Strong Positive Conditions - more stringent)
        strong_positive_met = (
            credit_score >= 800 and # Excellent credit
            income >= 200000 and    # Very high income
            dti <= 0.15 and       # Extremely low DTI
            employment_status in ['Salaried', 'Government'] and job_tenure >= 5 and # Highly stable, long-term employment
            data['Property_Ownership'][-1] == 'Owned' # Own property
        )

        # Final Approval Decision
        if strong_positive_met:
            data['Loan_Approved'].append(1) # Guaranteed Approval if truly exceptional
        elif approved >= 5: # Adjusted threshold for approval due to more complex scoring
            data['Loan_Approved'].append(1)
        else:
            data['Loan_Approved'].append(0)

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Synthetic dataset with {num_samples} samples generated and saved to '{filename}'")
    return df

if __name__ == "__main__":
    generate_synthetic_loan_data()