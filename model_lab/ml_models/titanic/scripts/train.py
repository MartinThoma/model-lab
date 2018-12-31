"""Train a model for Titanic."""

import re
import math
import pickle

# 3rd party modules
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor


def main():
    """Load, train, serialize, test."""
    data = load_data()
    analyze_features(data['full_features'])
    model = train(data)

    with open('model.pickle', 'wb') as f:
        pickle.dump(model, f)
    evaluate(model, data)


def load_data():
    """Load the titanic dataset."""
    train = pd.read_csv("../input/train.csv", dtype={"Age": np.float64}, )
    test = pd.read_csv("../input/test.csv", dtype={"Age": np.float64}, )

    train = train.set_index('PassengerId')
    test = test.set_index('PassengerId')

    train = train.apply(preprocess, axis=1)
    test = test.apply(preprocess, axis=1)

    x_train = train.drop(['Survived'], axis=1)
    y_train = train['Survived']
    x_test = test
    return {'train': {'x': x_train, 'y': y_train},
            'test': {'x': x_test},
            'full_features': pd.concat([x_train, x_test])}


def preprocess(item):
    """Preprocess the dictionary 'item'."""
    item = feature_engineering(item)
    item = encode_features(item)
    return item


def feature_engineering(item):
    """
    Develop new features.

    Parameters
    ----------
    item : Dict[str, Any]

    Returns
    -------
    item : Dict[str, Any]
    """
    if item["Cabin"] is None:
        item["Cabin"] = " "
    if item["Age"] is None or math.isnan(item["Age"]):
        item["Age"] = 18  # ????
    if item["Fare"] is None or math.isnan(item["Fare"]):
        item["Fare"] = -1  # ????

    def get_title(x):
        return re.search(' ([A-Za-z]+)\.', x).group(1)
    item["Title"] = get_title(item["Name"])
    return item


def encode_features(item):
    """
    Encode features for machine learning models.

    This step has no value for humans, in contrast to the feature_engineering
    step.
    """
    item['is_male'] = int(item['Sex'] == 'male')
    del item['Name']
    del item['Sex']
    # del item['Fare']
    del item['Cabin']
    del item['Ticket']

    # One-hot encoding: Embarked
    item['embarked_s'] = int(item['Embarked'] == 'S')
    item['embarked_c'] = int(item['Embarked'] == 'C')
    item['embarked_q'] = int(item['Embarked'] == 'Q')
    del item['Embarked']

    # One-hot encoding: Title
    item['title_mr'] = int(item['Title'] == 'Mr')
    item['title_miss'] = int(item['Title'] == 'Miss')
    item['title_mrs'] = int(item['Title'] == 'Mrs')
    item['title_master'] = int(item['Title'] == 'Master')
    item['title_other'] = 1 - (item['title_mr'] +
                               item['title_miss'] +
                               item['title_mrs'] +
                               item['title_master'])
    del item['Title']
    return item


def analyze_features(df_features):
    for column in df_features.columns:
        print('## ' + column)
        value_counts = df_features[column].value_counts()
        if len(value_counts) > 10:
            print('Many values')
        else:
            print(value_counts)
        count_nan = len(df_features[column]) - df_features[column].count()
        if count_nan > 0:
            print('has nan')
        print('')


def train(data):
    etr = ExtraTreesRegressor(n_estimators=10)
    etr.fit(data['train']['x'], np.ravel(data['train']['y']))
    return etr


def evaluate(model, data):
    score = model.score(data['train']['x'], data['train']['y'])
    print("Accuracy: %0.3f".format(score * 100))
    predictions = model.predict(data['test']['x'])
    passenger_id = np.array(data['test']['x'].index).astype(int)
    my_prediction = pd.DataFrame(predictions,
                                 passenger_id,
                                 columns=["Survived"])
    my_prediction.to_csv("my_prediction.csv", index_label=["PassengerId"])

if __name__ == '__main__':
    main()
