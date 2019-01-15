from flask import Blueprint, request, Response


bp = Blueprint("corpus", __name__, url_prefix="/corpus")


@bp.route("/wav", methods=("GET", "POST"))
def wav():
    if request.method == "POST":
        # Process incoming wav file
        return 200
    elif request.method == "GET":
        # Return a list of all wav files
        return 200


@bp.route("/elan", methods=("GET", "POST"))
def elan():
    if request.method == "POST":
        # Process incoming elan file
        return 200
    elif request.method == "GET":
        # Return a list of all elan files
        return 200


@bp.route("/trs", methods=("GET", "POST"))
def trs():
    if request.method == "POST":
        # Process incoming trs file
        return 200
    elif request.method == "GET":
        # Return a list of all trs files
        return 200


@bp.route("/wordlist", methods=("GET", "POST"))
def wordlist():
    if request.method == "POST":
        # Process incoming wordlist file
        return 200
    elif request.method == "GET":
        # Return current list of words
        return 200
