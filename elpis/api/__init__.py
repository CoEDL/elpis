from ..blueprint import Blueprint
from . import model

bp = Blueprint("api", __name__, url_prefix="/api")
bp.register_blueprint(model.bp)

@bp.route("/")
def whole_state():
    return '{"yet to be named": "the enture model!"}'

from flask import Flask,redirect, url_for

@bp.route("/re")
def re():
    return redirect(url_for('elpis.api.model.new'))

@bp.route("/em")
def em():
    return "empty page"
