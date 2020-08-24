from flask import request
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.engines import Interface
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.errors import InterfaceError
import os

bp = Blueprint("dataset", __name__, url_prefix="/dataset")


@bp.route("/new", methods=['POST'])
def new():
    interface: Interface = app.config['INTERFACE']
    try:
        dataset = interface.new_dataset(request.json['name'])
    except InterfaceError as e:
        return jsonify({
            "status": 500,
            "error": e.human_message
        })
    app.config['CURRENT_DATASET'] = dataset
    data = {
        "state": dataset.config._load()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/load", methods=['POST'])
def load():
    interface: Interface = app.config['INTERFACE']
    dataset = interface.get_dataset(request.json['name'])
    app.config['CURRENT_DATASET'] = dataset
    data = {
        "state": dataset.config._load()
    }
    if os.path.exists(dataset.pathto.word_count_json):
        with dataset.pathto.word_count_json.open() as fin:
            wordlist = fin.read()
        data.update({
            "wordlist": wordlist
        })
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/list", methods=['GET'])
def list_existing():
    interface: Interface = app.config['INTERFACE']
    data = {
        "list": interface.list_datasets()
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
        data = {"files": dataset.files}
        dataset.auto_select_importer()
        if dataset.importer is not None:
            # maybe a comment here will force this file update?
            dataset.validate()
            dataset.refresh_ui()
            data.update({
                'settings': dataset.importer.get_settings(),
                "ui": dataset.importer.get_ui(),
                "importer_name": dataset.importer.get_name()
            })
    return jsonify({
        "status": 200,
        "data": data
    })

@bp.route("/files/delete/<filename>", methods=['POST'])
def delete_file(dataset: Dataset, filename: str):
    if request.method == 'POST':
        dataset.remove_file(filename)
        data = {"files": dataset.files}
        if dataset.importer is not None:
            # maybe a comment here will force this file update?
            dataset.validate()
            dataset.refresh_ui()
            data.update({
                'settings': dataset.importer.get_settings(),
                "ui": dataset.importer.get_ui(),
                "importer_name": dataset.importer.get_name()
            })
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
