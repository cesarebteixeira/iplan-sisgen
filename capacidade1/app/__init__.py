"""
Flask application factory for Capacity 1 (Network Structure and Spending Management)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Create and configure the Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Configure JSON to use UTF-8
    app.config['JSON_AS_ASCII'] = False
    
    # Add UTF-8 charset to response headers
    @app.after_request
    def set_charset(response):
        if 'Content-Type' in response.headers:
            content_type = response.headers['Content-Type']
            if 'text/html' in content_type and 'charset' not in content_type:
                response.headers['Content-Type'] = content_type + '; charset=utf-8'
        return response
    
    # Register blueprints
    from app.routes import (
        bairro_routes,
        conta_routes,
        feriado_routes,
        fonte_routes,
        grupo_routes,
        periodo_routes,
        projeto_routes,
        tipo_processo_routes,
        transferencia_routes,
        transicao_routes,
        unidade_routes,
        vinculo_routes,
        consulta_routes
    )
    
    app.register_blueprint(bairro_routes.bp)
    app.register_blueprint(conta_routes.bp)
    app.register_blueprint(feriado_routes.bp)
    app.register_blueprint(fonte_routes.bp)
    app.register_blueprint(grupo_routes.bp)
    app.register_blueprint(periodo_routes.bp)
    app.register_blueprint(projeto_routes.bp)
    app.register_blueprint(tipo_processo_routes.bp)
    app.register_blueprint(transferencia_routes.bp)
    app.register_blueprint(transicao_routes.bp)
    app.register_blueprint(unidade_routes.bp)
    app.register_blueprint(vinculo_routes.bp)
    app.register_blueprint(consulta_routes.bp)
    
    # Register index route
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')
    
    # Initialize database tables on first run
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            # If there's an error (e.g., tables already exist), continue anyway
            pass
    
    return app
