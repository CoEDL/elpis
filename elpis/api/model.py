import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename
from ..blueprint import Blueprint
from . import comp

bp = Blueprint("model", __name__, url_prefix="/model")
bp.register_blueprint(comp.bp)

Model model

@bp.route("/new")
def new():
    #assuming that this would only be a POST?
    this.model = state.Model()
    return '{"status": "new model created"}'

@bp.route("/name")
def name():
    if request.method == "POST":
        newModel.name(name) = name
    elif request.methd == "GET":
        pass
    return newModel.name()
    
@bp.route("/date")
def date():
    if request.method == "POST":
        newModel.
    return ''

@bp.route("/audio")
def audio():
    return ''

@bp.route("/transcription")
def transcription():
    return ''

@bp.route("/additionalWords")
def additionalWord():
    return ''

@bp.route("/pronunciation")
def pronunciation():
    return ''

@bp.route("/settings")
def settings():
    return ''


