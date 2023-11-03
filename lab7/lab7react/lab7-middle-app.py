from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

#Enable POST method for route
@app.route('/test_json', methods = ['POST']) 

def test_json():   		  
    #We use RESTer to send a POST request
    # Note: The POST request is a JSON object
    if(request.method == 'POST'):       					 
        #    We know this because we selected the
        #    following in RESTer:
        #    1. Content-type
        #    2. application/json
        
        data = request.get_json() #Returns a dictionary
                
        #Indexing the dictionary returned by request.json():
        data_id = data['Id'] #Thanks to theDonKim!!  
        data_customer = data['Customer']
        data_quantity = data['Quantity']
        data_price = data['Price']
        
        #Print parsed values into Terminal
        print('Id: ', data_id)
        print('Customer: ', data_customer)
        print('Quantity: ', data_quantity)
        print('Price: ', data_price)
    return jsonify({'data': 'success'})
   	 
@app.route('/test', methods = ['GET','POST']) #Enable GET and POST
def test():   	 # We use this route for the webform
    if(request.method == 'POST'):
        content_type = request.headers.get('Content-Type') 
        #Check the Content-Type from Header
        print(content_type) 

        data_id = request.form.get('ID')
        data_customer = request.form.get('Customer')
        data_quantity  = request.form.get('Quantity')
        data_price = request.form.get('Price')
        print('Id: ', data_id)
        print('Customer: ', data_customer)
        print('Quantity: ', data_quantity)
        print('Price: ', data_price)
    return render_template('test.html') 
    #Render test.html from templates directory
    
@app.route('/insert', methods = ['POST']) #Enable GET and POST
def insert_test():

    data = request.get_json() #Returns a dictionary
    print(data)
        
    request_name = data_customer = data['name']
    print('name = ', request_name)
    request_email = data_customer = data['email']
    print('email = ', request_email)
        
    return jsonify({'data': 'success'})

if __name__ == '__main__':
    app.run(debug=True)