#!/bin/bash
echo "Starting Repository Analyzer Backend..."

# Create necessary directories
mkdir -p analysis_temp

# Start Gunicorn
gunicorn --workers=2 \
         --timeout=120 \
         --log-level=debug \
         --bind=0.0.0.0:$PORT \
         --access-logfile=- \
         --error-logfile=- \
         app:app 