import os
import re

from pathlib import Path
from flask import render_template, request, redirect, url_for
from flask_login import current_user, UserMixin, login_user
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
# from pygments.formatters import HtmlFormatter
from app import login_manager
from app.main import main

md = MarkdownIt("commonmark", {
    "html": True,
    "linkify": True
}).use(footnote_plugin).use(tasklists_plugin)

# css = HtmlFormatter().get_style_defs(".highlight")

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username


@login_manager.user_loader
def load_user(username):
    return User(username)


@main.route('/')
def index():
    md_files = list(Path(f"{os.environ['WEB_NOTE_HOME']}").glob("*.md"))
    return render_template('index.html', md_files=md_files)


@main.route('/<filename>')
def view(filename):
    md_file = f"{os.environ['WEB_NOTE_HOME']}/{filename}"
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = re.sub(r"(?s)\A\+\+\+.*?\+\+\+\n*", "", f.read())
    md_out = md.render(md_text)

    return render_template('view.html', md_out=md_out)


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        # password = request.form['password']
        user = User(username)
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html')
