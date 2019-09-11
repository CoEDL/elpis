from flask import request
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.dataset import Dataset


bp = Blueprint("databundle", __name__, url_prefix="/databundle")


@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    dataset = kaldi.new_dataset(request.json['name'])
    app.config['CURRENT_DATABUNDLE'] = dataset
    return jsonify({
        "status": "ok",
        "data": dataset.config._load()
    })


@bp.route("/load", methods=['GET', 'POST'])
def load():
    kaldi: KaldiInterface = app.config['INTERFACE']
    dataset = kaldi.get_dataset(request.json['name'])
    app.config['CURRENT_DATABUNDLE'] = dataset
    return jsonify({
        "status": "ok",
        "data": dataset.config._load()
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    dataset: Dataset = app.config['CURRENT_DATABUNDLE']
    if dataset is None:
        return '{"status":"error", "data": "No current data bundle exists (prehaps create one first)"}'
    if request.method == 'POST':
        dataset.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": dataset.name})


@bp.route("/settings", methods=['GET', 'POST'])
def settings():
    dataset: Dataset = app.config['CURRENT_DATABUNDLE']
    if dataset is None:
        return '{"status":"error", "data": "No current data bundle exists (prehaps create one first)"}'
    if request.method == 'POST':
        dataset.tier = request.json['tier']
        # TODO make this an optional parameter
    return jsonify({
        "status": "ok",
        # TODO formalise the setting of the data bundle
        "data": {"tier": dataset.tier}})


@bp.route("/list", methods=['GET', 'POST'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    return jsonify({
        "status": "ok",
        "data": kaldi.list_datasets()
    })


@bp.route("/files", methods=['GET', 'POST'])
def files():
    dataset: Dataset = app.config['CURRENT_DATABUNDLE']
    if dataset is None:
        return '{"status":"error", "data": "No current data bundle exists (prehaps create one first)"}'
    if request.method == 'POST':
        # TODO think about this below
        # files_overwrite = request.form["filesOverwrite"]
        # print('filesOverwrite:', files_overwrite)
        for file in request.files.getlist("file"):
            dataset.add_fp(file, file.filename)
    return jsonify(dataset.files)


@bp.route("/prepare", methods=['GET', 'POST'])
def prepare():
    dataset: Dataset = app.config['CURRENT_DATABUNDLE']
    if dataset is None:
        return '{"status":"error", "data": "No current data bundle exists (prehaps create one first)"}'
    dataset.process()
    with dataset.pathto.word_count_json.open() as fin:
        return fin.read()
