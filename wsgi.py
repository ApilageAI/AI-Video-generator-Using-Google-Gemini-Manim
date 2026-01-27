"""
WSGI entry point for production deployment
"""
from app import app, start_worker
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Start the background worker for video processing
start_worker()

# WSGI application
application = app

if __name__ == "__main__":
    # For development only
    app.run(host='0.0.0.0', port=5000, debug=False)
