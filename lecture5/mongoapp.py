from flask import Flask, jsonify, request, render_template, request, session, abort

from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS']= {'db':'Inventory', 'host':'localhost', 'port':27017}
db = MongoEngine()
db.init_app(app)


class Customer(db.Document):
    customer_id = db.IntField()
    name = db.StringField()
    quantity = db.IntField()
    price = db.IntField()

    meta = {'collection' : 'Customer', 'allow_inheritance' : False}

@app.route('/list', methods=['GET'])
def list_customers():
    #print(db) # print out what db we're in

    # for customer in Customer.objects :
    #     print("\n-------\ncustomer: ", customer.name,"\ncustomer price : ",customer.price)
    
    # return "Success!"
    return render_template('listing.html', customer_objects=list(Customer.objects))
    #return list(Customer.objects)


if __name__ == "__main__":
    app.run(debug=True)
