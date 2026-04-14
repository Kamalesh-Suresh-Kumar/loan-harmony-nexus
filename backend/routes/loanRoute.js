const express = require('express');
const { createLoan, getLoans, updateLoan } = require('../controllers/loanController');
const router = express.Router();

router.post('/loans', createLoan);   // POST from ML frontend
router.get('/loans', getLoans);      // GET loans
router.put('/loans/:id', updateLoan); // PUT to update loans

module.exports = router;
