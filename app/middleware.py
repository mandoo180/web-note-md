import os
import jwt
import json
import requests
from datetime import datetime
from flask import request, redirect, url_for
from flask_login import current_user


def trace_log_middleware(app):
    """Register request tracing middleware for Flask app."""

    @app.before_request
    def log_request():
        if request.path.startswith('/static'):
            return None
        agent = request.headers.get("User-Agent", "")
        remote_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
        app.logger.info(f"{datetime.now().isoformat()}::{request.method}::{request.path}::{remote_addr}::{agent}")


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
