const crypto = require('crypto');

// You should keep this secret key in your .env file for security
const secretKey = Buffer.from(process.env.SECRET_KEY, 'hex');
const iv = crypto.randomBytes(32); // Initialization vector

// Encrypt
function encrypt(text) {
  const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(secretKey, 'utf8'), iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const encryptedData = iv.toString('hex') + ':' + encrypted;
  return encryptedData;
}

// Decrypt
function decrypt(encryptedData) {
  const [ivHex, encryptedText] = encryptedData.split(':');
  const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(secretKey, 'utf8'), Buffer.from(ivHex, 'hex'));
  let decrypted = decipher.update(encryptedText, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

module.exports = { encrypt, decrypt };
