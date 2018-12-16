# core modules
import os
import json

# 3rd party modules
from flask import Flask

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(BASE_PATH, "ml_models")
TEMPLATE_DIR = os.path.join(BASE_PATH, "templates")
STATIC_DIR = os.path.join(BASE_PATH, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


def load_description(model_id):
    filepath = os.path.join(MODEL_DIR, model_id, 'description.json')
    with open(filepath) as data_file:
        description = json.load(data_file)
    return description


def load_model(model_id):
    """
    Load the 'model.py' of model_id.

    Parameters
    ----------
    model_id : str

    Returns
    -------
    module
    """
    import importlib.util
    filepath = os.path.join(MODEL_DIR, model_id, 'model.py')
    spec = importlib.util.spec_from_file_location("model", filepath)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    description_dict = load_description(model_id)
    foo.initialize(description_dict)
    return foo


def parse_model_input(description, request_dict):
    parameters = description['parameters']
    parameters = dict([(param['name'], param) for param in parameters])
    request_dict_edited = {}
    for name, value in request_dict.items():
        request_dict_edited[name] = value
        if name in parameters:
            param = parameters[name]
            if param['type'] == 'int':
                request_dict_edited[name] = int(value)
            elif param['type'] == 'float':
                request_dict_edited[name] = float(value)
            elif param['type'] in ['str', 'categorical']:
                request_dict_edited[name] = str(value)
            else:
                raise NotImplementedError(param['type'])
    return request_dict_edited
