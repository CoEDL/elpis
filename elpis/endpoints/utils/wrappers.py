from flask import current_app as app, jsonify
from elpis.engines.common.objects.dataset import Dataset

def require_dataset(f):
    def wrapper(*args, **kwargs):
        dataset: Dataset = app.config['CURRENT_DATASET']
        if dataset is None:
            return jsonify({"status": 404,
                            "data": "No current dataset exists (perhaps create one first)"})
        return f(dataset, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper