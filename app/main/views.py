import os
import re

from pathlib import Path
from flask import render_template
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

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/list')
def file_list():
    md_files = list(Path(f"{os.environ['WEB_NOTE_HOME']}").glob("*.md"))
    return render_template('list.html', md_files=md_files)


@main.route('/view/<filename>')
def view(filename):
    md_file = f"{os.environ['WEB_NOTE_HOME']}/{filename}"
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = re.sub(r"(?s)\A\+\+\+.*?\+\+\+\n*", "", f.read())
    md_out = md.render(md_text)

    return render_template('view.html', md_out=md_out)
