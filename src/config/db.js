const mongoose = require('mongoose');

const connectDB = async () => {
  const maxRetries = 5;
  let retries = 0;
  
  while (retries < maxRetries) {
    try {
      await mongoose.connect(process.env.MONGODB_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        serverSelectionTimeoutMS: 5000
      });
      console.log('MongoDB connected');
      return;
    } catch (err) {
      retries++;
      console.error(`MongoDB connection failed (attempt ${retries}):`, err);
      await new Promise(res => setTimeout(res, 5000));
    }
  }
  console.error('MongoDB connection failed after maximum retries');
  process.exit(1);
};

module.exports = connectDB;