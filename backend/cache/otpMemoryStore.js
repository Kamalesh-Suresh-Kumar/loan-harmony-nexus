const NodeCache = require('node-cache');
const otpCache = new NodeCache({ stdTTL: 300 }); // OTP valid for 5 minutes
module.exports = otpCache;
