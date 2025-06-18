import os
import jwt
import requests
from flask import request, redirect, url_for
from flask_login import current_user


def jwt_auth_middleware(app):
    """Register JWT authentication middleware for Flask app."""
    @app.before_request
    def check_jwt():
        if request.endpoint in {"auth.login", "static"}:
            return None
        if current_user.is_authenticated:
            headers = { 'Authorization': f'Bearer {current_user.id}' }
            r = requests.get('http://localhost:8085/api/v1/auth/verify', headers=headers)
            if r.status_code == 200:
                return None
            return redirect(url_for('auth.logout'))
        return redirect(url_for('auth.login'))
        # return redirect(url_for('auth.login'))
        # return redirect(url_for('auth.login', next=request.path))
