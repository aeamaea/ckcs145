import logging

from flask import Flask, request, jsonify, render_template
from dotenv import dotenv_values
from datetime import datetime

from flask_mongoengine import MongoEngine

# get secrets from the .env file 
config=dotenv_values(".env")

# import pugsql 
# queries = pugsql.module('queries/')
# queries.connect('postgresql://'+config["PG_USER"]+':'+config["PG_PASS"]+'@localhost:5432/jwfoods')


"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)

app.config['MONGODB_SETTINGS']= {'db':'jwfoods', 'host':'localhost', 'port':27017}
db = MongoEngine()
db.init_app(app)


class Coeffs(db.Document):
	weight_coeff = db.FloatField()
	distance_coeff = db.FloatField()

	meta = {'collection' : 'Coeffs', 'allow_inheritance' : False}

class Visits(db.Document):
	ip_address = db.StringField()
	timestamp = db.StringField()

	meta = {'collection' : 'Visits', 'allow_inheritance' : False}

class Contacts(db.Document): 

	contact_name = db.StringField()
	email = db.StringField()
	comments = db.StringField()
	ip_address = db.StringField()
	timestamp = db.StringField()

	meta = {'collection' : 'Contacts', 'allow_inheritance' : False}


@app.route("/", methods=["GET"])
def homepage():
	ip_address = request.remote_addr
	timestamp = str(datetime.now())
	# insert_result = queries.insert_visit(visit_time=visit_time, visit_ip=visit_ip)
	new_visit = Visits(ip_address=ip_address, timestamp=timestamp)
	print(ip_address,timestamp,"populated obj",new_visit.ip_address,"--", new_visit.timestamp)
	new_visit.save()

	# print("insert return code: ", insert_result)

	return render_template('company1.1.html')

# The delivery Calculator on the HTML page makes a POST request 
# to this route in the JQuery JS code in the SCRIPT tag This is an AJAX
# request to this endpoint from the page and then the JS on the html page
# shows it in line - A project requirement :: aeam
@app.route("/calc_charges",methods=["POST"])
def calc_charges():

	distance = float(request.form["distance"])
	weight = float(request.form["weight"])

	# get the coefficients from the Coeff documents 
	# from the Mongo backend.
	coeffs = Coeffs.objects.first()
	weight_coeff=coeffs.weight_coeff
	dist_coeff=coeffs.distance_coeff

	delivery_cost = round((distance * dist_coeff) + (weight * weight_coeff),2)
	print(weight,distance,delivery_cost)

	return jsonify({"delivery_cost" : delivery_cost})

@app.route("/add_contact",methods=["POST"])
def add_contact():

	ip_address = request.remote_addr
	timestamp = str(datetime.now())
	contact_name = request.form["name"]
	email = request.form["email"]
	comments = request.form["comments"]

	
	# create a Contacts instance and fill it up with values
	# then persist it to the MongoDB backend :: aeam

	new_contact = Contacts(ip_address=ip_address,timestamp=timestamp,contact_name=contact_name, email=email, comments=comments)
	db_opstatus = new_contact.save()

	print("\n\n---\ndb operation status: ",list(db_opstatus),"\n---\n\n")

	if db_opstatus:
		return jsonify({"status" : "Success"})
	else:
		return jsonify({"status":"ERROR"})




if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
