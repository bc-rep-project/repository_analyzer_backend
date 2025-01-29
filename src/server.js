const http = require('http');
const app = require('./app');
const setupWebSocket = require('./services/websocket');

const PORT = process.env.PORT || 5000;

const server = http.createServer(app);

// WebSocket setup
setupWebSocket(server);

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});