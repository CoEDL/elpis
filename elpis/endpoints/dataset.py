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
    dataset.select_importer('Elan')
    app.config['CURRENT_DATASET'] = dataset
    data = {
        "state": dataset.state # TODO: ensure we use get_state() in the future
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

def require_dataset(f):
    def wrapper(*args, **kwargs):
        dataset: Dataset = app.config['CURRENT_DATASET']
        if dataset is None:
            return jsonify({"status": 404,
                            "data": "No current dataset exists (perhaps create one first)"})
        return f(dataset, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Handle file uploads. For now, default to the "original" dir.
# Dataset.add_fp() will check file names, moving corpora files to own dir
# later we might have a separate GUI widget for corpora files
# which could have a different route with a different destination.
# add_fp scans the uploaded files and returns lists of all tier types and tier names for eafs
@bp.route("/files", methods=['POST'])
@require_dataset
def files(dataset: Dataset):
    if request.method == 'POST':
        for file in request.files.getlist("file"):
            dataset.add_fp(fp=file, fname=file.filename, destination='original')
        dataset.validate()
        dataset.refresh_ui()
    data = {
        "files": dataset.files,
        'settings': dataset.importer.get_settings(),
        "ui": dataset.importer.get_ui()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/import/settings", methods=['GET', 'POST'])
@require_dataset
def settings(dataset: Dataset):
    # Only edit if POST
    if request.method == 'POST':
        settings = dataset.importer.get_settings()
        for key in request.json.keys():
            if key in settings.keys():
                dataset.importer.set_setting(key, request.json[key])
            else:
                pass # TODO throw an invalid key error here?
        
    # Return imports current/updated settings.
    data = {
        'settings': dataset.importer.get_settings()
    }
    return jsonify({
        "status": 200,
        "data": data
    })

@bp.route("/import/ui", methods=['GET', 'POST'])
@require_dataset
def settings_ui(dataset: Dataset):
    data = {
        'ui': dataset.importer.get_ui()
    }
    return jsonify({
        "status": 200,
        "data": data
    })

@bp.route("/punctuation_to_explode_by", methods=['POST'])
@require_dataset
def punctuation_to_explode_by(dataset: Dataset):
    if 'punctuation_to_explode_by' in request.json.keys():
        dataset.punctuation_to_explode_by = request.json['punctuation_to_explode_by']
    data = {
        'punctuation_to_explode_by': dataset.punctuation_to_explode_by
    }
    return jsonify({
        "status": 200,
        "data": data
    })

# TODO prepare endpoint returns file contents as text.
# Probably nicer to send back JSON data instead

@bp.route("/prepare", methods=['POST'])
@require_dataset
def prepare(dataset: Dataset):
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
