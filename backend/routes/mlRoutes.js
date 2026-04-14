const express = require('express');
const router = express.Router();
const { predictLoanRepayment } = require('../controllers/mlController');

router.post('/predict-loan', predictLoanRepayment);

module.exports = router;
