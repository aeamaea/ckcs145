from flask import Flask, redirect, render_template, request, session, abort

app = Flask(__name__)

@app.route('/')
def test1():
    return 'Lab3: Accessed endpoint powered by Flask & Python'

@app.route('/param')
def param_home():
    return 'Parameter may submitted to this URL.'

@app.route('/param/<name>')
def param_submit(name):
    return render_template('app.html', name=name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5090')
