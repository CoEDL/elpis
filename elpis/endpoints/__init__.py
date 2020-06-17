from ..blueprint import Blueprint
from . import config
from . import dataset
from . import model
from . import pron_dict
from . import transcription


bp = Blueprint("endpoints", __name__, url_prefix="/api")

# add blueprint collections to the endpoints blueprint.
bp.register_blueprint(config.bp)
bp.register_blueprint(dataset.bp)
bp.register_blueprint(pron_dict.bp)
bp.register_blueprint(model.bp)
bp.register_blueprint(transcription.bp)


@bp.route("/")
def whole_state():
    # TODO: implement this if needed
    return '{"yet to be named": "the entire model!"}'
