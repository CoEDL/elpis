from typing import Callable, Dict
from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
import subprocess
from elpis.engines.common.objects.model import Model
from elpis.engines.common.errors import InterfaceError

MISSING_MODEL_MESSAGE = "No current model exists (perhaps create one first)"
MISSING_MODEL_RESPONSE = jsonify(
    {"status": 404, "data": MISSING_MODEL_MESSAGE})

MISSING_LOG_MESSAGE = "No log file was found, couldn't parse the results"
MISSING_LOG_RESPONSE = jsonify({"status": 404, "data": MISSING_LOG_MESSAGE})

bp = Blueprint("model", __name__, url_prefix="/model")


def run(cmd: str) -> str:
    import shlex
    """Captures stdout/stderr and writes it to a log file, then returns the
    CompleteProcess result object"""
    args = shlex.split(cmd)
    process = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return process.stdout


@bp.route("/new", methods=['POST'])
def new():
    interface = app.config['INTERFACE']
    try:
        model = interface.new_model(request.json["name"])
        print(f"New model created {model.name} {model.hash}")
    except InterfaceError as e:
        return jsonify({
            "status": 500,
            "error": e.human_message
        })
    dataset = interface.get_dataset(request.json['dataset_name'])
    model.link_dataset(dataset)
    app.config['CURRENT_DATASET'] = dataset
    if 'engine' in request.json and request.json['engine'] == 'kaldi':
        pron_dict = interface.get_pron_dict(request.json['pron_dict_name'])
        model.link_pron_dict(pron_dict)
        app.config['CURRENT_PRON_DICT'] = pron_dict
    if 'engine' in request.json and request.json['engine'] in ["espnet", "hftransformers"]:
        pass
    model.build_structure()
    app.config['CURRENT_MODEL'] = model
    data = {
        "config": model.config._load()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/load", methods=['POST'])
def load():
    interface = app.config['INTERFACE']
    model = interface.get_model(request.json["name"])
    app.config['CURRENT_DATASET'] = model.dataset
    app.config['CURRENT_PRON_DICT'] = model.pron_dict
    app.config['CURRENT_MODEL'] = model
    data = {
        "config": model.config._load()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/list", methods=['GET'])
def list_existing():
    interface = app.config['INTERFACE']
    data = {
        "list": [{
            'name': model['name'],
            'dataset_name': model['dataset_name'],
            'engine_name': model['engine_name'],
            'pron_dict_name': model['pron_dict_name'],
            'status': model['status'],
            'results': model['results']
        } for model in interface.list_models_verbose()]
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/settings", methods=['POST'])
def settings():
    def setup(model: Model):
        if request.method == 'POST':
            model.ngram = request.json['ngram']

    def build_data(model: Model):
        return {
            "settings": {
                "ngram": model.ngram
            }
        }

    return _model_response(setup=setup, build_data=build_data)


@bp.route("/train", methods=['GET'])
def train():
    def setup(model: Model):
        model.train(on_complete=lambda: print('Trained model!'))

    def build_data(model: Model):
        return {
            "status": model.status,
            "stage_status": model.stage_status
        }

    return _model_response(setup=setup, build_data=build_data)


@bp.route("/status", methods=['GET'])
def status():
    def build_data(model: Model):
        return {
            "status": model.status,
            "stage_status": model.stage_status
        }
    return _model_response(build_data=build_data)


@bp.route("/log", methods=['GET'])
def log():
    def build_data(model: Model):
        return {
            "log": model.log
        }
    return _model_response(build_data=build_data)


@bp.route("/results", methods=['GET'])
def results():
    model: Model = app.config['CURRENT_MODEL']
    if model is None:
        return MISSING_MODEL_RESPONSE
    try:
        results = model.get_train_results()
    except FileNotFoundError:
        print("Results file not found.")
        return MISSING_LOG_RESPONSE
    data = {
        "results": results
    }
    return jsonify({
        "status": 200,
        "data": data
    })


def _model_response(build_data: Callable[[Model], Dict],
                    setup: Callable[[Model], None] = (lambda model: None)):
    """Sets up the model and returns the requested data, based on a supplied 
    function to extract the data from the model, with an optional setup function
    that will run first.

    Parameters:
        build_data: A function to extract the necessary information from the model.
        setup: An optional function to run before the data transformation.

    Returns:
        A 200 response with the supplied data, if successful. 
    """
    model: Model = app.config['CURRENT_MODEL']
    if model is None:
        return MISSING_MODEL_RESPONSE

    setup(model)
    data = build_data(model)

    return jsonify({
        "status": 200,
        "data": data
    })
