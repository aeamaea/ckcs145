from flask import Flask

app = Flask(__name__)

@app.route('/test1')
def test1() :
    return "Accessed endpoint test1:  powered by Flask!!!"


@app.route('/test2')
def test1() :
    return "Accessed endpoint test2:  powered by Flask!!!"

if __name__ == '__main__'
    app.run()
