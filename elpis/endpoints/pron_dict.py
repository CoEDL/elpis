from flask import request
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.wrappers.objects.interface import KaldiInterface
from elpis.wrappers.objects.pron_dict import PronDict
from elpis.wrappers.objects.dataset import Dataset


bp = Blueprint("pron_dict", __name__, url_prefix="/pron-dict")


@bp.route("/new", methods=['POST'])
def new():
    kaldi: KaldiInterface = app.config['INTERFACE']
    pron_dict = kaldi.new_pron_dict(request.json['name'])
    dataset = kaldi.get_dataset(request.json['dataset_name'])
    pron_dict.link(dataset)
    app.config['CURRENT_PRON_DICT'] = pron_dict
    data = {
        "config": pron_dict.config._load()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/load", methods=['POST'])
def load():
    kaldi: KaldiInterface = app.config['INTERFACE']
    pron_dict = kaldi.get_pron_dict(request.json['name'])
    app.config['CURRENT_PRON_DICT'] = pron_dict
    app.config['CURRENT_DATASET'] = pron_dict.dataset
    data = {
        "config": pron_dict.config._load(),
        "l2s": pron_dict.get_l2s_content(),
        "lexicon": pron_dict.get_lexicon_content()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/list", methods=['GET'])
def list_existing():
    kaldi: KaldiInterface = app.config['INTERFACE']
    data = {
        "list": kaldi.list_pron_dicts_verbose()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/l2s", methods=['POST'])
def l2s():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    if request.method == 'POST':
        file = request.files['file']
        if pron_dict is None:
            return '{"status":"error", "data": "No current pron dict exists (perhaps create one first)"}'
        pron_dict.set_l2s_fp(file)
    # TODO fix this to return json wrapper
    return pron_dict.l2s


@bp.route("/generate-lexicon", methods=['GET'])
def generate_lexicon():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    pron_dict.generate_lexicon()
    # TODO fix this to return json wrapper
    return pron_dict.get_lexicon_content()


@bp.route("/save-lexicon", methods=['POST'])
def save_lexicon():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    if request.method == 'POST':
        lexicon = request.json['lexicon']
    pron_dict.save_lexicon(lexicon)
    # data = {
    #     "config": pron_dict.config._load(),
    #     "l2s": pron_dict.get_l2s_content(),
    #     "lexicon": repr(pron_dict.get_lexicon_content())
    # }
    # TODO fix this to return the json wrapper
    return lexicon
