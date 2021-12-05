import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from app import app
from app.forms import LoginForm, RegisterForm, EventForm
from flask import render_template, session, redirect, url_for, flash
from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

try:
    myclient = MongoClient(getenv("MONGO_URI"))
    mydb = myclient[getenv("MONGO_COLLECTION")]
    print(mydb.collection_names())
    events = mydb["events"]
    users = mydb["users"]
    print(events)
except:
    print("Error: Unable to connect to database")

def assignSession(username):
    session["username"] = username

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form=LoginForm()
    if form.validate_on_submit():
        user = mydb.users.find_one({'username': form.username.data})
        if user and user['password'] == form.password.data:
            assignSession(user['username'])
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
        assignSession(form.username.data)
    return render_template("signin.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirmPassword = form.confirmPassword.data
        if password != confirmPassword:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
        if mydb.users.find_one({'username': username}):
            flash('Username already taken')
            return redirect(url_for('signup'))
        mydb.users.insert_one({"username": username, "email": email, "password": password})
        assignSession(username)
        return redirect(url_for('dashboard'))
    return render_template("signup.html", form=form)

@app.route("/dashboard")
def dashboard():
    if not 'username' in session:
        return redirect(url_for('signin'))
    return render_template("dashboard.html", session=session)

@app.route("/events/create", methods=['GET', 'POST'])
def createEvent():
    if not 'username' in session:
        return redirect(url_for('signin'))
    form=EventForm()
    if form.validate_on_submit():
        eventName = form.eventName.data
        goal = form.goal.data
        imageURL = form.imageURL.data
        mydb.events.insert_one({"eventName": eventName, "goal": goal, "imageURL": imageURL, "creator": session['username'], "currentRaised": 0})
        print(eventName, goal)
        return redirect(url_for("dashboard"))
    return render_template("createEvent.html", session=session, form=form)

@app.route("/events")
def events():
    if not 'username' in session:
        return redirect(url_for('signin'))
    events = mydb.events.find()
    print(events)
    return render_template("events.html", session=session, events=events)

@app.route("/events/<eventName>", methods=[ 'GET', 'POST'])
def event(eventName):
    if not 'username' in session:
        return redirect(url_for('signin'))
    event = mydb.events.find_one({"eventName": eventName})
    return render_template("event.html", session=session, event=event)