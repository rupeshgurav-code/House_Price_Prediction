import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the Flask app to be imported as 'app'
# The app is already defined in app.py, we just re-export it here
