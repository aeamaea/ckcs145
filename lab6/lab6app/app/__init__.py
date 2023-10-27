import logging

from flask import Flask, request, jsonify
from flask_appbuilder import AppBuilder, SQLA





"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


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

@app.route('/list', methods=['GET'])
def list_all_users():
    result_set = db.session.query(models.User).all()
    return jsonify(result_set)

@app.route('/insert',methods=['POST'])
def insert_user():
    form_name  = request.form.get('user_name')
    form_email = request.form.get('user_email')

    user_obj = models.User(email=form_email,name=form_name)
    db.session.add(user_obj)
    
    db.session.flush()
    db.session.commit()

    status_message = 'A row with primary key of ' + form_email + ' inserted into database'

    return jsonify({'status': status_message})

@app.route('/update',methods=['POST'])
def update_user():
    form_name  = request.form.get('user_name')
    form_email = request.form.get('user_email')

    query = db.session.query(models.User)
    query = query.filter(models.User.email==form_email)
    rows_changed = query.update({models.User.name: form_name})

    print('rows_changed: ', rows_changed)
    print('query : ', query)
    
    db.session.flush()
    db.session.commit()

    status_message = str(rows_changed) + ' rows have been updated'

    return jsonify({'status': status_message})

@app.route('/delete',methods=['POST'])
def delete_user():
    form_email = request.form.get('user_email')
    query = db.session.query(models.User)
    query = query.filter(models.User.email==form_email)
    rows_changed = query.delete(synchronize_session=False)

    print('rows_changed: ',rows_changed)
    print('query : ',query)

    db.session.flush()
    db.session.commit()

    status_message = f'{rows_changed} rows have been DELETED'
    return jsonify({'status': status_message})

from app import views, models
