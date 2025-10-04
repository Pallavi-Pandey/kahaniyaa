#!/bin/sh

# Docker entrypoint script for frontend
# This script handles environment variable injection and starts nginx

set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting Kahaniyaa Frontend..."

# Create runtime environment configuration
# This allows environment variables to be injected at runtime
cat > /usr/share/nginx/html/env-config.js << EOF
window.ENV = {
  API_BASE_URL: '${API_BASE_URL:-/api}',
  APP_NAME: '${APP_NAME:-Kahaniyaa}',
  APP_VERSION: '${APP_VERSION:-1.0.0}',
  ENVIRONMENT: '${ENVIRONMENT:-production}'
};
EOF

log "Environment configuration created"

# Validate nginx configuration
nginx -t

log "Nginx configuration validated"

# Execute the main command
exec "$@"
