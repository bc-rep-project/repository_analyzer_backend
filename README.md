**backend/README.md**
```markdown
# Backend API

[![Node.js](https://img.shields.io/badge/Node.js-18.x-green)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-4.x-blue)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.x-green)](https://www.mongodb.com/)

Backend service for the multi-page application featuring REST API endpoints and WebSocket support for real-time notifications.

## Features

- User management (CRUD operations)
- Real-time notifications via WebSocket
- MongoDB integration
- Secure API endpoints
- Rate limiting and CORS protection
- Error handling and logging

## Tech Stack

- Node.js
- Express
- MongoDB/Mongoose
- WebSocket (ws library)
- Helmet
- CORS
- Express Rate Limit

## Getting Started

### Prerequisites

- Node.js 18.x
- MongoDB Atlas account or local MongoDB instance
- npm 9.x

### Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/repo-name.git
cd backend
```

2. Install dependencies
```bash
npm install
```

3. Create `.env` file
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-address>/<database-name>?retryWrites=true&w=majority
PORT=5000
NODE_ENV=development
```

### Running the Application

Development mode (with nodemon):
```bash
npm run dev
```

Production mode:
```bash
npm start
```

## API Documentation

### Endpoints

| Method | Endpoint           | Description                |
|--------|--------------------|----------------------------|
| GET    | /api/users         | Get all users              |
| POST   | /api/users         | Create new user            |
| PUT    | /api/users/{id}    | Update user                |
| GET    | /api/notifications | WebSocket notifications    |

### WebSocket

Connect to `wss://your-backend-url/api/notifications` for real-time updates.

## Deployment

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Set environment variables:
   - `MONGODB_URI`
   - `PORT` (use 10000 for Render)
   - `NODE_ENV=production`
4. Set build command: `npm install`
5. Set start command: `npm start`

## Testing

Example cURL commands:
```bash
# Create user
curl -X POST -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com"}' \
  http://localhost:5000/api/users

# Get users
curl http://localhost:5000/api/users
```

## License

MIT
```