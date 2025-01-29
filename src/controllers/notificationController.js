const Notification = require('../models/Notification');
const WebSocket = require('ws');

exports.getNotifications = async (req, res) => {
  try {
    const notifications = await Notification.find()
      .sort({ createdAt: -1 })
      .limit(10)
      .lean();
      
    res.status(200).json(notifications);
  } catch (err) {
    res.status(500).json({ message: 'Error fetching notifications' });
  }
};

exports.createNotification = async (req, res) => {
  try {
    const { message, userId } = req.body;
    
    const newNotification = new Notification({
      message,
      user: userId || null
    });

    await newNotification.save();

    // Broadcast to WebSocket clients
    const wss = req.app.get('wss');
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'NEW_NOTIFICATION',
          payload: newNotification
        }));
      }
    });

    res.status(201).json(newNotification);
  } catch (err) {
    res.status(500).json({ message: 'Error creating notification' });
  }
};