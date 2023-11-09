import logging

from flask import Flask, request, jsonify, render_template,redirect,url_for, Response, flash
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

from dotenv import dotenv_values
from datetime import datetime

from flask_mongoengine import MongoEngine

# get secrets from the .env file 
config=dotenv_values(".env")

# we're not going to use the secrets because I'm using the mongo engine
# ORM now, PUGSQL not allowed by Mihal for the project, and I don't want to 
# deal with SQLAlchemy. :: aeam

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'aquickbrownfoxjumpsoverthelazydog' 	#The login/logout aka flask_login stuff needs this.mmkay?

app.config['MONGODB_SETTINGS']= {'db':'jwfoods', 'host':'localhost', 'port':27017}
db = MongoEngine()
db.init_app(app)

login_manager  = LoginManager()
login_manager.init_app(app)

#defin class that will interface with the backend for the protected pages (admin/login system)
class Users(db.Document):
    email = db.StringField()
    password = db.StringField()

    meta = {'collection' : 'Users', 'allow_inheritance' : False}

# define the jwfoods main page related stuff that is persisted in the mongo db
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

#----------------   End Database related Class definitions --------------------

#----------------   J&W foods contacts and Delivery calculator + main page --------------------
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

#----------------   End main page related routes --------------------

#----------------   Login/Logout + update coefficients table --------------------
# User class (what exactly is this doing?)
# from the docs: https://flask-login.readthedocs.io/en/latest/
# To make implementing a user class easier, you can inherit from UserMixin, 
# which provides default implementations for all of these properties and methods...
class User(UserMixin):
    pass

#Who calls this ? I don't see a direct reference to it in code below.
@login_manager.user_loader
def user_loader(email):

    user_from_db = Users.objects(email=email).first() # mongo document
    print("user_loader: ",user_from_db.password)

    if email != user_from_db.email:
        return
    
    user = User()
    user.id = email
    return user

#Login route that is used to create secure routes.
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return '''
            <form action='/login' method='POST'>
                    username &nbsp; <input type='text' name='email' id='email' placeholder='email'/> <br /> &nbsp; <br />
                    password &nbsp; <input type='password' name='password' id='password' placeholder='password'/> <br /> &nbsp; <br />
                    <input type='submit' name='submit'/>
                </form>
            '''

    email = request.form['email']

    user_from_db = Users.objects(email=email).first()  # Mongo collection
    if user_from_db:
        print(user_from_db.email, user_from_db.password)

    # if email in users and request.form['password'] == users[email]['password']:
    if user_from_db and email == user_from_db.email and request.form['password'] == user_from_db.password:
        user = User()       # instantiate user from class User which has default stuff
                            # coming in from the UserMixin 
        user.id = email     # user.id came in via UserMixin, now we're setting it before
        login_user(user)    # we call login_user() with user object whose id attribute we just set. mmkay?
        return redirect(url_for('admin'))

    return 'Incorrect login'


# Protected route hence user must be logged in to access it.
@app.route('/admin', methods=["GET","POST"])
@login_required
def admin():
    # return 'Logged in as: ' + current_user.id 
    coeffs_from_db = Coeffs.objects().first()

    #===============
    #    GET 
    #===============
    if request.method == 'GET':
        return '''
            <h3>Change Values and press Submit</h3>
            <form action='/protected' method='POST'>
                    weight coefficient &nbsp; <input type='text' name='weight_coeff' id='weight_coeff' placeholder='Weight Coeff like 0.3 etc' value='{wcoeff}' /> <br /> &nbsp; <br />
                    distance coefficient &nbsp; <input type='text' name='distance_coeff' id='distance_coeff' placeholder='Weight Coeff like 0.5 etc' value='{dcoeff}' /> <br /> &nbsp; <br />
                    <input type='submit' name='submit'/>
            </form>
            <br/><br/>
            <h2><a href="logout">LOG OUT</a></h2>
            '''.format(wcoeff=coeffs_from_db.weight_coeff,dcoeff=coeffs_from_db.distance_coeff)


    #===============
    #    POST 
    #===============
    # We're here so the request wasn't a GET , it was a POST ... 
    # so we just fell through to this code section

    # get values from the form fields sent via POST
    weight_coeff = request.form['weight_coeff']
    distance_coeff = request.form['distance_coeff']

    # print(weight_coeff, distance_coeff)

    # we already have the object populated with data from mongh
    # now we set the objects values to new values from form fields
    coeffs_from_db.weight_coeff = float(weight_coeff)
    coeffs_from_db.distance_coeff = float(distance_coeff)

    # and save it back :: aeam
    coeffs_from_db.save()

    # let the user know stuff happened.
    flash('Database updated!')

    # redirect back to the route /protected and we should see new values.
    return redirect('/admin')


# Logout from current session
@app.route('/logout')
@login_required # I added this cuz the docs do this. The lab code didn't have this :: aeam
def logout():
    logout_user()
    return 'Logged out'

# Handle unauthenticated users that access protected routes
@login_manager.unauthorized_handler
def unauthorized_handler():
     return 'Unauthorized', 401

#----------------   END Login/Logout + update coefficients table --------------------

if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
