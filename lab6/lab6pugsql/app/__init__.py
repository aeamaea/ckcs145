import logging

from flask import Flask, request, jsonify

import pugsql 
from dotenv import dotenv_values

# get secrets from the .env file  
# IT MUST EXIST IN same directory where this current file is executed from
config=dotenv_values(".env")


queries = pugsql.module('queries/')
queries.connect('postgresql://'+config["PG_USER"]+':'+config["PG_PASS"]+'@localhost:5432/lab6')


"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")

"""
******************
routes
******************
"""
@app.route('/list', methods=['GET'])
def list_all_users():
    # result_set = db.session.query(models.User).all()
    result_set = queries.get_all_users()

    return jsonify(list(result_set))

@app.route('/insert',methods=['POST'])
def insert_user():
    form_name  = request.form.get('user_name')
    form_email = request.form.get('user_email')

    queries.insert_user(name=form_name,email=form_email)

    status_message = 'A row with primary key of ' + form_email + ' inserted into database'

    return jsonify({'status': status_message})

@app.route('/update',methods=['POST'])
def update_user():
    form_name  = request.form.get('user_name')
    form_email = request.form.get('user_email')

    rows_changed = queries.update_one_user(email=form_email,name=form_name)

    status_message = str(rows_changed) + ' rows have been updated'

    return jsonify({'status': status_message})

@app.route('/delete',methods=['POST'])
def delete_user():
    form_email = request.form.get('user_email')

    rows_changed = queries.delete_one_user(email=form_email)

    status_message = f'{rows_changed} rows have been DELETED'
    return jsonify({'status': status_message})

