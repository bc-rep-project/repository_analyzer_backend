const logger = require('./logger'); // Optional: Add a logging utility

const errorHandler = (err, req, res, next) => {
  // Log error information
  if (logger) {
    logger.error({
      message: err.message,
      stack: err.stack,
      path: req.path,
      method: req.method
    });
  }

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const errors = Object.values(err.errors).map(el => el.message);
    return res.status(400).json({
      status: 'error',
      message: 'Validation failed',
      errors
    });
  }

  // Mongoose duplicate key error
  if (err.code === 11000) {
    const field = Object.keys(err.keyValue)[0];
    return res.status(409).json({
      status: 'error',
      message: `${field} already exists`
    });
  }

  // Mongoose cast error (invalid ObjectId)
  if (err.name === 'CastError') {
    return res.status(400).json({
      status: 'error',
      message: `Invalid ${err.path}: ${err.value}`
    });
  }

  // WebSocket error handler
  if (err.name === 'WebSocketError') {
    return res.status(426).json({
      status: 'error',
      message: 'WebSocket upgrade failed'
    });
  }

  // Default error handler
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  res.status(statusCode).json({
    status: 'error',
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = errorHandler;