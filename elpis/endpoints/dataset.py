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

# Handle file uploads. For now, default to the "original" dir.
# Dataset.add_fp() will check file names, moving corpora files to own dir
# later we might have a separate GUI widget for corpora files
# which could have a different route with a different destination.
# add_fp scans the uploaded files and returns lists of all tier types and tier names for eafs
@bp.route("/files", methods=['POST'])
def files():
    dataset: Dataset = app.config['CURRENT_DATASET']
    if dataset is None:
        return jsonify({"status": 404,
                        "data": "No current dataset exists (perhaps create one first)"})
    if request.method == 'POST':
        for file in request.files.getlist("file"):
            dataset.add_fp(fp=file, fname=file.filename, destination='original')
        dataset.get_elan_tier_attributes(dataset.pathto.original)
        print(dataset.tier_types, dataset.tier_names)

    data = {
        "files": dataset.files,
        "tier_types": dataset.tier_types,
        "tier_names": dataset.tier_names
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
        dataset.tier_type = request.json['tier_type']
        dataset.tier_name = request.json['tier_name']
        dataset.config['punctuation_to_explode_by'] = request.json['punctuation_to_explode_by']
    print(f"saving settings {dataset.tier_type} {dataset.tier_name}")
    data = {
        "tier_type": dataset.tier_type,
        "tier_name": dataset.tier_name,
        "punctuation_to_explode_by": dataset.config['punctuation_to_explode_by']
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
