const WebSocket = require('ws');
const Notification = require('../models/Notification');

const setupWebSocket = (server) => {
  const wss = new WebSocket.Server({ server });

  wss.on('connection', (ws) => {
    console.log('New WebSocket connection');

    // Send initial notifications
    Notification.find().sort({ createdAt: -1 }).limit(10)
      .then(notifications => {
        ws.send(JSON.stringify(notifications));
      });

    ws.on('close', () => {
      console.log('WebSocket connection closed');
    });
  });

  return wss;
};

module.exports = setupWebSocket;