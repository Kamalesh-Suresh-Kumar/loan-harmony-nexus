const mongoose = require('mongoose');

const adminActivitySchema = new mongoose.Schema({
  adminEmail: { type: String, required: true },
  action: { type: String, required: true },
  details: { type: Object }, // You can store extra info here
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('AdminActivity', adminActivitySchema);