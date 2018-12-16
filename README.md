# model_lab

The model_lab helps machine learning developers to make their models accessible
for humans.

During a machine learning project you want that humans can interact with it.
It might be simply yourself, smoke-testing if the model gets some basic inputs
right. Or a stakeholder who is not quite convinced that your model performs as
advertised. Or a colleague whom you want to show what you're working on.


## Installation

Install the model_lab with

```
$ pip install -e git+https://github.com/MartinThoma/model_lab.git
```

## Usage

The following command starts a web server:

```
$ model_lab start model.zip
```

## model.zip

Each zip package consists of a model.py which contains an `infer(input_dict)` function and a `description.json`:

```
{
    "name": "Titanic Survival Model",
    "parameters": [
        {
            "name": "Pclass",
            "label": "Pclass",
            "type": "int",
            "comment": "Passenger Class: 1 (First Class) is the most expensive one, 3 is the cheapest"
        },
        {
            "name": "age",
            "label": "age",
            "type": "float",
            "comment": ""
        },
        {
            "name": "SibSp",
            "label": "SibSp",
            "type": "float",
            "comment": "# of siblings / spouses aboard the Titanic"
        },
        {
            "name": "Parch",
            "label": "Parch",
            "type": "float",
            "comment": "# of parents / children aboard the Titanic"
        },
        {
            "name": "Fare",
            "label": "Fare",
            "type": "float",
            "comment": ""
        }
    ],
    "output": [
        {
            "name": "Survival Probability",
            "comment": "Survival probability in [0, 1], where 0 means the model is certain that the passenger did not survive and 1 means it is certain that the passenger survived."
        }
    ],
    "archetypes": [
        {
            "name": "The mother",
            "parameters": {
                "Pclass": 1,
                "age": 42,
                "SibSp": 12.34,
                "Parch": 3.141,
                "Fare": 2.141
            }
        }
    ],
    "info": {
        "text": "The model was trained on the values of 123 passangers of the titanic where it is known if the did / did not survive.\n\nThe model is an SVM with C = 1.234."
    }
}
```
