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

@app.errorhandler(Exception)
def handle_error(error):
    logger.exception("An error occurred")
    return jsonify({
        'error': str(error),
        'status': 'error'
    }), 500

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_repo():
    try:
        app.logger.debug("Received analyze request")
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

        # Clone repo in background
        def clone_and_analyze():
            try:
                # Clone repository with timeout
                process = subprocess.run(
                    ['git', 'clone', '--depth', '1', repo_url, str(analysis_dir)],
                    check=True,
                    capture_output=True,
                    timeout=60  # 1 minute timeout
                )
                
                analyses[analysis_id]['status'] = 'processing'
                
                # Analyze Java code
                analyses[analysis_id]['results']['java'] = analyze_java(analysis_dir)
                analyses[analysis_id]['status'] = 'completed'
                
            except subprocess.TimeoutExpired:
                analyses[analysis_id]['status'] = 'failed'
                analyses[analysis_id]['error'] = 'Repository cloning timed out'
            except Exception as e:
                analyses[analysis_id]['status'] = 'failed'
                analyses[analysis_id]['error'] = str(e)
            finally:
                # Clean up repository
                shutil.rmtree(analysis_dir, ignore_errors=True)

        # Start analysis in background thread
        from threading import Thread
        Thread(target=clone_and_analyze, daemon=True).start()

        return jsonify({
            'id': analysis_id,
            'status': 'initiated'
        }), 202

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/v1/analysis/<analysis_id>/status', methods=['GET'])
def get_analysis_status(analysis_id):
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

@app.route('/api/v1/analysis/<analysis_id>/<language>', methods=['GET'])
def get_analysis_results(analysis_id, language):
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

@app.route('/api/v1', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 