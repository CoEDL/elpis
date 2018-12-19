"""
Babylon is the server component for Elpis.
"""

import os
os.environ["FLASK_ENV"] = "development"

from flask import Flask
server = Flask(__name__)

@server.route("/")
def hello():
    with open("src/templates/example.tpl.html", "r") as fout:
        return fout.read()