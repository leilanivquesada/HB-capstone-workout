"""CRUD Operations"""

from model import db, User, Workout, Exercise, Log, Muscle, connect_to_db

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

def get_user_by_email(email):
    """get user by email"""
    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """get user info by username"""
    return User.query.filter(User.username == username).first()

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
    return new_workout

def get_all_workouts():
    return Workout.query.all()

def get_all_workouts_by_user_id(user_id):
    """get all workouts for a particular user"""
    return Workout.query.filter_by(user_id=user_id).all()

def get_user_workout_by_date(date_of_scheduled_workout, user_id):
    """get workout for user on scheduled date"""
    return Workout.query.filter_by(date_of_scheduled_workout=date_of_scheduled_workout, user_id=user_id).first()

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

def view_all_logs():
    """view all workout logs"""
    return Log.query.all()

def view_all_logs_by_user_id(user_id):
    """view all logs for a user"""
    return Log.query.filter_by(user_id=user_id)

def view_all_logs_by_user_by_workout(user_id, workout_id):
    """view all logs for a user and date"""
    return Log.query.filter_by(user_id=user_id, workout_id=workout_id)

def get_exercise_by_muscle_id(muscle_id):
    """get list of exercises pertaining to a specific muscle group"""
    return Exercise.query.filter(muscle_id=muscle_id).all()

def get_all_muscles():
    """get a list of all muscles"""
    return Muscle.query.get.all()

def get_muscle_by_id(muscle_id):
    """return a muscle by its id"""
    return Muscle.query.get(muscle_id)

def create_muscle(name):
    """create muscle"""
    new_muscle = Muscle(name=name)
    return new_muscle