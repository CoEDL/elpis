bp = Blueprint("transcriptions", __name__, url_prefix="/transcriptions")
'Is this needed?'
#bp.register_blueprint(comp.bp)

@bp.route("/name")
def name():
    return ''

@bp.route("/date")
def date():
    return ''

@bp.route("/usedModelName")
def usedModelName():
    return ''

@bp.route("/results")
def results():
    return ''

@bp.route("/audio")
def audio():
    return ''