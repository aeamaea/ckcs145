from flask import Flask

app = Flask(__name__)

@app.route('/')
def test1():
    return 'Accessed endpoint at /'

@app.route('/param')
def param_home():
    return 'A parameter may be submitted to this endpoint URL thingy'


@app.route('/param/<name>')
def name_handler(name):
    return f"Parameter {name=}" 

if __name__ == '__main__':
    app.run()

