from flask import request, current_app as app, jsonify
from ..blueprint import Blueprint
import subprocess
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.model import Model
from elpis.wrappers.objects.dataset import Dataset
from elpis.wrappers.objects.pron_dict import PronDict

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


@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    model = kaldi.new_model(request.json["name"])
    print(app.config['CURRENT_DATASET'])
    print(app.config['CURRENT_PRON_DICT'])
    dataset: Dataset = app.config['CURRENT_DATASET']
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    model.link(dataset, pron_dict)
    model.build_kaldi_structure()
    app.config['CURRENT_MODEL'] = model
    data = {"config": model.config._load()}
    return jsonify({
        "status": "ok",
        "data": data
    })


@bp.route("/load", methods=['GET', 'POST'])
def load():
    kaldi: KaldiInterface = app.config['INTERFACE']
    model = kaldi.get_model(request.json["name"])
    # set the dataset to match the model
    app.config['CURRENT_DATASET'] = model.dataset
    app.config['CURRENT_PRON_DICT'] = model.pron_dict
    app.config['CURRENT_MODEL'] = model
    data = {
        "config": model.config._load()
    }
    return jsonify({
        "status": "ok",
        "data": data
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    model = app.config['CURRENT_MODEL']
    if model is None:
        # TODO sending a string error back in incorrect, jsonify it.
        return '{"status":"error", "data": "No current model exists (perhaps create one first)"}'
    if request.method == 'POST':
        model.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": model.name
    })


@bp.route("/settings", methods=['GET', 'POST'])
def settings():
    model = app.config['CURRENT_MODEL']
    if model is None:
        # TODO sending a string error back in incorrect, jsonify it.
        return '{"status":"error", "data": "No current model exists (perhaps create one first)"}'
    if request.method == 'POST':
        model.ngram = request.json['ngram']
        # TODO make this an optional parameter
    return jsonify({
        "status": "ok",
        "data": {
            "ngram": model.ngram
        }
    })



@bp.route("/list", methods=['GET', 'POST'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    # TODO see the two todos below
    fake_results = {}
    data = [{
        'name': model['name'],
        'results': fake_results,
        'dataset_name': model['dataset_name'],
        'pron_dict_name': model['pron_dict_name']
        } for model in kaldi.list_models_verbose()]
    return jsonify({
        "status": "ok",
        "data": data
    })

    # TODO make this endpoint list-verbose or something like that
    # TODO /names could list just the name and /list can be the descriptive verison


@bp.route("/status", methods=['GET', 'POST'])
def status():
    model: Model = app.config['CURRENT_MODEL']
    return jsonify({
        "status": "ok",
        "data": model.status
    })


@bp.route("/train", methods=['GET', 'POST'])
def train():
    model: Model = app.config['CURRENT_MODEL']
    model.train(on_complete=lambda: print("Training complete!"))
    return jsonify({
        "status": "ok",
        "data": model.status
    })


@bp.route("/results", methods=['GET', 'POST'])
def results():
    model: Model = app.config['CURRENT_MODEL']

    wer_lines = []
    log_file = Path('/elpis/state/tmp_log.txt')
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
            line_results = line_results.replace('[','')
            line_results = line_results.replace(']','')
            results_split = line_results.split(',')
            count_val = results_split[0].strip()
            ins_val = results_split[1].replace(' ins','').strip()
            del_val = results_split[2].replace(' del','').strip()
            sub_val = results_split[3].replace(' sub','').strip()
            results = {'wer':wer, 'count_val':count_val, 'ins_val':ins_val, 'del_val':del_val, 'sub_val':sub_val}
            print(results)
    return jsonify({
        "status": "ok",
        "data": results
    })
