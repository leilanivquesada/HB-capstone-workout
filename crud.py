"""CRUD Operations"""

from model import db, User, Workout, Exercise, Log, Muscle, connect_to_db
from sqlalchemy import func

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    
"""Users CRUD Operations"""
    
def create_user(email, password, username):
    """ create a new user """
    user = User(email=email, password=password, username=username)
    return user

def get_by_user_id(user_id):
    """get user info by user_id"""
    return User.query.get_or_404(user_id)

def get_user_by_email(email):
    """get user by email"""
    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """get user info by username"""
    return User.query.filter(User.username == username).first()

def get_all_users():
    """ return all users """
    return User.query.all()

"""Exercise CRUD Operations"""

def create_exercise(exercise_api_id, exercise_name, exercise_description):
    """ create a new exercise """
    new_exercise = Exercise(exercise_api_id=exercise_api_id, exercise_name=exercise_name, exercise_description=exercise_description)
    return new_exercise

def get_all_exercises():
    """ return all exercises """
    return Exercise.query.all()

def get_exercise_by_id(id):
    """return an exercise by exercise_id"""
    return Exercise.query.get(id)

def get_exercise_by_api_id(exercise_api_id):
    """return an exercise by exercise_id"""
    return Exercise.query.filter_by(exercise_api_id=exercise_api_id).first()

"""Workout CRUD Operations"""

def create_workout(date_of_scheduled_workout, user_id):
    """schedule a workout"""
    new_workout = Workout(date_of_scheduled_workout=date_of_scheduled_workout, user_id=user_id)
    return new_workout

def get_all_workouts():
    return Workout.query.all()

def get_all_workouts_by_id(workout_id):
    """get all workouts for a particular user"""
    return Workout.query.get(workout_id)

def get_all_workouts_by_user_id(user_id):
    """get all workouts for a particular user"""
    return Workout.query.filter_by(user_id=user_id).all()

def get_user_workout_by_date(date_of_scheduled_workout, user_id):
    """get workout for user on scheduled date"""
    return Workout.query.filter_by(date_of_scheduled_workout=date_of_scheduled_workout, user_id=user_id).first()

"""Log CRUD operations"""

def get_log_by_id(log_id):
    return Log.query.get(log_id)

def create_new_log(workout_id, exercise_id):
    """create a new log to add to the workout"""
    new_log = Log(workout_id=workout_id, exercise_id=exercise_id)
    return new_log

def update_workout_log(log_id, new_num_reps, new_weight, new_weight_unit):
    """update workout log"""
    log_update = Log.query.get(log_id)
    log_update.num_reps = new_num_reps
    log_update.weight = new_weight
    log_update.weight_unit = new_weight_unit
    db.session.commit()

def view_all_logs():
    """view all workout logs"""
    return Log.query.all()

def view_all_logs_by_workout(workout_id):
    """view all logs for a user and date"""
    return Log.query.filter_by(workout_id=workout_id).all()


    
    
    
def get_exercise_in_log(log_id):
    """get the name of the exercise in the log"""
    log = Log.query.get(log_id)
    exercise_id = log.exercise_id
    return Exercise.query.get(exercise_id)

def delete_log(log_id):
    log = Log.query.get(log_id)
    db.session.delete(log)
    db.session.commit()
    return
    

"""Muscles CRUD operations"""

def get_exercise_by_muscle_id(muscle_id):
    """get list of exercises pertaining to a specific muscle group"""
    return Exercise.query.filter(muscle_id=muscle_id).all()

def get_all_muscles():
    """get a list of all muscles"""
    return Muscle.query.get.all()

def get_muscle_by_id(id):
    """return a muscle by its id"""
    return Muscle.query.get_or_404(id)

def get_muscle_by_api_id(muscle_id):
    """return a muscle by its api id"""
    return Muscle.query.filter_by(muscle_id=muscle_id).first()

def create_muscle(muscle_id, name, en_name):
    """create muscle"""
    new_muscle = Muscle(muscle_id=muscle_id, name=name, en_name=en_name)
    return new_muscle

def create_muscle_no_en(muscle_id, name):
    """create muscle"""
    new_muscle = Muscle(muscle_id=muscle_id, name=name)
    return new_muscle

"""USER DASHBOARD CRUD OPERATIONS"""
def get_user_max_weight(user_id):
    """lame function. get the user's max weight (EVERRR)"""
    return db.session.query(func.max(Log.weight)).join(Workout).filter_by(user_id=user_id).first()

def get_user_distinct_exercise_list(user_id):
    """get list of distinct exercises that user has done"""
    # get list of user workouts
    # get list of logs in each workout
    # for each log, get exercise name, exercise id
    user_exercise_set = set()
    # user_workouts = 
    user = User.query.get(user_id)
    for workout in user.workouts:
        for log in workout.logs:
            user_exercise_set.add(log.exercise.id)
            
    user_exercise_list= []
    for item in user_exercise_set:
        exercise=Exercise.query.get(item)
        user_exercise_list.append({'exercise_id': item, 'exercise_name': exercise.exercise_name})
    return user_exercise_list        
        
            
            
    
    

def get_log_by_exercise_id(exercise_id, user_id):
    """ return the logs for user that contain that exercise"""
    # take all the logs with that exercise in it
    logs = Log.query.filter_by(exercise_id=exercise_id).all()
    user_logs = []
    # take all the workouts those logs
    for log in logs:
        # get the workout ids
        workout_id = log.workout_id
        workout = Workout.query.filter_by(workout_id=workout_id, user_id=user_id).all()
        if workout:
            user_logs.append(log)
    return user_logs