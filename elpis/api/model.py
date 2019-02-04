import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename
from ..blueprint import Blueprint
from . import comp

bp = Blueprint("model", __name__, url_prefix="/model")
bp.register_blueprint(comp.bp)


@bp.route("/new")
def new():
    return '{"status": "new model created"}'

@bp.route("/name")
def name():
    return ''
    
@bp.route("/date")
def date():
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


