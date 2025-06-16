import os
from flask import Flask
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['FLASK_LOGIN_SECRET']

    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
