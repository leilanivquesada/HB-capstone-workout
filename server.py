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

# TODO: test this route
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

# TODO: test this route
# @app.route('/exercises/<exercise_id>')
# def show_exercise(exercise_id):
#     """Show details on a particular exercise."""
#     url = 'https://wger.de/api/v2/exerciseinfo/{exercise_id}'
#     data = '{"key": "value"}'
#     headers = {'Accept': 'application/json',
#                'Authorization': WGER_API_KEY}
#     response = requests.get(url=url, data={}, headers=headers)
#     muscles = response.json()
    
#     exercise = crud.get_exercise_by_id(exercise_id)
#     return render_template("exercise_details.html", exercise=exercise)

@app.route('/muscle')
def show_muscles():
    """Select muscle group to search exercises and add muscles to server DB if new are added to API"""
    print(f'LEILANILOOKATTHISTHENEXTLINEISTHEDATEOFTHEWORKOUTTHATISINSESSION')
    print(session["workout"])
    print(f'LEILANILOOKATTHISTHENEXTLINEISTHEDATEOFTHEWORKOUTTHATISINSESSION')
    #FIXME: why is the session workout date defaulting to 5/10/2022 even though I've popped it at log out?
    if session["workout"] == "":
        flash("Please schedule your workout first!", 'alert alert-danger')
        return redirect("/user_dashboard")
    
    url = 'https://wger.de/api/v2/muscle/'
    data = '{"key": "value"}'
    headers = {'Accept': 'application/json',
               'Authorization': WGER_API_KEY}
    response = requests.get(url=url, data={}, headers=headers)
    muscles = response.json()
    results = muscles['results']
    sorted_results = sorted(results, key=lambda k : k['id'])
    
    for result in sorted_results:    
        muscle_id = result['id']    
        muscle = crud.get_muscle_by_api_id(muscle_id)
        if muscle == None:
            muscle_name = result['name']
            muscle_en_name = result['name_en']
            if muscle_en_name not in result:
                new_muscle = crud.create_muscle(muscle_id, muscle_name, muscle_name)
            else:
                new_muscle = crud.create_muscle(muscle_id, muscle_name, muscle_en_name)
            db.session.add(new_muscle)
            db.session.commit()
            
    return render_template("muscle.html", muscles=muscles)    

@app.route('/exercise_details/<muscle_id>')
def get_exercise_by_muscle_id(muscle_id):
    """display exercise by muscle_id, create new logs for workout"""
    url = f'https://wger.de/api/v2/exercise/?muscles={muscle_id}&language=2'
    headers = {'Accept': 'application/json',
               'Authorization': WGER_API_KEY}
    response = requests.get(url=url, data={}, headers=headers)
    exercise = response.json()
    
    session["muscle_id"] = muscle_id
    session.modified = True
    
    return render_template("exercise_details.html", exercise=exercise)
    
@app.route("/add_to_workout", methods=["POST"])
def create_log():
    """create new logs and exercises"""
    # INFO needed to create new LOG record
    date = session["workout"]
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    workout = crud.get_user_workout_by_date(date, user_id)
    workout_id = workout.workout_id
    num_of_sets = request.json.get("numberOfSets")
    num_of_sets = int(num_of_sets)
    #INFO needed to create/check exercise record for exercise db
    exercise_api_id = str(request.json.get("exercise_id"))
    exercise = crud.get_exercise_by_api_id(exercise_api_id)
    print("*"*20, "\n\n")
    if exercise:
        exercise_id = exercise.id
    else:    
        exercise_name = request.json.get("exercise_name")
        exercise_description = request.json.get("exercise_description")    
        new_exercise = crud.create_exercise(exercise_api_id, exercise_name, exercise_description)
        db.session.add(new_exercise)
        db.session.commit()
        exercise_id = new_exercise.id
    # create logs 
    for number in range(num_of_sets):
        log = crud.create_new_log(workout_id, exercise_id)
        db.session.add(log)
        db.session.commit()
    return "You got this!"

@app.route('/update_workout_log', methods=["GET"])
def display_workout_log():
    """View logs scheduled to a workout, allowing users to update each log"""
    
    # TODO: make a way for the person to add to the log. They can grab from the calendar or click on a link?
    workout_date = session['workout']
    user_email = session["user_email"]
    
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    user_workout = crud.get_user_workout_by_date(workout_date, user_id)
    
    if not user_workout:
        flash('Select the workout date to log first!', 'alert alert-danger')
        return redirect('/user_dashboard', user=user)
    
    workout_id = user_workout.workout_id
    user_logs = crud.view_all_logs_by_workout(workout_id)
    full_workout_log = []
    
    for workout_log in user_logs:
        exercise_id = workout_log.exercise_id
        exercise = crud.get_exercise_by_id(exercise_id)
        exercise_name = exercise.exercise_name
        exercise_description = exercise.exercise_description
        log_to_render = {
            # 'exercise_id': log['exercise_id'], #unsure if I need this code
            'exercise_name': exercise_name,
            'exercise_description': exercise_description,
            'log_id': workout_log.log_id
        }
        full_workout_log.append(log_to_render)
    # in jinja, create a form that loops through the user_logs and creates fields to fill- num reps, weight and defaults to lb for weight unit
    
    return render_template("workout_log.html", full_workout_log=full_workout_log, workout_date=workout_date)

@app.route('/update_workout_log', methods=["POST"])
def update_workout_log():
    """Update workout logs with info from form"""
    weight = request.json.get("weight")
    print(f'weight: {weight}')
    # weight = int(weight)
    num_of_reps = request.json.get("num_of_reps")
    # num_of_reps = int(num_of_reps)
    weight_unit = request.json.get("weight_unit")
    log_id = request.json.get('log_id')
    log_update = crud.update_workout_log(log_id, num_of_reps, weight, weight_unit)
    print(log_update)
    print(crud.get_log_by_id(log_id))
    # FIXME: the committed record is not showing that num_reps nor weight are being saved. when convert to int, showing error.
    print("Updated")
    
    view_user_workout_logs = crud.get_log_by_id(log_id)
    print(view_user_workout_logs)
    return "Success!"

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
    session.modified = True
    if workout:
        flash("Workout already exists! Add more exercises, or update your workout details by recording it.", 'alert alert-danger')
    else:
        workout = crud.create_workout(date, user_id)
        db.session.add(workout)
        db.session.commit()
        flash("Workout added! Start adding exercises.", 'alert alert-success')
    return redirect("/muscle")

@app.route('/delete_log', methods=["DELETE"])
def delete_exercise_log():
    """The user may delete an exercise log"""
    log_id = request.json.get("log_id")
    deleted_log = crud.delete_log(log_id)
    
    
    
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
    return render_template("/user_dashboard.html", user=user)

#TODO: VIEW/GET: view all exercises in a given workout when workout is clicked (view Logs)
#TODO: VIEW all workouts for user in a list
  
   
# @app.route('/workout_log')
# def update_log():
    
# TODO: test this route. is this route even necessary?
@app.route('/every_single_exercise')
def process_all_exercises():
    for index in range(0,2000,20):
        url = f'https://wger.de/api/v2/api/v2/exercise/?limit={index}&language=2'
        headers = {'Accept': 'application/json',
                   'Authorization': WGER_API_KEY}
        data = '{"key": "value"}'
        response = requests.get(url=url, data=data, headers=headers)
        exercises = response.json()
        print("*"*20, "\n\n")
        with open('exercises.json','w') as json_file:
            json.dump(exercises, json_file)
        return "There you go!"
    
@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""
    email = request.form.get("email")
    password = request.form.get("password") 
    user = crud.get_user_by_email(email)
    if email == "":
        flash("Please enter an email and password to log in", 'alert alert-danger')
        return redirect("/")
    elif not user or user.password != password: 
        flash("The email or password you entered is incorrect.", 'alert alert-danger')
        return redirect("/")
    else: 
        session["user_email"] = user.email
        username = user.username
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
    session.pop(session["workout"], None)
    session.pop(session["muscle_id"], None)
    flash("Successfully logged out", 'alert alert-success')
    return redirect("/")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
