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
    url = 'https://wger.de/api/v2/exerciseinfo/{exercise_id}'
    data = '{"key": "value"}'
    headers = {'Accept': 'application/json',
               'Authorization': WGER_API_KEY}
    response = requests.get(url=url, data={}, headers=headers)
    muscles = response.json()
    
    exercise = crud.get_exercise_by_id(exercise_id)
    return render_template("exercise_details.html", exercise=exercise)

@app.route('/muscle')
def show_muscles():
    """Select muscle group to search exercises and add muscles to server DB if new are added to API"""
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
                new_muscle = crud.create_muscle_no_en(muscle_id, muscle_name)
                db.session.add(new_muscle)
                db.session.commit()
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
    """create new logs"""
    print("*"*20, "\n\n")
    print("WE ARE HAVING A PARTY IN create_log")
    
    # INFO needed to create new LOG record
    date = session["workout"]
    user_email = session.get("user_email")
    user = crud.get_user_by_email(user_email)
    user_id = user.user_id
    workout = crud.get_user_workout_by_date(date, user_id)
    workout_id = workout.workout_id
    num_of_sets = request.json.get("numberOfSets")
    num_of_sets = int(num_of_sets)
    #create exercise record for exercise db
    """TODO: is it necessary for me to make tables of exercise names and ids, since I'm pulling from the API anyway?"""
    """Yes, because I need those IDs for the workout logs"""
    #TODO grab exercise information from the form, check for existing record in DB
    exercise_id = request.json.get("exercise_id")
    exercise_id = int(exercise_id)
    exercise_name = request.json.get("exercise_name")
    exercise_description = request.json.get("exercise_description")
    print(request.json)
    print("*"*20, "\n\n")
    print(f"exercise id={exercise_id} exercise name = {exercise_name} exercise_description = {exercise_description}")
    print("*"*20, "\n\n")
    exercise = crud.get_exercise_by_API_id(exercise_id)
    print(exercise)
    print(exercise == "")
    
    if exercise == None:
        exercise = crud.create_exercise(exercise_id, exercise_name, exercise_description)
        db.session.add(exercise)
        db.session.commit()
        print("*"*20, "\n\n")
        print(f'Here are your exercises: {exercise}')
        print("*"*20, "\n\n")
    # FIXME: error when trying to create new exercise and new log; 
    # psycopg2.errors.ForeignKeyViolation) insert or update on table "logs" violates foreign key constraint "logs_exercise_id_fkey"
    # DETAIL:  Key (exercise_id)=(307) is not present in table "exercises".
    
    # create logs 
    for number in range(num_of_sets):
        log = crud.create_new_log(workout_id, exercise_id)
        db.session.add(log)
        db.session.commit()
        print("*"*20, "\n\n")
        print(log)
        print("*"*20, "\n\n")
    return "You got this!"

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

#TODO: VIEW/GET: view all exercises in a given workout when workout is clicked (view Logs)
#TODO: VIEW all workouts for user in a list
  
   
# @app.route('/workout_log')
# def update_log():
    
#     """add exercise to workout by creating a new log"""
#     # index_of_exercise = request.form.get("index_value")
#     # flash(f'{index_of_exercise}')
#     # muscle_id = session["muscle_id"]
#     # date = session["date"]
#     # email = session["email"]
#     # user_id = crud.get_user_by_email(email)
    
#     """check for exercise and/or create new exercise in db"""
#     exercise_name= request.form.get("exercise_name")
#     exercise_description = request.form.get("exercise_description")
#     exercise_id=request.form.get("exercise_id")
#     flash(f'{exercise_name}, {exercise_description}, {exercise_id}')
    
    
    
    
#     # workout_id = crud.get_user_workout_by_date(date_of_scheduled_workout=date, user_id=user_id)
#     # new_log = crud.create_new_log(workout_id=workout_id, exercise_id=exercise_id, )
# # index of exercise, add to exercise log
# # send to server the exercise and exercise id
# # flash that it's added
# # return redirect to same page
#     return redirect('/user_dashboard')


@app.route('/every_single_exercise')
def process_all_exercises():
    for index in range(0,2000,20):
        url = f'https://wger.de/api/v2/api/v2/exercise/?limit={index}&language=2'
        headers = {'Accept': 'application/json',
                   'Authorization': WGER_API_KEY}
        data = '{"key": "value"}'
        response = requests.get(url=url, data=data, headers=headers)
        print("*"*20, "\n\n")
        print(response)
        print("*"*20, "\n\n")
        exercises = response.json()
        print("*"*20, "\n\n")
        print(exercises)
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
    flash("Successfully logged out", 'alert alert-success')
    return redirect("/")




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
