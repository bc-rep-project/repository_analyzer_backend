const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  githubUrl: {
    type: String,
    match: [/https?:\/\/(www\.)?github\.com\/[a-zA-Z0-9-]+(\/)?/, 'Invalid GitHub URL'],
    unique: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});