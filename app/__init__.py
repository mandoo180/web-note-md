from flask import Flask
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'not-safe-key'

    login_manager.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
