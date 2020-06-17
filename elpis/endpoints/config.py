from ..blueprint import Blueprint
from flask import current_app as app, jsonify, request
from pathlib import Path
from elpis.engines import Interface, ENGINES
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

@bp.route("/engine/list", methods=['GET', 'POST'])
def engine_list():
    data = {
        'engine_list': ENGINES.keys()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/engine/load", methods=['GET', 'POST'])
def engine_load():
    engine_name = request.json["engine_name"]
    if engine_name not in ENGINES:
        return jsonify({"status": 404,
            "data": "No current dataset exists (perhaps create one first)"})
    engine = ENGINES[engine_name]
    interface = app.config['INTERFACE']
    interface.set_engine(engine)
    data = {
        "engine": engine_name
    }
    return jsonify({
        "status": 200,
        "data": data
    })
