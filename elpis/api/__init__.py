from ..blueprint import Blueprint
print("# start api.init")
bp = Blueprint("api", __name__, url_prefix="/api")
print("# created api.bp")

from . import model
print("# imported  model")
bp.register_blueprint(model.bp)
print("# registered model.bp into api.bp")

@bp.route("/")
def whole_state():
    return '{"yet to be named": "the enture model!"}'
print("# routed api.bp('/')")

from flask import Flask,redirect, url_for

@bp.route("/re")
def re():
    return redirect(url_for('elpis.api.model.new'))

@bp.route("/em")
def em():
    return "empty page"
