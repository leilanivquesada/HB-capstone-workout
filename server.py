import json
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

from pprint import pformat, pprint
import os
import requests


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

BB_QUOTES_API_KEY = os.environ['BB_QUOTES_API_KEY']
WGER_API_KEY = os.environ['WGER_API_KEY']


@app.route('/')
def homepage():
    # Pull random bodybuilding quote from API to greet user at homepage
    url = 'https://bodybuilding-quotes1.p.rapidapi.com/random-quote'
    headers = {
	"X-RapidAPI-Host": "bodybuilding-quotes1.p.rapidapi.com",
	"X-RapidAPI-Key": BB_QUOTES_API_KEY
}
    bb_quote_response = requests.request("GET", url, headers=headers)
    bb_data = bb_quote_response.json()

    
    return render_template('homepage.html',
                           bb_data=bb_data
                           )

@app.route('/all_exercises')
def all_exercises():
    """View all exercises"""
    
    url = 'https://wger.de/api/v2/exercise/?language=2'
    data = '{"key": "value"}'
    headers = {'Accept': 'application/json',
               'Authorization': WGER_API_KEY}
    response = requests.get(url=url, data={}, headers=headers)
    exercises = response.json()
    exercises.keys()
    
    return render_template("all_exercises.html", exercises=exercises)

@app.route('/exercises/<exercise_id>')
def show_movie(exercise_id):
    """Show details on a particular exercise."""
    # url = f''
    
    
    
    exercise = crud.get_exercise_by_id(exercise_id)
    return render_template("exercise_details.html", exercise=exercise)

@app.route('/body')
def show_muscles():
    """Select muscle group to search exercises"""
    url = 'https://wger.de/api/v2/muscle/'
    data = '{"key": "value"}'
    headers = {'Accept': 'application/json',
               'Authorization': WGER_API_KEY}
    response = requests.get(url=url, data={}, headers=headers)
    muscles = response.json()
    
    
    return render_template("body.html", muscles=muscles)    

    
    
    
@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if not user or user.password != password: 
        flash("The email or password you entered is incorrect.")
    else: 
        session["user_email"] = user.email
        flash(f"welcome back, {user.username}!")
    return redirect("/")

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")
    
# @app.route('/users')
# def all_users():
#     """"View all users"""
#     users = crud.get_users()
#     return render_template("all_users.html",users=users)

# #TODO for some reason would not route to USERS, so changed to user. unsure what is causing this
# @app.route('/user/<user_id>')
# def show_users(user_id):
#     """Show details on a particular user"""
#     user = crud.get_user_by_id(user_id)
#     return render_template("user_details.html",user=user)
    


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
