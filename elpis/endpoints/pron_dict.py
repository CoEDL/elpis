from flask import request
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.pron_dict import PronDict
from elpis.wrappers.objects.dataset import Dataset


bp = Blueprint("pron_dict", __name__, url_prefix="/pron-dict")


@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    pron_dict = kaldi.new_pron_dict(request.json['name'])
    dataset: Dataset = app.config['CURRENT_DATABUNDLE']
    pron_dict.link(dataset)
    app.config['CURRENT_PRON_DICT'] = pron_dict
    data = {
        "config": pron_dict.config._load()
    }
    return jsonify({
        "status": "ok",
        "data": data
    })


@bp.route("/load", methods=['GET', 'POST'])
def load():
    kaldi: KaldiInterface = app.config['INTERFACE']
    pron_dict = kaldi.get_pron_dict(request.json['name'])
    app.config['CURRENT_DATABUNDLE'] = pron_dict.dataset
    app.config['CURRENT_PRON_DICT'] = pron_dict
    data = {
        "config": pron_dict.config._load(),
        "l2s": pron_dict.get_l2s_content()
    }
    return jsonify({
        "status": "ok",
        "data": data
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    if pron_dict is None:
        return '{"status":"error", "data": "No current pron dict exists (prehaps create one first)"}'
    if request.method == 'POST':
        pron_dict.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": pron_dict.name
    })


@bp.route("/list", methods=['GET', 'POST'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    return jsonify({
        "status": "ok",
        "data": kaldi.list_pron_dicts()
    })


@bp.route("/l2s", methods=['POST'])
def l2s():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    # handle incoming data
    if request.method == 'POST':
        file = request.files['file']
        if pron_dict is None:
            # TODO some of the end points (like this one) return files, but on error we still return a json string? Looks like bad practice to me
            return '{"status":"error", "data": "No current pron dict exists (prehaps create one first)"}'
        pron_dict.set_l2s_fp(file)
    return pron_dict.l2s


@bp.route("/lexicon", methods=['GET', 'POST'])
def generate_lexicon():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    pron_dict.generate_lexicon()
    return pron_dict.lexicon
