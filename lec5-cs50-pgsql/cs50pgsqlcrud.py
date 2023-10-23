from flask import Flask, jsonify, request, flash, render_template, request, session, abort,redirect

from dataclasses import dataclass               # maybe we don't need these?
from flask_sqlalchemy import SQLAlchemy         #
from sqlalchemy import select,func, desc        #

from cs50 import SQL

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL('postgresql://mikemoloch:tingoo@localhost:5432/inventory')


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/list', methods=['GET'])
def list_customers():

    next_cust_id = 0    # Initialize var, not sure if we even need to?
    
    # Get all the customers so we can display them. Never mind the pagination concerns :)
    customers=db.execute('select * from customer order by customer_id')
    
    # Get the max customer id and add one to it , then pass it to
    # the listing.html so the New Entry field can be pre-populated 
    # db.session.execute(select(func.max(db.customer.c.customer_id)))
    
    # the select returns a list of dicts, in this case it only has one dict
    # of the form [{'customer_id': 6}], so you just get the first (0th) element
    # of that list and then index into the dict value by providing the key (customer_id)
    # note that YOU asked via the select statement to return that name 
    max_cust_id = db.execute('select max(customer_id) as customer_id from customer')[0]['customer_id']
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

    new_customer = db.execute("insert into customer(customer_id,name,price,quantity) values (:customer_id,:name,:price,:quantity)",customer_id=customer_id,name=name,price=price,quantity=quantity)

    
    return redirect("/list")

@app.route('/update-form/<cust_id>', methods=["GET"])
def update_form(cust_id):
    # Note the [0] at the end, it's getting the first item in the list that is returned
    customer = db.execute('select * from customer where customer_id=:cust_id',cust_id=cust_id)[0]
    return render_template("update_form.html",customer=customer)

@app.route('/update', methods=["POST"])
def update_customer():

    form_customer_id = request.form.get('customer_id')
    form_name = request.form.get('name')
    form_price = request.form.get('price')
    form_quantity = request.form.get('quantity')

    # persist in postgresql backend.
    retval = db.execute("update customer set  name=:name, price=:price, quantity=:quantity where customer_id=:customer_id",customer_id=form_customer_id,name=form_name,price=form_price,quantity=form_quantity)    
    
    return redirect("/list")
    #return(jsonify({"customer":customer.to_json()}))

@app.route('/delete/<cust_id>')
def delete_custid(cust_id):
    
    db.execute('delete from customer where customer_id=:cust_id',cust_id=cust_id)
    # log # print('deleted customer with customer_id= ',cust_id)
    return redirect('/list')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
