import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename

'''New Code'''
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
    
