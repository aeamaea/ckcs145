from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)

@app.route('/')
def test1():
   return 'Accessed endpoint powered by Plask and Python'

@app.route('/param')
def param_home():
    return 'Parameter may be submitted to this url.'

@app.route('/param/<simon>')
def param_submit(simon):
    # return 'Parameter %s!' % name
    return render_template('test.html', name=simon)

def 
if __name__ == '__main__':
   app.run(host='0.0.0.0', port='5090')
