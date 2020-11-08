from flask import current_app as app, jsonify
from flask import request, make_response
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.pron_dict import PronDict

def require_dataset(f):
    def wrapper(*args, **kwargs):
        dataset: Dataset = app.config['CURRENT_DATASET']
        if dataset is None:
            return jsonify({"status": 404,
                            "data": "No current dataset exists (perhaps create one first)"})
        return f(dataset, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def require_pron_dict(f):
    def wrapper(*args, **kwargs):
        pron_dict: PronDict = app.config['CURRENT_PRON_DICT']
        if pron_dict is None:
            return jsonify({"status": 404,
                            "data": "No current pron dict exists (perhaps create one first)"})
        return f(pron_dict, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def file_param(f):
    # Can I make this wrapper require the dataset? hmmmm
    def wrapper(dataset: Dataset, *args, **kwargs):
        file_name = request.args.get("file")
        if file_name is not None:
            # File specified
            # We need to bork this, because filenames are stored with eaf extensions
            if (file_name + ".eaf") not in dataset.config['files']:
                return jsonify({"status": 404,
                                "data": "File not found."})
            else:
                return f(dataset, *args, file_name=file_name, **kwargs)
        else:
            return f(dataset, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper