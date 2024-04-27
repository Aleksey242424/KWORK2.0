from flask import Flask
from config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    from app.main import main
    from app.admin import admin
    from app.auth import auth
    from app.profile import profile
    app.register_blueprint(main,url_prefix="/")
    app.register_blueprint(admin,url_prefix='/admin/')
    app.register_blueprint(auth,url_prefix="/auth/")
    app.register_blueprint(profile,url_prefix="/profile/")
    
    return app