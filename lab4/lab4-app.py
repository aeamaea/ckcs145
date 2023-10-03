from flask import Flask, jsonify, request

app = Flask(__name__)
my_debug = True

@app.route ('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        data = "hello world"
        return jsonify({'data': data})
    
    if request.method == 'POST':
        data = request.get_json()
        return data # don't "jsonify" cuz it's already json
    
@app.route('/home/<int:num>', methods=['GET'])
def disp(num):
    #return jsonify({'data':num**2})
    return 

@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        print(request.form.keys())
        print(request.form.get('Id'))
        data_id = request.form.get('Id')
        data_customer = request.form.get('Customer')
        data_quantity = request.form.get('Quantity')
        data_price = request.form.get('Price')
        if my_debug == True:
            print('Id: ', data_id)
            print('Customer', data_customer)
            print('Quantity', data_quantity)
            print('Price', data_price)
        
        return jsonify({'data': 'success'})
    
if __name__ == "__main__":
    app.run(debug=True)
