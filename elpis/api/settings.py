import os
from pathlib import Path
from flask import Blueprint, redirect, request, url_for, escape
from werkzeug.utils import secure_filename


ELPIS_ROOT_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(ELPIS_ROOT_DIR, "Uploaded_files")
ALLOWED_EXTENSIONS = {'wav', 'eaf', 'trs', 'wordlist'}
bp = Blueprint("settings", __name__, url_prefix="/settings")


"""
Settings Route
"""
@bp.route("/settings", methods=("GET", "POST"))
def settings(Model):
    if request.method == "POST":
            # Add settings for model
            state.add_settings(Settings)
            return 200
    elif request.method == "GET":
        # Returns all model settings
        state.settings.get_settings()
        return 200


