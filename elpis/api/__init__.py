from ..blueprint import Blueprint
from . import databundle
from . import model
from . import transcription

bp = Blueprint("api", __name__, url_prefix="/api")
bp.register_blueprint(databundle.bp)
bp.register_blueprint(model.bp)
bp.register_blueprint(transcription.bp)

@bp.route("/")
def whole_state():
    # TODO: implement this if needed
    return '{"yet to be named": "the enture model!"}'
