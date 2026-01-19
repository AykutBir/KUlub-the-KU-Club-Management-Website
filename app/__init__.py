from flask import Flask
from dotenv import load_dotenv
from app.routes.auth import auth_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.admin_routes import admin_bp
from app.db import init_db

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    
    # Set login route as default
    @app.route('/')
    def index():
        from flask import redirect
        return redirect('/login')
    
    return app
