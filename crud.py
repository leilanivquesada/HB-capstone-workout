"""CRUD Operations"""

from model import db, User, Workout, Exercise, Log, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    
def create_user(email, password, username):
    """ create a new user """
    user = User(email=email, password=password, username=username)
    return user

def get_by_user_id(user_id):
    """get user info by user_id"""
    return User.query.get(user_id)

def get_by_email(email):
    """get user by email"""
    return User.query.get(email)

def get_all_users():
    """ return all users """
    return User.query.all()

def create_exercise(exercise_name, exercise_description, exercise_pic_url):
    """ create a new exercise """
    new_exercise = Exercise(exercise_name=exercise_name, exercise_description=exercise_description, exercise_pic_url=exercise_pic_url)
    return new_exercise

def get_all_exercises():
    """ return all exercises """
    return Exercise.query.all()

def get_exercise_by_id(exercise_id):
    """return an exercise by exercise_id"""
    return Exercise.query.get(exercise_id)

def create_workout(date_of_scheduled_workout, user_id):
    """schedule a workout"""
    new_workout = Workout(date_of_scheduled_workout=date_of_scheduled_workout, user_id=user_id)

def get_all_workouts():
    return Workout.query.get.all()

def get_all_workouts_by_user_id(user_id):
    """get all workouts for a particular user"""
    return Workout.query.get(user_id).all()

def create_new_log(workout_id, exercise_id, num_reps, weight, weight_unit):
    """create a new log to add to the workout"""
    new_log = Log(workout_id=workout_id, exercise_id=exercise_id, num_reps=num_reps, weight=weight, weight_unit=weight_unit)
    return new_log

def update_workout_log(log_id, new_num_reps, new_weight, new_weight_unit):
    """update workout log"""
    log_update = Log.query.get(log_id)
    log_update.num_reps = new_num_reps
    log_update.weight = new_weight
    log_update.weight_unit = new_weight_unit
    return log_update