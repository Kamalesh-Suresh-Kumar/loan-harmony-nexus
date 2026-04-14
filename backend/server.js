const express = require('express');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const loanRoutes = require('./routes/loanRoute');
const authRoutes = require('./routes/auth');
const mlRoutes = require('./routes/mlRoutes');

dotenv.config();

// Temporary wrapper for connectDB since we don't have db info
try {
  connectDB();
} catch (e) {
  console.log("DB Connection skipped or failed during startup: ", e.message);
}

const app = express();
app.use(express.json()); // to parse JSON body

// Enable CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
});

app.use('/api', loanRoutes); // loan routes
app.use('/api', authRoutes); // auth routes
app.use('/api', mlRoutes);   // ml routes

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT} 🚀`));
