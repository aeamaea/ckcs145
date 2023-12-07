from flask import Flask, request, jsonify

import json

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'data': 'Hello Python!!!'})

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
    app.run(debug=True)