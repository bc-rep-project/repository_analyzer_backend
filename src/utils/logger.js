const logger = {
    error: (data) => {
      console.error('[ERROR]', new Date().toISOString(), data);
    },
    info: (data) => {
      console.log('[INFO]', new Date().toISOString(), data);
    },
    warn: (data) => {
      console.warn('[WARN]', new Date().toISOString(), data);
    }
  };
  
  module.exports = logger;