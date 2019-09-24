from flask import request
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.dataset import Dataset


bp = Blueprint("dataset", __name__, url_prefix="/dataset")


@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    dataset = kaldi.new_dataset(request.json['name'])
    app.config['CURRENT_DATASET'] = dataset
    data = {
        "config": dataset.config._load()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/load", methods=['GET', 'POST'])
def load():
    kaldi: KaldiInterface = app.config['INTERFACE']
    dataset = kaldi.get_dataset(request.json['name'])
    app.config['CURRENT_DATASET'] = dataset
    data = {
        "config": dataset.config._load()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return '{"status":"error", "data": "No current dataset exists (perhaps create one first)"}'
    if request.method == 'POST':
        dataset.name = request.json['name']
    data = {
        "name": dataset.name
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/settings", methods=['GET', 'POST'])
def settings():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return '{"status":"error", "data": "No current dataset exists (perhaps create one first)"}'
    if request.method == 'POST':
        dataset.tier = request.json['tier']
    data = {
        "tier": dataset.tier
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/list", methods=['GET', 'POST'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    data = {
        "list": kaldi.list_datasets()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/files", methods=['GET', 'POST'])
def files():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return '{"status":"error", "data": "No current dataset exists (perhaps create one first)"}'
    if request.method == 'POST':
        for file in request.files.getlist("file"):
            dataset.add_fp(file, file.filename)
    # TODO fix this to return a json wrapper
    return jsonify(dataset.files)


@bp.route("/prepare", methods=['GET', 'POST'])
def prepare():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return '{"status":"error", "data": "No current dataset exists (perhaps create one first)"}'
    dataset.process()
    with dataset.pathto.word_count_json.open() as fin:
        # TODO this returns file contents. fix this to return json wrapper
        return fin.read()
