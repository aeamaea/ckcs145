# This version shows a form in the /protected page with values filled
# in from the backend db and lets you update them. :: aeam Nov 7 2023:w

from flask import Flask, redirect, request, url_for, Response, flash
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required


app = Flask(__name__)
app.secret_key = 'aquickbrownfoxjumpsoverthelazydog'

app.config['MONGODB_SETTINGS']= {'db':'jwfoods', 'host':'localhost', 'port':27017}

db = MongoEngine()
db.init_app(app)

login_manager  = LoginManager()
login_manager.init_app(app)

# mock "database"
# users = {'student@ryerson.ca': {'password':'secret'}}

# So this is the class to interface with the Users collection
# in the backend (notice the plural name) it's not the same
# as "User" just below. :: aeam

class Users(db.Document):
    email = db.StringField()
    password = db.StringField()

    meta = {'collection' : 'Users', 'allow_inheritance' : False}

class Coeffs(db.Document):
    weight_coeff = db.FloatField()
    distance_coeff = db.FloatField()

    meta = {'collection' : 'Coeffs', 'allow_inheritance' : False}

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
        return redirect(url_for('protected'))

    return 'Incorrect login'


# Protected route hence user must be logged in to access it.
@app.route('/protected', methods=["GET","POST"])
@login_required
def protected():
        # return 'Logged in as: ' + current_user.id 
    coeffs_from_db = Coeffs.objects().first()

    if request.method == 'GET':
        return '''
            <h3>Change Values and press Submit</h3>
            <form action='/protected' method='POST'>
                    weight coefficient &nbsp; <input type='text' name='weight_coeff' id='weight_coeff' placeholder='Weight Coeff like 0.3 etc' value='{wcoeff}' /> <br /> &nbsp; <br />
                    distance coefficient &nbsp; <input type='text' name='distance_coeff' id='distance_coeff' placeholder='Weight Coeff like 0.5 etc' value='{dcoeff}' /> <br /> &nbsp; <br />
                    <input type='submit' name='submit'/>
                </form>
            '''.format(wcoeff=coeffs_from_db.weight_coeff,dcoeff=coeffs_from_db.distance_coeff)

    # get values from the form fields
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
    return redirect('/protected')


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



if __name__ == "__main__":
    app.run(port=5000, debug=True)
