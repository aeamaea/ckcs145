from flask import Flask, request, render_template, jsonify

import flask_monitoringdashboard as dashboard

import json


app = Flask(__name__)

dashboard.bind(app)


def waste_time():
  for i in range(1, 1000000):
    j = i / 10
    k = j * 5
    l = j * 2

@app.route('/fast')
def fast_execution_get():
  #return jsonify({'data': 'Hello Python!!!'})
  #return 'worked'
  return render_template("index.html")

@app.route('/long')
def long_execution_get():
  waste_time()
  #return jsonify({'data': 'Hello Python!!!'})
  return render_template("index.html")

@app.route('/post/test', methods=['POST'])
def receive_post():
  headers = request.headers
  
  data_string = request.get_data()
  data = json.loads(data_string)

  request_id = data.get('request_id')
  payload = data.get('payload')

  if request_id and payload:
    return 'Ok', 200
  else:
    return 'Bad Request', 400


if __name__ == '__main__':
  app.run(debug = True)