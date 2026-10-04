"""
Application configuration for Capacity 1
"""

import os
from datetime import timedelta

class Config:
    """Base configuration for Flask application"""
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///capacity1.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }
    
    # JSON configuration
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application configuration
    APP_NAME = 'Capacidade 1'
    APP_VERSION = '1.0.0'
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    ITEMS_PER_PAGE = 10
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Timezone
    TIMEZONE = 'UTC'
