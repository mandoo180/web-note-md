import os

from flask import render_template
from markdown import markdown
from app.main import main


@main.route('/')
def index():
    md_file = f"{os.environ['WEB_NOTE_HOME']}/note1.md"
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
    md_out = markdown(md_text)

    return render_template('index.html', md_out=md_out)
