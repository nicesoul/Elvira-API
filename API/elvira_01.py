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
import joblib


app = Flask(__name__)

def transform_categorical_feature(
    df: pd.DataFrame, column_name: str, column_prefix: str = ""
) -> pd.DataFrame:
    """
    creates columns of binary values from categorical textual information
    """

    df1 = pd.get_dummies(df[column_name].astype(str))
    if column_prefix != "":
        df1.columns = ["is_type_" + col for col in df1.columns]

    new_df = pd.concat([df, df1], axis=1)

    # we don't need transformed column anymore
    new_df = new_df.drop(columns=[column_name])

    return new_df

# please, run a script from API subfolder 
df = pd.read_csv('data/Brussels-price-predictions.csv')
df = df.drop(["predicted_price"], axis=1)
ndf = transform_categorical_feature(df, "subtype", "is_subtype_")
ndf = transform_categorical_feature(
        ndf, "building_condition", "is_building_condition_"
    )
ndf = transform_categorical_feature(ndf, "location", "zipcode_")

model = joblib.load('model/random_forest_BXL.joblib')
y = ndf.price.to_numpy().reshape(-1,1)
ndf = ndf.drop(["price"], axis=1)
x = ndf.to_numpy()
print(model.score(x,y))
print(x[0])
print('shape of x', x.shape)
print(y[0])
print('shape of y', y.shape)
print(ndf.iloc[0])

@app.route('/predict', methods=['POST'])
def prediction_post_return():
    params = request.json
    if params == None:
        return jsonify("You didn't provide any JSON data. Please, check if the submitted form is not empty")
    else: return jsonify(params)

# just for checking API responses 
"""
@app.route('/predict', methods=['GET'])
def prediction_get_return():
    args = request.args
    if args == {}:
        return jsonify("You didn't provide any JSON data. Please, check if the submitted form is not empty")
    else: return jsonify(args)


@app.route('/', methods=['GET'])
def response_root():
    return jsonify('alive')
"""
# END of checking part

# secret route
@app.route('/*', methods=['GET'])
def response_star():
    return jsonify('welcome, my friend :)')

# ERRORs handling part
@app.errorhandler(400)
def page_not_found(e):
    return jsonify('Bad request (400). It seems that your JSON is broken, did you forget to put a quotation mark or a comma somewhere? Maybe :)')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
    return jsonify('Page not found (404). Click here to return to the main page or go to Elvira Github repo for documentation.')

@app.errorhandler(405)
def page_not_found(e):
    return jsonify('The method is not allowed for the requested URL (405). It means that you are probably doing a POST request to the endpoint, which receives only GET requests or vice versa')

@app.errorhandler(500)
def page_not_found(e):
    return jsonify('Internal server error (500). Usually it means that you have found a bug. So, please, report to me how to reproduce it so I could fix the bug ASAP. Email to nicesoul.beyourself@gmail.com or check my other contacts here https://nicesoul.me/contact ')

# main entry part
if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception:
        port = int(os.environ.get('PORT', 80))

    app.run(host="0.0.0.0", port=port)
