from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    on_breach=None
)

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.passwords import passwords_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(passwords_bp, url_prefix='/passwords')

    from app.models.user import User
    from app.models.password_entry import PasswordEntry
    from app.models.audit_log import AuditLog

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
            return jsonify({
            'error': 'Too many requests',
            'message': 'Rate limit exceeded. Please try again in one minute.'
        }), 429
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'error': 'Method not allowed'}), 405

    return app