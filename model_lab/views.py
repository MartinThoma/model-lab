# core modules
import glob
import os

# 3rd party modules
from flask import render_template, request

# internal modules
from model_lab.backend import app, MODEL_DIR, load_description, load_model, parse_model_input


@app.route('/')
def index():
    html_list = '<ul>'
    for glob_path in glob.glob(MODEL_DIR + '/*'):
        _, name = os.path.split(glob_path)
        url = 'id/{}'.format(name)
        html_list += ('<li><a href="{url}">{name}</a></li>'
                      .format(url=url, name=name))
    html_list += '</ul>'
    return html_list


@app.route('/id/<string:ml_model>', methods=['GET'])
def model_view(ml_model):
    model = load_model(ml_model)
    description = load_description(ml_model)
    request_dict = parse_model_input(description, request.args.to_dict(flat=True))
    return render_template('model_page.html',
                           ml_model=ml_model,
                           inference=model.infer(request_dict),
                           args=request_dict,
                           description=description)
