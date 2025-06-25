import os
import re
import requests
import json

from datetime import datetime
from pathlib import Path
from flask import render_template, request, redirect, url_for, flash
from flask_login import UserMixin, AnonymousUserMixin, login_user, logout_user, login_required, current_user
from app import login_manager
from app.auth import auth


class User(UserMixin):
    """User class for Flask-Login integration."""
    def __init__(self, token):
        self.id = token

        
@login_manager.user_loader
def load_user(token):
    return User(token)


class AnonymousUser(AnonymousUserMixin):
    """Anonymous user class for Flask-Login integration."""
    def __init__(self):
        self.id = None


login_manager.anonymous_user = AnonymousUser


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps(dict(username=username, password=password))
        r = requests.post('http://localhost:8085/api/v1/auth/login', headers=headers, data=payload)
        if r.status_code == 200:
            try:
                login_user(User(r.json()['token']))
                # FIXME: 분리할 것
                userid = current_user.get_id()
                agent = request.headers.get("User-Agent", "")
                remote_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
                headers = {'Content-Type': 'application/json'}
                data = {
                    "text": f"{datetime.now().isoformat()}::AUTH::{remote_addr}::{agent}::{userid}",
                    "chat_id": os.environ.get('TELEGRAM_CHAT_ID'),
                }
                boturl = os.environ.get('TELEGRAM_BOT_URL')
                if boturl:
                    r = requests.post(boturl, headers=headers, data=json.dumps(data))
            except ValueError:
                pass
            return redirect(url_for('main.index'))
        flash('Invalid authentication.')
    return render_template('login.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
