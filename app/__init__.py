from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.passwords import passwords_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(passwords_bp, url_prefix='/passwords')

    from app.models.user import User
    from app.models.password_entry import PasswordEntry

    return app