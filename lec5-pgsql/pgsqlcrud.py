from flask import Flask, jsonify, request, flash, render_template, request, session, abort,redirect
from dataclasses import dataclass 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select,func, desc 

# you must pip install python_dotenv first :: aeam
# Also see: https://pypi.org/project/python-dotenv/#file-format

from dotenv import dotenv_values

app = Flask(__name__)

# get secrets from the .env file 
config=dotenv_values(".env")

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://'+config["PG_USER"]+':'+config["PG_PASS"]+'@localhost:5432/inventory'
db = SQLAlchemy(app)


@dataclass
class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id: int
    name: str
    quantity: int
    price: int

    customer_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/list', methods=['GET'])
def list_customers():

    next_cust_id = 0    # Initialize var, not sure if we even need to?
    
    # Get all the customers so we can display them. Never mind the pagination concerns :)
    customers=Customer.query.all()
    
    # Get the max customer id and add one to it , then pass it to
    # the listing.html so the New Entry field can be pre-populated 
    # db.session.execute(select(func.max(db.customer.c.customer_id)))
    
    # Stupid SQLAlchemy ORM nastiness
    max_cust_id = Customer.query.order_by(desc(Customer.customer_id)).first().customer_id
    print(max_cust_id)
    next_cust_id = max_cust_id + 1
   
    return render_template('listing.html',customer_list=list(customers),next_cust_id=next_cust_id)


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

    # Stupid SQLAlchemy gymnastics
    db.session.add(new_customer)
    db.session.commit()
    db.session.flush()
    
    return redirect("/list")

@app.route('/update-form/<cust_id>', methods=["GET"])
def update_form(cust_id):
    customer = Customer.query.get(cust_id) # Ask Mongo if collection has a document with customer_id we're sending
 
    return render_template("update_form.html",customer=customer)

@app.route('/update', methods=["POST"])
def update_customer():
    form_customer_id = request.form.get('customer_id')
    form_name = request.form.get('name')
    form_price = request.form.get('price')
    form_quantity = request.form.get('quantity')

    # Get customer from the backend by giving the Customer object the customer_id 
    # we got from the form

    customer = Customer.query.get(form_customer_id)

    if not customer:
        # we should never get here because 
        return("Customer ID NOT FOUND!")
    else:
        # No need to set customer_id because the customer object already has that 
        # we'll just update the other fields and persist is through the ORM
        customer.name=form_name
        customer.price=form_price
        customer.quantity=form_quantity

        # persist in postgresql backend.
        db.session.commit()
        db.session.flush()       
        
        return redirect("/list")
        #return(jsonify({"customer":customer.to_json()}))

@app.route('/delete/<cust_id>')
def delete_custid(cust_id):
    customer = Customer.query.get(cust_id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        db.session.flush()

    return redirect('/list')


# @app.route('/delete', methods=["POST"])
# def delete_customer():
#     form_customer_id = request.form.get('customer_id')

#     # Get customer from the backend by giving the Customer object the customer_id 
#     # we got from the form
#     customers = Customer.objects(customer_id=form_customer_id)
#     customer = customers.first() # Returns first item in the QuerySet or None

#     if not customer:
#         return("Customer not found!")
#     else:
#         # No need to set customer_id because the customer object already has that         
#         customer.delete()         # Nuke it with a vengeance!
#         return("Deleted Customer with id: "+form_customer_id)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
