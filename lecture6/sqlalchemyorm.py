from flask import Flask, request, request, flash, jsonify
from dataclasses import dataclass 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mikemoloch:tingoo@127.0.0.1:5432/ckcs145'
db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    __tablename__ = 'User'

    email: str
    name: str

    email = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(100))


@app.route('/list')
def list_all():
    print("in list all")
    all_users = User.query.all()
    print(all_users)

    return all_users



if __name__ == '__main__' :
    app.run(debug=True)