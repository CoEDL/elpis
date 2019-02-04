from ..blueprint import Blueprint
print("# start model (__name__ =",__name__,")")
bp = Blueprint("model", __name__, url_prefix="/model")
print("# created model.bp")
# def route(blueprint, rule):


@bp.route("/new")
def new():
    return '{"status": "new model created"}'
print("# routed model.bp('/new')")