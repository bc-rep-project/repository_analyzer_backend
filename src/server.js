const http = require('http');
const WebSocket = require('ws');
const app = require('./app');

// Create HTTP server
const server = http.createServer(app);

// WebSocket Server
const wss = new WebSocket.Server({ server });

// Render requires port 10000 for WebSockets
const PORT = process.env.PORT || 10000;

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`WebSocket endpoint: ws://localhost:${PORT}/api/notifications`);
});