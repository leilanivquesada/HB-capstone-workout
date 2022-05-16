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
def render_homepage():
    """render the initial page."""
    return render_template('homepage.html')

@app.route('/all-exercises')
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
def show_exercise(exercise_id):
    """Show details on a particular exercise."""
    # url = f''
    
    exercise = crud.get_exercise_by_id(exercise_id)
    return render_template("exercise_details.html", exercise=exercise)

@app.route('/muscle')
def show_muscles():
    """Select muscle group to search exercises"""
    url = 'https://wger.de/api/v2/muscle/'
    data = '{"key": "value"}'
    headers = {'Accept': 'application/json',
               'Authorization': WGER_API_KEY}
    response = requests.get(url=url, data={}, headers=headers)
    muscles = response.json()
    
    
    return render_template("muscle.html", muscles=muscles)    

@app.route('/exercise_details/<muscle_id>')
def get_exercise_by_muscle_id(muscle_id):
    """display exercise by muscle_id"""
    url = f'https://wger.de/api/v2/exercise/?muscles={muscle_id}&language=2'
    data = '{"key": "value"}'
    headers = {'Accept': 'application/json',
               'Authorization': WGER_API_KEY}
    response = requests.get(url=url, data={}, headers=headers)
    exercise = response.json()
    results = exercise['results']
    length = len(results)
    
    session["muscle_id"] = muscle_id
    session.modified = True
    
    # change this to instead render via a fetch request using javascript
    return render_template("exercise_details.html", exercise=exercise, length=length)
    
    
#TODO create route to CREATE workout by scheduling workout
    #TODO create exercises 
#TODO add route to VIEW workout
#

#TODO
@app.route("/schedule_workout", methods=["POST"])
def create_workout():
    """Create a new workout."""
    # import pdb; pdb.set_trace()

    date = request.form.get("cal-to-schedule-workout")
    user_email = session["user_email"]
    
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    
    workout = crud.get_user_workout_by_date(date, user_id)
    session["workout"] = date
    # TODO make sure only one workout in session, check your notes
    if workout:
        flash("Workout already exists! Edit the workout by adding exercises.", 'alert alert-danger')
    else:
        workout = crud.create_workout(date, user_id)
        db.session.add(workout)
        db.session.commit()
        flash("Workout added! Start adding exercises.", 'alert alert-success')

    return redirect("/muscle")

@app.route('/user_dashboard')
def display_user_dashboard():
    """display user dashboard"""
    #TODO need to make a chart in JS Chart
    #TODO need to display lists of workouts
        # Pull random bodybuilding quote from API to greet user at user_dashboard
    #TODO why isn't username displaying in dashboard? Error 'user' is undefined 
    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    username = user.username  
    
#     url = 'https://bodybuilding-quotes1.p.rapidapi.com/random-quote'
#     headers = {
#     "X-RapidAPI-Host": "bodybuilding-quotes1.p.rapidapi.com",
#     "X-RapidAPI-Key": BB_QUOTES_API_KEY
# }
#     bb_quote_response = requests.request("GET", url, headers=headers)
#     bb_data = bb_quote_response.json()
    
    # return render_template("/user_dashboard.html", bb_data=bb_data)
    return render_template("/user_dashboard.html")

#TODO: POST: add exercises to workout by making new Logs
#TODO: VIEW/GET: view all exercises in a given workout when workout is clicked (view Logs)
#TODO: VIEW all workouts for user in a list
  
    
@app.route('/add_to_workout', methods=["POST"])
def add_exercise_to_workout():
    """add exercise to workout by creating a new log"""
    index_of_exercise = request.form.get("index_value")
    flash(f'{index_of_exercise}')
    muscle_id = session["muscle_id"]
    date = session["date"]
    email = session["email"]
    user_id = crud.get_user_by_email(email)
    
    """check for exercise and/or create new exercise in db"""
    exercise_name= request.form.get("exercise_name")
    exercise_description = request.form.get("exercise_description")
    exercise_id=request.form.get("exercise_id")
    flash(f'{exercise_name}, {exercise_description}, {exercise_id}')
    
    
    
    
    
    
    # workout_id = crud.get_user_workout_by_date(date_of_scheduled_workout=date, user_id=user_id)
    # new_log = crud.create_new_log(workout_id=workout_id, exercise_id=exercise_id, )
# index of exercise, add to exercise log
# send to server the exercise and exercise id
# use crud new log function to create new log
# flash that it's added
# return redirect to same page
    return redirect('/exercise_details/')






    
@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    username = user.username
    
    if email == "":
        flash("Please enter an email and password to log in", 'alert alert-danger')
        return redirect("/")
    elif not user or user.password != password: 
        flash("The email or password you entered is incorrect.", 'alert alert-danger')
        return redirect("/")
    else: 
        session["user_email"] = user.email
        flash(f"Welcome back, {user.username}!", 'alert alert-success')
        return redirect("/user_dashboard")
    

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    user_email = crud.get_user_by_email(email)
    user_username = crud.get_user_by_username(username)

    if user_email or user_username:
        flash("Cannot create an account. The email or username is already in use. Try again.", 'alert alert-danger')
    else:
        user = crud.create_user(email, password, username)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.", 'alert alert-success')

    return redirect("/")
    
@app.route('/users')
def all_users():
    """"View all users"""
    users = crud.get_all_users()
    return render_template("all_users.html",users=users)

@app.route('/user/<user_id>')
def show_users(user_id):
    """Show details on a particular user"""
    user = crud.get_by_user_id(user_id)
    return render_template("user_details.html",user=user)
    
@app.route("/logout")
def logout():
    """Log user out."""
    session.pop(session["user_email"], None)
    flash("Successfully logged out", 'alert alert-success')
    return redirect("/")




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
