#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Model for the Titanic survival."""

# core modules
import os

# 3rd party modules.
import pickle
import pandas as pd

model = None


def initialize(description_dict):
    """Initialize the model."""
    global model
    path = os.path.join(os.path.dirname(__file__), 'scripts/model.pickle')
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


def infer(input_dict):
    """
    Infer the likelyness of survival.

    Parameters
    ----------
    input_dict : Dict[str, Any]

    Returns
    -------
    prediction : float
    """
    expected_keys = set(['Age', 'Name', 'Sex', 'Ticket'])
    missing_keys = expected_keys - set(input_dict.keys())
    if len(missing_keys) > 0:
        return str(missing_keys)
    input_dict['Cabin'] = None
    input_dict = {x: [y] for x, y in input_dict.items() }
    df = pd.DataFrame(input_dict, index=[0])
    print('!' * 80)
    print(df)
    train = load_module('scripts/train.py')
    df = df.apply(train.preprocess, axis=1)
    return model.predict(df)[0]


def load_module(relative_path):
    """
    Load the 'model.py' of model_id.

    Parameters
    ----------
    relative_path : str

    Returns
    -------
    module
    """
    import importlib.util
    filepath = os.path.join(os.path.dirname(__file__), relative_path)
    spec = importlib.util.spec_from_file_location("model", filepath)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo
