from ..blueprint import Blueprint
from . import comp

bp = Blueprint("model", __name__, url_prefix="/model")
bp.register_blueprint(comp.bp)


@bp.route("/new")
def new():
    return '{"status": "new model created"}'
    