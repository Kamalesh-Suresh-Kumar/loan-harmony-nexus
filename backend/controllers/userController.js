const User = require('../models/User');
const { encrypt, decrypt } = require('../utils/encryption');

// Create user with encrypted password
exports.createUser = async (req, res) => {
  try {
    const encryptedPassword = encrypt(req.body.password);

    const newUser = new User({
      ...req.body,
      password: encryptedPassword
    });

    await newUser.save();
    res.status(201).json({ message: 'User created successfully', user: newUser });
  } catch (error) {
    console.error("Error creating user:", error);
    res.status(500).json({ error: 'Failed to create user' });
  }
};

// Get users with decrypted password
exports.getUsers = async (req, res) => {
  try {
    const users = await User.find();
    const usersWithDecryptedPasswords = users.map(user => ({
      ...user.toObject(),
      password: decrypt(user.password)
    }));

    res.json(usersWithDecryptedPasswords);
  } catch (error) {
    console.error("Error fetching users:", error);
    res.status(500).json({ error: 'Failed to fetch users' });
  }
};
