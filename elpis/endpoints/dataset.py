from flask import request
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.dataset import Dataset


bp = Blueprint("dataset", __name__, url_prefix="/dataset")


@bp.route("/new", methods=['POST'])
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


@bp.route("/load", methods=['POST'])
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


@bp.route("/list", methods=['GET'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    data = {
        "list": kaldi.list_datasets()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/files", methods=['POST'])
def files():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return jsonify({"status":404, "data": "No current dataset exists (perhaps create one first)"})
    if request.method == 'POST':
        for file in request.files.getlist("file"):
            dataset.add_fp(file, file.filename)
    data = {
        "files": dataset.files
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/settings", methods=['POST'])
def settings():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return jsonify({"status":404, "data": "No current dataset exists (perhaps create one first)"})
    if request.method == 'POST':
        dataset.tier = request.json['tier']
    data = {
        "tier": dataset.tier
    }
    return jsonify({
        "status": 200,
        "data": data
    })

# TODO prepare endpoint returns file contents as text.
# Probably nicer to send back JSON data instead

@bp.route("/prepare", methods=['POST'])
def prepare():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return jsonify({"status":404, "data": "No current dataset exists (perhaps create one first)"})
    dataset.select_importer('Elan')
    dataset.process()
    with dataset.pathto.word_count_json.open() as fin:
        wordlist = fin.read()
    data = {
        "wordlist": wordlist
    }
    return jsonify({
        "status": 200,
        "data": data
    })
