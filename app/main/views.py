import os

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
    md_file = f"{os.environ['WEB_NOTE_HOME']}/note1.md"
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
    md_out = md.render(md_text)

    return render_template('index.html', md_out=md_out)
