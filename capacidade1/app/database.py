"""
Database utilities for Capacity 1
"""

def init_db(app):
    """Initialize database and create all tables"""
    from app import db
    
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")

def drop_all(app):
    """Drop all tables (use with caution)"""
    from app import db
    
    with app.app_context():
        db.drop_all()
        print("All database tables dropped")
