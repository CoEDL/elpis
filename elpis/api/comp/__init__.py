from ...blueprint import Blueprint

bp = Blueprint("comp", __name__, url_prefix="/comp")

@bp.route("/")
def something():
    return '{"something": "nothing"}'

from flask import Flask,redirect, url_for

@bp.route("/see")
def see():
    return redirect(url_for('api.model.new'))

@bp.route("/this")
def this():
    return "a non-page"
