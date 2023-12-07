from werkzeug.middleware.profiler import ProfilerMiddleware

from flask import Flask, request, jsonify

import json

app = Flask(__name__)

#app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30], profile_dir='./profile')

def waste_time():
  for i in range(1, 1000000):
    j = i / 10
    k = j * 5
    l = j * 2

@app.route('/fast')
def fast_execution_get():
  return jsonify({'data': 'Fast! Hello Python!!!'})

@app.route('/long')
def long_execution_get():
  waste_time()
  return jsonify({'data': 'Loooong! Hello Python!!!'})

if __name__ == '__main__':
  app.run(debug = True)