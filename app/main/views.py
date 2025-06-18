import os
import re

from pathlib import Path
from flask import render_template, url_for, abort, send_file
from flask_login import login_required
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
# from pygments.formatters import HtmlFormatter
from app.main import main


md = MarkdownIt("commonmark", {
    "html": True,
    "linkify": True
}).use(footnote_plugin).use(tasklists_plugin)

# css = HtmlFormatter().get_style_defs(".highlight")


@main.route('/favicon.ico')
def favicon():
    return send_file(os.path.join(app.root_path, 'static'), 'favicon.ico')


@main.route('/')
@login_required
def index():
    md_files = list(Path(f"{os.environ['WEB_NOTE_HOME']}").glob("*.md"))
    return render_template('index.html', md_files=md_files)


@main.route('/view/<filename>')
@login_required
def view(filename):
    base_dir = Path(os.environ['WEB_NOTE_HOME']).resolve()
    file_path = (base_dir / filename).resolve()
    if not str(file_path).startswith(str(base_dir)) or not file_path.is_file():
        abort(404)
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = re.sub(r"(?s)\A\+\+\+.*?\+\+\+\n*", "", f.read())
    md_out = md.render(md_text)
    return render_template('view.html', md_out=md_out)
