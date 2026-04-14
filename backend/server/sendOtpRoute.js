const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");
const otpCache = require("../cache/otpMemoryStore");
const User = require("../models/User");
const { hashPassword } = require("../utils/passwordUtils");

router.post("/api/send-otp", (req, res) => {
    const { email, ...userData } = req.body;
    if (!email) return res.status(400).json({ message: "Email is required" });

    // Check if user already exists in DB
    User.findOne({ email }).then(existingUser => {
        if (existingUser) {
            return res.status(400).json({ message: "User already exists with this email" });
        }

        // Check if user is already in cache (pending verification)
        if (otpCache.get(email)) {
            return res.status(400).json({ message: "A signup attempt is already in progress for this email. Please verify your OTP or wait a few minutes and try again." });
        }

        const otp = Math.floor(100000 + Math.random() * 900000).toString();
        const python = spawn("python", ["./scripts/send_otp.py", email, otp]);

        python.stdout.on("data", (data) => {
            const result = data.toString().trim();
            if (result === "SUCCESS") {
                otpCache.set(email, { otp, userData });
                return res.status(200).json({ message: "OTP sent successfully" });
            } else {
                otpCache.del(email); // <--- Clear cache on failure
                return res.status(500).json({ message: "OTP sending failed" });
            }
        });

        python.stderr.on("data", (data) => {
            console.error(`stderr: ${data}`);
        });

        python.on("error", (err) => {
            console.error("Python spawn error:", err);
            otpCache.del(email); // <--- Clear cache on failure
            return res.status(500).json({ message: "Server error while sending OTP" });
        });
    });
});

router.post("/api/verify-otp", async (req, res) => {
    const { email, otp } = req.body;
    const cached = otpCache.get(email);

    if (!cached) {
        return res.status(400).json({ message: "OTP expired or not found" });
    }

    if (otp === cached.otp) {
        // Create user in DB
        try {
            // Check again if user exists (race condition safety)
            const existingUser = await User.findOne({ email });
            if (existingUser) {
                otpCache.del(email);
                return res.status(400).json({ message: "User already exists with this email" });
            }
            // Hash password before saving
            const hashedPassword = await hashPassword(cached.userData.password);
            const user = new User({ ...cached.userData, email, password: hashedPassword });
            await user.save();
            otpCache.del(email); // clear after use
            return res.status(200).json({ message: "OTP verified and user created" });
        } catch (err) {
            return res.status(500).json({ message: "Error creating user" });
        }
    } else {
        return res.status(401).json({ message: "Invalid OTP" });
    }
});

module.exports = router;
