from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import subprocess
import os
import shutil
import time
from pathlib import Path

# Language-specific analyzers
from analyzers.java_analyzer import analyze_java

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://repository-analyzer-frontend.vercel.app",
            "http://localhost:3000"
        ]
    }
})

ANALYSIS_BASE = Path('/tmp/code_analysis')
ANALYSIS_BASE.mkdir(exist_ok=True)

# In-memory storage for demonstration (use database in production)
analyses = {}

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_repo():
    data = request.get_json()
    repo_url = data.get('url')
    
    if not repo_url or 'github.com' not in repo_url:
        return jsonify({'error': 'Invalid GitHub repository URL'}), 400

    analysis_id = str(uuid.uuid4())
    analysis_dir = ANALYSIS_BASE / analysis_id
    analysis_dir.mkdir()

    analyses[analysis_id] = {
        'status': 'cloning',
        'languages': {},
        'results': {}
    }

    # Clone repo in background
    def clone_and_analyze():
        try:
            # Clone repository
            subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, str(analysis_dir)],
                check=True
            )
            
            analyses[analysis_id]['status'] = 'processing'
            
            # Analyze different languages
            analyses[analysis_id]['results']['java'] = analyze_java(analysis_dir)
            
            analyses[analysis_id]['status'] = 'completed'
            
        except Exception as e:
            analyses[analysis_id]['status'] = 'failed'
            analyses[analysis_id]['error'] = str(e)
        finally:
            # Clean up repository
            shutil.rmtree(analysis_dir, ignore_errors=True)

    # Start analysis in background thread
    from threading import Thread
    Thread(target=clone_and_analyze).start()

    return jsonify({'id': analysis_id}), 202

@app.route('/api/v1/analysis/<analysis_id>/status')
def get_analysis_status(analysis_id):
    analysis = analyses.get(analysis_id)
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    return jsonify({
        'status': analysis['status'],
        'error': analysis.get('error')
    })

@app.route('/api/v1/analysis/<analysis_id>/<language>')
def get_analysis_results(analysis_id, language):
    analysis = analyses.get(analysis_id)
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    if analysis['status'] != 'completed':
        return jsonify({'error': 'Analysis not complete'}), 425
    
    if language not in analysis['results']:
        return jsonify({'error': 'Language not analyzed'}), 404
    
    return jsonify({
        'callGraph': analysis['results'][language]['call_graph'],
        'metrics': analysis['results'][language]['metrics']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 