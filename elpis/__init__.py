import os
os.environ["FLASK_ENV"] = "development"

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    with open("elpis/templates/example.tpl.html", "r") as fout:
        return fout.read()