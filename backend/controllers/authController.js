const User = require('../models/User');
const { hashPassword } = require('../utils/passwordUtils');

const signup = async (req, res) => {
  try {
    const {
      name,
      email,
      phone,
      dob,
      gender,
      maritalStatus,
      dependents,
      password
    } = req.body;

    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: 'User already exists with this email' });
    }

    // Hash password
    const hashedPassword = await hashPassword(password);

    // Create new user
    const user = new User({
      name,
      email,
      phone,
      dob,
      gender,
      maritalStatus,
      dependents,
      password: hashedPassword
    });

    await user.save();

    // Don't send password in response
    const userResponse = user.toObject();
    delete userResponse.password;

    res.status(201).json({
      message: 'User created successfully',
      user: userResponse
    });
  } catch (error) {
    console.error('Signup error:', error);
    res.status(500).json({ message: 'Error creating user' });
  }
};

const sendOtp = async (req, res) => {
  try {
    const { email } = req.body;
    // Mock sending OTP.
    console.log(`Sending mock OTP to ${email}`);
    res.status(200).json({ message: 'OTP sent successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error sending OTP' });
  }
};

const verifyOtp = async (req, res) => {
  try {
    const { email, otp } = req.body;
    // Mock verification (any OTP is accepted for now, or require a specific one like 123456)
    if (otp === "123456" || otp) {
      await User.findOneAndUpdate({ email }, { isVerified: true });
      res.status(200).json({ message: 'Account verified successfully' });
    } else {
      res.status(400).json({ message: 'Invalid OTP' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Error verifying OTP' });
  }
};

const { comparePassword } = require('../utils/passwordUtils');

const login = async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Check if user exists
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ message: 'Invalid email or password' });
    }

    // Check password
    const isMatch = await comparePassword(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid email or password' });
    }

    const userResponse = user.toObject();
    delete userResponse.password;

    res.status(200).json({
      message: 'Login successful',
      user: userResponse
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Error logging in' });
  }
};

module.exports = {
  signup,
  sendOtp,
  verifyOtp,
  login
};