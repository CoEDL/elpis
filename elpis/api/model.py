from ..blueprint import Blueprint
from .comp import bp as comp_bp
print("# start model (__name__ =",__name__,")")
bp = Blueprint("model", __name__, url_prefix="/model")
print("# created model.bp")
# def route(blueprint, rule):

bp.register_blueprint(comp_bp)


@bp.route("/new")
def new():
    return '{"status": "new model created"}'
print("# routed model.bp('/new')")