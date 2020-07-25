from flask import request, make_response
from ..blueprint import Blueprint
from flask import current_app as app, jsonify
from elpis.engines import Interface
from elpis.engines.common.objects.pron_dict import PronDict
from elpis.engines.kaldi.errors import KaldiError


bp = Blueprint("pron_dict", __name__, url_prefix="/pron-dict")


@bp.route("/new", methods=['POST'])
def new():
    interface: Interface = app.config['INTERFACE']
    try:
        pron_dict = interface.new_pron_dict(request.json['name'])
    except KaldiError as e:
        return jsonify({
            "status": 500,
            "error": e.human_message
        })
    print(f"****{request.json['name']}****")
    dataset = interface.get_dataset(request.json['dataset_name'])
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
    interface: Interface = app.config['INTERFACE']
    pron_dict = interface.get_pron_dict(request.json['name'])
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
    interface: Interface = app.config['INTERFACE']
    data = {
        "list": interface.list_pron_dicts_verbose()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/l2s", methods=['POST'])
def l2s():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    if pron_dict is None:
        return jsonify({"status": 404,
                        "data": "No current pron dict exists (perhaps create one first)"})
    if request.method == 'POST':
        file = request.files['file']
        pron_dict.set_l2s_fp(file)
    data = {
        "l2s": pron_dict.get_l2s_content()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/generate-lexicon", methods=['GET'])
def generate_lexicon():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    if pron_dict is None:
        return jsonify({"status": 404,
                        "data": "No current pron dict exists (perhaps create one first)"})
    pron_dict.generate_lexicon()
    data = {
        "lexicon": pron_dict.get_lexicon_content()
    }
    return jsonify({
        "status": 200,
        "data": data
    })


@bp.route("/save-lexicon", methods=['POST'])
def save_lexicon():
    pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
    if pron_dict is None:
        return jsonify({"status": 404,
                        "data": "No current pron dict exists (perhaps create one first)"})
    if request.method == 'POST':
        lexicon = request.json['lexicon']
    else:
        return make_response(405, "GET not allowed")
    pron_dict.save_lexicon(lexicon)
    data = {
        "lexicon": pron_dict.get_lexicon_content()
    }
    return jsonify({
        "status": 200,
        "data": data
    })
