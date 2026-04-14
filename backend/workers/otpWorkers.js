const { Worker } = require('bullmq');
const { spawn } = require('child_process');
const path = require('path');

const connection = { host: 'localhost', port: 6379 };

const worker = new Worker('otpQueue', async (job) => {
const { phone, otp } = job.data;

return new Promise((resolve, reject) => {
const py = spawn('python', [
path.join(__dirname, '../scripts/send_otp.py'),
phone,
otp,
]);

py.on('close', (code) => {
  code === 0 ? resolve('Success') : reject('Failed');
});

});
}, { connection });

worker.on('completed', job => console.log("✅ Job ${job.id} done"));
worker.on('failed', (job, err) => console.log("❌ Job ${job.id} failed, err"));
