from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import subprocess
import os
import shutil
import time
from pathlib import Path
import logging

# Language-specific analyzers
from analyzers.java_analyzer import analyze_java

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS for all routes
CORS(app)

# Ensure base directory exists
ANALYSIS_BASE = Path('/tmp/code_analysis')
ANALYSIS_BASE.mkdir(exist_ok=True)

# In-memory storage for demonstration
analyses = {}

@app.route('/')
def root():
    return jsonify({
        'message': 'Repository Analyzer API',
        'version': '1.0',
        'status': 'operational'
    })

@app.route('/api/v1')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'endpoints': [
            '/api/v1/analyze',
            '/api/v1/analysis/<id>/status',
            '/api/v1/analysis/<id>/<language>'
        ]
    })

@app.errorhandler(Exception)
def handle_error(error):
    logger.exception("An error occurred")
    return jsonify({
        'error': str(error),
        'status': 'error'
    }), 500

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_repo():
    """Submit a repository for analysis"""
    try:
        logger.debug("Received analyze request")
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing repository URL',
                'status': 'error'
            }), 400
            
        repo_url = data['url']
        if not repo_url or 'github.com' not in repo_url:
            return jsonify({
                'error': 'Invalid GitHub repository URL',
                'status': 'error'
            }), 400

        analysis_id = str(uuid.uuid4())
        analysis_dir = ANALYSIS_BASE / analysis_id
        analysis_dir.mkdir(exist_ok=True)

        analyses[analysis_id] = {
            'status': 'cloning',
            'error': None,
            'results': {}
        }

        def clone_and_analyze():
            try:
                logger.info(f"Cloning repository: {repo_url}")
                process = subprocess.run(
                    ['git', 'clone', '--depth', '1', repo_url, str(analysis_dir)],
                    check=True,
                    capture_output=True,
                    timeout=60
                )
                
                analyses[analysis_id]['status'] = 'processing'
                logger.info(f"Analyzing repository: {analysis_id}")
                
                analyses[analysis_id]['results']['java'] = analyze_java(analysis_dir)
                analyses[analysis_id]['status'] = 'completed'
                logger.info(f"Analysis completed: {analysis_id}")
                
            except subprocess.TimeoutExpired:
                analyses[analysis_id]['status'] = 'failed'
                analyses[analysis_id]['error'] = 'Repository cloning timed out'
                logger.error(f"Cloning timeout: {analysis_id}")
            except Exception as e:
                analyses[analysis_id]['status'] = 'failed'
                analyses[analysis_id]['error'] = str(e)
                logger.error(f"Analysis failed: {analysis_id} - {str(e)}")
            finally:
                shutil.rmtree(analysis_dir, ignore_errors=True)

        # Start analysis in background thread
        from threading import Thread
        Thread(target=clone_and_analyze, daemon=True).start()

        return jsonify({
            'id': analysis_id,
            'status': 'initiated'
        }), 202

    except Exception as e:
        logger.exception("Error in analyze_repo")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/v1/analysis/<analysis_id>/status')
def get_analysis_status(analysis_id):
    """Get the status of an analysis"""
    logger.debug(f"Checking status for analysis: {analysis_id}")
    
    analysis = analyses.get(analysis_id)
    if not analysis:
        return jsonify({
            'error': 'Analysis not found',
            'status': 'error'
        }), 404
    
    return jsonify({
        'status': analysis['status'],
        'error': analysis.get('error', None)
    })

@app.route('/api/v1/analysis/<analysis_id>/<language>')
def get_analysis_results(analysis_id, language):
    """Get analysis results for a specific language"""
    logger.debug(f"Getting {language} results for analysis: {analysis_id}")
    
    analysis = analyses.get(analysis_id)
    if not analysis:
        return jsonify({
            'error': 'Analysis not found',
            'status': 'error'
        }), 404
    
    if analysis['status'] != 'completed':
        return jsonify({
            'error': 'Analysis not complete',
            'status': analysis['status']
        }), 425
    
    if language not in analysis['results']:
        return jsonify({
            'error': f'Language {language} not analyzed',
            'status': 'error'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': analysis['results'][language]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def server_error(error):
    logger.exception("Server error")
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 