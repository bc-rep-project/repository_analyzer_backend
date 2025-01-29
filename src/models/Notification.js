const mongoose = require('mongoose');

const notificationSchema = new mongoose.Schema({
  message: {
    type: String,
    required: true,
    trim: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  isRead: {
    type: Boolean,
    default: false
  },
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: false
  }
});

// Index for faster querying
notificationSchema.index({ createdAt: -1 });
notificationSchema.index({ isRead: 1 });

module.exports = mongoose.model('Notification', notificationSchema);