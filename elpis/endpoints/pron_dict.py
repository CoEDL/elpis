from flask import request
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.pron_dict import PronDict


bp = Blueprint("pron_dict", __name__, url_prefix="/pron_dict")


@bp.route("/new", methods=['GET', 'POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    pd = kaldi.new_pron_dict(request.json['name'])
    app.config['CURRENT_PRON_DICT'] = pd
    return jsonify({
        "status": "ok",
        "data": pd.config._load()
    })


@bp.route("/load", methods=['GET', 'POST'])
def load():
    kaldi: KaldiInterface = app.config['INTERFACE']
    pd = kaldi.get_pron_dict(request.json['name'])
    app.config['CURRENT_PRON_DICT'] = pd
    return jsonify({
        "status": "ok",
        "data": pd.config._load()
    })


@bp.route("/name", methods=['GET', 'POST'])
def name():
    pd: PronDict = app.config['CURRENT_PRON_DICT']
    if pd is None:
        return '{"status":"error", "data": "No current pron dict exists (prehaps create one first)"}'
    if request.method == 'POST':
        pd.name = request.json['name']
    return jsonify({
        "status": "ok",
        "data": pd.name})


@bp.route("/list", methods=['GET', 'POST'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    return jsonify({
        "status": "ok",
        "data": kaldi.list_pron_dicts()
    })


@bp.route("/l2s", methods=['POST'])
def l2s():
    pd: PronDict = app.config['CURRENT_PRON_DICT']
    # handle incoming data
    if request.method == 'POST':
        file = request.files['file']
        if pd is None:
            # TODO some of the end points (like this one) return files, but on error we still return a json string? Looks like bad practice to me
            return '{"status":"error", "data": "No current pron dict exists (prehaps create one first)"}'
        pd.set_l2s_fp(file)
    return pd.l2s


@bp.route("/lexicon", methods=['GET', 'POST'])
def generate_lexicon():
    pd: PronDict = app.config['CURRENT_PRON_DICT']
    pd.generate_lexicon()
    return pd.lexicon
