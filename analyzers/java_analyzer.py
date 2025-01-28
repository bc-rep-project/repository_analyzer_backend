import javalang
from pathlib import Path

def analyze_java(analysis_dir):
    """Analyze Java source code in the given directory."""
    try:
        # Find all Java files
        java_files = list(Path(analysis_dir).rglob('*.java'))
        
        # Basic metrics
        metrics = {
            'fileCount': len(java_files),
            'totalLines': sum(1 for f in java_files if f.is_file() for _ in open(f, encoding='utf-8')),
            'complexity': len(java_files)  # Simplified complexity metric
        }
        
        # Simple call graph
        nodes = [{'id': str(f.name), 'group': 1} for f in java_files]
        links = []  # In real implementation, analyze actual calls between files
        
        return {
            'callGraph': {
                'nodes': nodes,
                'links': links
            },
            'metrics': metrics
        }
        
    except Exception as e:
        print(f"Error analyzing Java code: {e}")
        return {
            'callGraph': {'nodes': [], 'links': []},
            'metrics': {'error': str(e)}
        } 