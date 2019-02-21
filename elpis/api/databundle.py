from flask import request
from ..blueprint import Blueprint
from .kaldi import bp as parent_bp
from flask import current_app as app, jsonify
from ..kaldi.interface import KaldiInterface
from ..kaldi.dataset import Dataset


bp = Blueprint("databundle", __name__, url_prefix="/databundle")
bp.register_blueprint(parent_bp)


@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    ds = kaldi.new_dataset(request.values.get("name"))
    app.config['CURRENT_DATABUNDLE'] = ds
    return jsonify({
        "status": "ok",
        "data": ds.config._load()
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    ds: Dataset = app.config['CURRENT_DATABUNDLE']
    if ds is None:
        return '{"status":"error", "data": "No current data bundle exists (prehaps create one first)"}'
    if request.method == 'POST':
        ds.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": ds.name})


@bp.route("/list")
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    return jsonify({
        "status": "ok",
        "data": kaldi.list_datasets()
    })


@bp.route("/files", methods=['GET', 'POST'])
def files():
    ds: Dataset = app.config['CURRENT_DATABUNDLE']
    if ds is None:
        return '{"status":"error", "data": "No current data bundle exists (prehaps create one first)"}'
    if request.method == 'POST':
        files_overwrite = request.form["filesOverwrite"]
        print('filesOverwrite:', files_overwrite)
        for file in request.files.getlist("file"):
            ds.add_fp(file, file.filename)
    return jsonify(ds.files)


@bp.route("/prepare", methods=['GET', 'POST'])
def prepare():
    ds: Dataset = app.config['CURRENT_DATABUNDLE']
    if ds is None:
        return '{"status":"error", "data": "No current data bundle exists (prehaps create one first)"}'
    ds.process()
    with ds.pathto.word_count_json.open() as fin:
        return fin.read()
