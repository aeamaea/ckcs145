from flask import Flask, jsonify, request, render_template, request, session, abort,redirect

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

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/data_entry')
def data_entry():
    return render_template('data_entry.html')

@app.route('/create', methods=['GET','POST'])
def create_customer():
    customer_id = request.form.get('customer_id')
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')

    new_customer = Customer(customer_id=customer_id,name=name,price=price,quantity=quantity)
    new_customer.save()

    return redirect("/list")

@app.route('/update-form/<cust_id>', methods=["GET"])
def update_for(cust_id):
    customers = Customer.objects(customer_id=cust_id) # Ask Mongo if collection has a document with customer_id we're sending
    customer = customers.first() # This gives the first item in the QuerySet or None if nothing came back from Mongodb

    return render_template("update_form.html",customer=customer)

@app.route('/update', methods=["POST"])
def update_customer():
    form_customer_id = request.form.get('customer_id')
    form_name = request.form.get('name')
    form_price = request.form.get('price')
    form_quantity = request.form.get('quantity')

    # Get customer from the backend by giving the Customer object the customer_id 
    # we got from the form
    customers = Customer.objects(customer_id=form_customer_id)
    customer = customers.first() # This gives the first item in the QuerySet or None

    # print(form_customer_id,form_name,form_price,form_quantity)
    # print(customer.to_json())


    if not customer:
        return("Customer ID NOT FOUND!")
    else:
        # No need to set customer_id because the customer object already has that 
        # we'll just update the other fields and hit save()
        customer.name=form_name
        customer.price=form_price
        customer.quantity=form_quantity
        customer.save()         # this basically saves it in the mongo back end.
        
        return redirect("/list")
        #return(jsonify({"customer":customer.to_json()}))

@app.route('/delete/<cust_id>')
def delete_custid(cust_id):
    customers = Customer.objects(customer_id=cust_id)
    customer = customers.first()

    if customer:
        customer.delete()

    return redirect('/list')


@app.route('/delete', methods=["POST"])
def delete_customer():
    form_customer_id = request.form.get('customer_id')

    # Get customer from the backend by giving the Customer object the customer_id 
    # we got from the form
    customers = Customer.objects(customer_id=form_customer_id)
    customer = customers.first() # Returns first item in the QuerySet or None

    if not customer:
        return("Customer not found!")
    else:
        # No need to set customer_id because the customer object already has that         
        customer.delete()         # Nuke it with a vengeance!
        return("Deleted Customer with id: "+form_customer_id)


@app.route('/list', methods=['GET'])
def list_customers():

    next_cust_id = 0    # Initialize var, not sure if we even need to?
    
    # Get all the customers so we can display them. Never mind the pagination concerns :)
    customers=Customer.objects

    # Get the max customer id and add one to it , then pass it to
    # the listing.html so the New Entry field can be pre-populated 
    # in case the user wants to enter a new row. :: aeam
    # see https://stackoverflow.com/a/25059302 (how to get max of a column value)
    max_cust_id = customers.order_by("-customer_id").limit(-1).first().customer_id
    next_cust_id = max_cust_id + 1
    return render_template('listing.html',customer_list=list(customers),next_cust_id=next_cust_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
