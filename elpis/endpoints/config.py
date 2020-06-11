from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from pathlib import Path
from elpis.engines import Interface
import shutil

bp = Blueprint("config", __name__, url_prefix="/config")


@bp.route("/reset", methods=['GET', 'POST'])
def reset():
    current_interface_path = app.config['INTERFACE'].path
    shutil.rmtree(current_interface_path)
    app.config['INTERFACE'] = Interface(current_interface_path)
    app.config['CURRENT_DATASET'] = None # not okay for multi-user
    app.config['CURRENT_PRON_DICT'] = None # not okay for multi-user
    app.config['CURRENT_MODEL'] = None # not okay for multi-user
    data = {
        "message": "reset ok"
    }
    return jsonify({
        "status": 200,
        "data": data
    })
