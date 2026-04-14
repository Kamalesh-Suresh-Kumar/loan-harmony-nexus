const http = require('http');

const data = JSON.stringify({
  "Date_of_Birth": "1990-05-15",
  "Gender": "Male",
  "Marital_Status": "Single",
  "Number_of_Dependents": 0,
  "Monthly_Income": 85000,
  "Sources_of_Income": "Primary",
  "Current_Loans": "No",
  "Debt_to_Income_Ratio": 0.15,
  "Property_Ownership": "Owned",
  "Employment_Status": "Salaried",
  "Job_Tenure_Work_Experience": 8,
  "Credit_Score": 780,
  "Loan_Amount_Requested": 500000,
  "Loan_Purpose": "Home",
  "Desired_Loan_Tenure": 60,
  "Rent_Payment_History": "Good",
  "Utility_Bill_Payments": "Good",
  "Spending_Patterns": "Consistent",
  "BNPL_Payment_History": "Good",
  "Gig_Economy_Income": "No",
  "Behavioral_Data": "Positive"
});

const options = {
  hostname: 'localhost',
  port: 5000,
  path: '/api/predict-loan',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length,
  },
};

const req = http.request(options, (res) => {
  let body = '';
  res.on('data', (chunk) => { body += chunk; });
  res.on('end', () => {
    console.log(`Status Code: ${res.statusCode}`);
    console.log(JSON.stringify(JSON.parse(body), null, 2));
  });
});

req.on('error', (error) => {
  console.error(error);
});

req.write(data);
req.end();
