from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
import subprocess
from elpis.engines import Interface
from elpis.objects.model import Model

from pathlib import Path

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
    interface: Interface = app.config['INTERFACE']
    model = interface.new_model(request.json["name"])
    # use the selected pron dict
    pron_dict = interface.get_pron_dict(request.json['pron_dict_name'])
    # get its dataset
    dataset = interface.get_dataset(pron_dict.dataset.name)
    app.config['CURRENT_DATASET'] = dataset
    app.config['CURRENT_PRON_DICT'] = pron_dict
    model.link(dataset, pron_dict)
    model.build_kaldi_structure()
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
    interface: Interface = app.config['INTERFACE']
    model = interface.get_model(request.json["name"])
    # set the dataset to match the model
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
    interface: Interface = app.config['INTERFACE']
    fake_results = {}
    data = {
        "list": [{
                'name': model['name'],
                'results': fake_results,
                'dataset_name': model['dataset_name'],
                'pron_dict_name': model['pron_dict_name']
                } for model in interface.list_models_verbose()]
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/settings", methods=['POST'])
def settings():
    model = app.config['CURRENT_MODEL']
    if model is None:
        return jsonify({"status": 404,
                        "data": "No current model exists (perhaps create one first)"})
    if request.method == 'POST':
        model.ngram = request.json['ngram']
    data = {
        "settings": {
            "ngram": model.ngram
        }
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/train", methods=['GET'])
def train():
    model: Model = app.config['CURRENT_MODEL']
    if model is None:
        return jsonify({"status": 404,
                        "data": "No current model exists (perhaps create one first)"})
    model.train(on_complete=lambda: print("Training complete!"))
    data = {
        "status": model.status
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/status", methods=['GET'])
def status():
    model: Model = app.config['CURRENT_MODEL']
    if model is None:
        return jsonify({"status": 404,
                        "data": "No current model exists (perhaps create one first)"})
    data = {
        "status": model.status
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/results", methods=['GET'])
def results():
    model: Model = app.config['CURRENT_MODEL']
    if model is None:
        return jsonify({"status":404, "data": "No current model exists (perhaps create one first)"})
    wer_lines = []
    log_file = Path('/elpis/state/tmp_log.txt')
    results = {}
    if log_file.exists():
        with log_file.open() as fin:
            for line in reversed(list(fin)):
                line = line.rstrip()
                if "%WER" in line:
                    # use line to sort by best val
                    line_r = line.replace('%WER ', '')
                    wer_lines.append(line_r)
            wer_lines.sort(reverse = True)
            line = wer_lines[0]
            line_split = line.split(None, 1)
            wer = line_split[0]
            line_results = line_split[1]
            line_results = line_results.replace('[', '')
            line_results = line_results.replace(']', '')
            results_split = line_results.split(',')
            count_val = results_split[0].strip()
            ins_val = results_split[1].replace(' ins', '').strip()
            del_val = results_split[2].replace(' del', '').strip()
            sub_val = results_split[3].replace(' sub', '').strip()
            results = {'wer': wer, 'count_val': count_val, 'ins_val': ins_val, 'del_val': del_val,
                       'sub_val': sub_val}
            print(results)
    else:
        return jsonify({"status": 404,
                        "data": "No log file was found, couldn't parse the results"})
    data = {
        "results": results
    }
    return jsonify({
        "status": 200,
        "data": data
    })
