#!/bin/bash

# Create necessary directories
mkdir -p /opt/render/project/src/analysis_temp

# Start Gunicorn
exec gunicorn \
    --workers=2 \
    --timeout=120 \
    --log-level=debug \
    --bind=0.0.0.0:$PORT \
    --access-logfile=- \
    --error-logfile=- \
    app:app 