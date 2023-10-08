import logging
from flask import Flask, request, jsonify
from flask_appbuilder.security.mongoengine.manager import SecurityManager
from flask_appbuilder import AppBuilder
from flask_mongoengine import MongoEngine

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)
appbuilder = AppBuilder(app, security_manager_class=SecurityManager)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    

from app import views, models

@app.route('/listusers', methods=['GET'])
def list_all_users() :
    data = list(models.User.objects)
    return data 

@app.route('/adduser', methods=['POST'])
def create_user():
    name = request.form.get('user_name')
    email = request.form.get('user_email')

    new_user = models.User(name=name, email=email)
    new_user.save()

    return new_user.to_json()

@app.route('/find', methods=['POST'])
def find_user():
    query_name = request.form.get('user_name')

    users = models.User.objects(name=query_name)

    user = users.first()

    if not user :
        return jsonify({'error': 'data not found'})
    else:
        return user.to_json()

@app.route('/delete_user', methods=['POST'])
def delete_user():
    #get data from HTML form
    name = request.form.get('user_name')

    #find all names that match name
    users = models.User.objects(name=name)

    #get the first name from list of matching names 
    # sent back from mongodb
    user = users.first()

    if not user:
        return jsonify({'error': 'user not found!'})
    else:
        user.delete()

    status_message = user.name + ' has been deleted'
    return jsonify({'status': status_message})