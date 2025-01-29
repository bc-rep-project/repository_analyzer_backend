const express = require('express');
const router = express.Router();
const {
  getUsers,
  createUser,
  updateUser
} = require('../controllers/userController');

const {
  getNotifications,
  createNotification
} = require('../controllers/notificationController');

// User routes
router.get('/users', getUsers);
router.post('/users', createUser);
router.put('/users/:id', updateUser);

// Notification routes
router.get('/notifications', getNotifications);
router.post('/notifications', createNotification);

router.get('/health', (req, res) => {
    res.status(200).json({ status: 'OK' });
  });

module.exports = router;