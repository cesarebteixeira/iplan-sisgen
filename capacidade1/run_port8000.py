"""
Entry point for running the Capacidade 1 application on PORT 8000
(Use this if port 5000 is blocked by Windows firewall/permissions)

Usage on Windows 11:
    python run_port8000.py

The application will be available at http://localhost:8000
"""
import os
import sys
from pathlib import Path

# Add the application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from app import create_app, db


def main():
    """Create and run the Flask application on port 8000"""
    app = create_app()
    
    # Initialize database tables
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")
    
    # Run the application on port 8000
    print(f"Starting {app.config['APP_NAME']}")
    print(f"Version: {app.config['APP_VERSION']}")
    print("Access the application at http://localhost:8000")
    print("")
    
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=app.config['DEBUG'],
        use_reloader=False,
        use_debugger=False,
        threaded=True
    )


if __name__ == '__main__':
    main()

