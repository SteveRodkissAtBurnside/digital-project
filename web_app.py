"""
Web app to provide feedback from and to students and teachers
Author: Joseph Grace
Version: 1.0
Created 05/05/2020
"""

import os
from flask import Flask, request, url_for, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user
from passlib.hash import bcrypt

#HASHKEY_FILENAME = "hashkey.dat"
SECRET_KEY_FILENAME = "secretkey.dat"
BCRYPT_ROUNDS = 14

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__) ) #This is the directory of the project
database_file = "sqlite:///{}".format(os.path.join(PROJECT_DIR,"database.db")) #Get path to database file

app = Flask(__name__) #define app
app.config["SQLALCHEMY_DATABASE_URI"] = database_file #give path of database to app
db = SQLAlchemy(app) #connect to database

#Using user structure for flask_login:
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable = False)
    site_access = db.Column(db.Integer, default=0)
    def get_id(self):
        return str(self.user_id)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))

class Projects(db.Model):
    __tablename__ = "projects"
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    visitor_default_access = db.Column(db.Integer, default=0)
    student_default_access = db.Column(db.Integer, default=0)
    time_created = db.Column(db.DateTime)
    time_updated = db.Column(db.DateTime)

@app.route("/")
def index():
    return "This is the home page"

@app.route("/dashboard")
@login_required
def dashboard():
    return "You've accessed the dashboard!"

@app.route("/register", methods=["GET", "POST"])
def register():
    print("Register", request.form, flush=True)
    if request.form:
        print("Form recieved", flush=True)
        username = request.form.get("username")
        if not Users.query.filter_by(username=username).first() is None:
            print("Error 1", flush=True)
        else:
            password_plaintext = request.form.get("password")
            password_hash = bcrypt.hash(password_plaintext, rounds=BCRYPT_ROUNDS)
            new_user = Users(username=request.form.get("username"),
                             password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            print("Added new user:",new_user, flush=True)
            login_user(new_user)
            return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    logout_user()
    if request.form:
        username = request.form.get("username")
        user = Users.query.filter_by(username=username).first()
        password_plaintext = request.form.get("password")
        if Users.query.filter_by(username=username).first() is None:
            print("Error 2", flush=True)
        else:
            if bcrypt.verify(password_plaintext,user.password_hash):
                login_user(user)
                return redirect(url_for("dashboard"))
            else:
                print("Error 3", flush=True)
                #Error 2 and 3 must be presented as the same error for security reasons.
    return render_template("login.html")    

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

def generate_key(filename, size):
    file = open(filename,"wb")
    print(os.urandom(size))
    file.write(os.urandom(size))
    file.close()
    
def get_key(filename):
    file = open(filename,"rb")
    key = file.read()
    file.close()
    return key

def file_location(path):
    return os.path.join(PROJECT_DIR, path)

if __name__ == "__main__":
    #if not os.path.exists(file_location(HASHKEY_FILENAME)):
        ##Create password hash key
        #generate_key(HASHKEY_FILENAME, 64)
    if not os.path.exists(file_location(SECRET_KEY_FILENAME)):
        #Create session secret key
        generate_key(SECRET_KEY_FILENAME, 24)
    app.secret_key = get_key(SECRET_KEY_FILENAME)
    if not os.path.exists(file_location(database_file)):
        db.create_all()
    app.run(debug=True)