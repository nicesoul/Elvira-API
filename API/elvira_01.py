# welcome, my friend :) ...

# this is test, temporary version

import os
import sys
import time
# import shutil

from flask import Flask, request, jsonify
from flask.templating import render_template

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


app = Flask(__name__)


df = pd.read_csv('data/Brussels-price-predictions.csv')

@app.route('/predict', methods=['POST'])
def prediction_post_return():
    params = request.json
    if params == None:
        return jsonify("You didn't provide any JSON data. Please, check if the submitted form is not empty")
    else: return jsonify(params)

@app.route('/predict', methods=['GET'])
def prediction_get_return():
    args = request.args
    if args == None:
        return jsonify("You didn't provide any JSON data. Please, check if the submitted form is not empty")
    else: return jsonify(args)


@app.route('/', methods=['GET'])
def response_root():
    return jsonify('alive')

@app.route('/*', methods=['GET'])
def response_star():
    return jsonify('welcome, my friend :)')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(405)
def page_not_found(e):
    return jsonify('The method is not allowed for the requested URL (405). It means that you are probably doing a POST request to the endpoint, which receives only GET requests or vice versa')

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception:
        port = int(os.environ.get('PORT', 443))

    app.run(host="0.0.0.0", port=port)
