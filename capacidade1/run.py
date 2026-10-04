"""
Entry point for running the Capacidade 1 application

Usage on Windows 11:
    python run.py

The application will be available at http://localhost:8000
(Uses port 8000 to avoid Windows firewall restrictions on port 5000)
"""
import os
import sys
from pathlib import Path

# Add the application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from app import create_app, db


def main():
    """Create and run the Flask application"""
    app = create_app()
    
    # Initialize database tables
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")
    
    # Run the application
    print(f"Starting {app.config['APP_NAME']}")
    print(f"Version: {app.config['APP_VERSION']}")
    
    # Port priority: 8000 (primary), then 8080, then 5000
    # This avoids Windows firewall issues with port 5000
    ports_to_try = [8000, 8080, 5000]
    host = '127.0.0.1'
    port_used = None
    
    for port in ports_to_try:
        try:
            print(f"Access the application at http://localhost:{port}")
            port_used = port
            app.run(
                host=host,
                port=port,
                debug=app.config['DEBUG'],
                use_reloader=False,
                use_debugger=False,
                threaded=True
            )
            break  # Success, exit the loop
        except (OSError, PermissionError) as e:
            error_msg = str(e).lower()
            if "permission" in error_msg or "socket" in error_msg:
                if port == ports_to_try[-1]:  # Last port in list
                    print(f"\nâŒ Error: Could not bind to any port: {e}")
                    raise
                else:
                    next_port = ports_to_try[ports_to_try.index(port) + 1]
                    print(f"\nâš ï¸  Port {port} has socket permission issues")
                    print(f"Trying alternative port {next_port}...\n")
            else:
                raise


if __name__ == '__main__':
    main()

