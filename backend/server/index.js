// backend/server/index.js or app.js

const express = require('express');
const cors = require('cors');
const sendOtpRoute = require('./sendOtpRoute');

const app = express();
const PORT = 5001;

app.use(cors());
app.use(express.json());
app.use('/api', sendOtpRoute); // <-- Mount it here

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
