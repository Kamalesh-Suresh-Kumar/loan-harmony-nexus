const mongoose = require('mongoose');

const loanSchema = new mongoose.Schema({
  id: String,
  borrowerId: String,
  borrowerName: String,
  lenderId: String,
  lenderName: String,
  loanAmount: Number, // Frontend 'amount' maps to this or we can map it via API
  amount: Number,
  purpose: String,   // Added missing field
  loanType: String,
  term: Number,      // Frontend 'term'
  durationMonths: Number,
  interestRate: Number,
  status: String,
  
  // Financial specifics from frontend
  creditScore: Number,
  monthlyIncome: Number,
  employmentStatus: String,
  yearsEmployed: Number,
  existingLoanAmount: Number,
  existingLoanPeriod: Number,
  monthlyExpenses: Number,
  
  propertyDetails: {
    address: String,
    value: Number,
    type: { type: String }
  },
  
  paidMonths: {
    type: Number,
    default: 0
  },
  
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  }
});

module.exports = mongoose.model('Loan', loanSchema);
// → Will map to 'loans' collection in 'loanharmonydb'
