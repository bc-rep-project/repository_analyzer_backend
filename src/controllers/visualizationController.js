const User = require('../models/User');
const axios = require('axios');

exports.visualizeRepository = async (req, res) => {
  try {
    const { userId } = req.params;
    const user = await User.findById(userId);
    
    if (!user?.githubUrl) {
      return res.status(400).json({ message: 'No GitHub URL associated' });
    }

    // Extract repo path from GitHub URL
    const repoPath = user.githubUrl
      .replace('https://github.com/', '')
      .replace(/\/$/, '');

    // Fetch repo structure from GitHub API
    const response = await axios.get(
      `https://api.github.com/repos/${repoPath}/contents`,
      {
        headers: {
          'User-Agent': 'Repository-Analyzer',
          Accept: 'application/vnd.github+json'
        }
      }
    );

    res.json({
      user: user.username,
      repoUrl: user.githubUrl,
      structure: response.data
    });
    
  } catch (err) {
    console.error('Visualization Error:', err);
    res.status(500).json({ 
      message: 'Error visualizing repository',
      error: err.response?.data?.message || err.message
    });
  }
};