import os
import logging
from flask import Flask, render_template

from .middleware import jwt_auth_middleware, trace_log_middleware
from flask_login import LoginManager, current_user as flask_current_user


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_filename=None):
    """Create and configure the Flask application."""
    if config_filename:
        os.environ['FLASK_CONFIG'] = config_filename
    
    app = Flask(__name__)
    
    if not app.logger.handlers:
        logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    app.secret_key = os.environ['FLASK_LOGIN_SECRET']

    login_manager.init_app(app)
    jwt_auth_middleware(app)
    trace_log_middleware(app)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("500.html"), 500

    return app
