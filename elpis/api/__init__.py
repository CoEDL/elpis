from ..blueprint import Blueprint
from . import databundle
from . import model
from . import transcription

from pathlib import Path

bp = Blueprint("api", __name__, url_prefix="/api")

# add blueprint collections to the api blueprint.
bp.register_blueprint(databundle.bp)
bp.register_blueprint(model.bp)
bp.register_blueprint(transcription.bp)

@bp.route("/")
def whole_state():
    # TODO: implement this if needed
    return '{"yet to be named": "the enture model!"}'

@bp.route("/log.txt")
def log():
    log_file = Path('/elpis/state/tmp_log.txt')
    if log_file.exists():
        with log_file.open() as fin:
            return fin.read()
    else:
        return "No log file."
