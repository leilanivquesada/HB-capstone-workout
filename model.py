"""Models for workout application"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    
    def __repr__(self):
        """Show info about the user"""
        return f"<User id={self.user_id} email={self.email} username ={self.username}>"
    
    @classmethod
    def create(cls, email, password, username):
        """create and return a new user"""
        return cls(email=email, password=password, username=username)
    
    @classmethod
    def get_by_id(cls, user_id):
        """get by user id"""
        return cls.query.get(user_id)
    
    @classmethod
    def get_by_username(cls, username):
        """get by username"""
        return cls.query.get(username)
    
    @classmethod
    def get_by_email(cls,email):
        """queries by user email"""
        return cls.query(User.email == email).first()
    
    @classmethod
    def all_users(cls):
        """ returns a list of all users"""
        return cls.query.all()
    
class Exercise(db.Model):
    
    __tablename__ = "exercises"
    
    exercise_id = db.Column(db.Integer, autoincrement=True, primary_key= True, nullable=False)
    exercise_name = db.Column(db.Text)
    exercise_description = db.Column(db.String)
    exercise_pic_url = db.Column(db.String)
    
    def __repr__(self):
        return f'<Exercise id={self.exercise_id} exercise name={self.exercise_name} description={self.exercise_description}>'

    @classmethod
    def create(cls, exercise_name, exercise_description, exercise_pic_url):
        """ creates an exercise for the exercise database"""
        return cls(
            exercise_name=exercise_name, 
            exercise_description=exercise_description, 
            exercise_pic_url=exercise_pic_url
        )
        
    @classmethod
    def all_exercises(cls):
        """ returns all exercises """
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls,exercise_id):
        """ returns an exercise by primary key"""
        return cls.query.get(exercise_id)
    
class Workout(db.Model):
    
    __tablename__ = "workouts"
    
    workout_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    date_of_scheduled_workout= db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    user = db.relationship("User", backref="workouts")
    
    def __repr__(self):
        return f'<Workout id={self.workout_id}, date of scheduled workout={self.date_of_scheduled_workout}, user={self.user_id}>'

    @classmethod
    def create(cls, date_of_scheduled_workout, user):
        return cls(date_of_scheduled_workout=date_of_scheduled_workout, user=user)
    
    @classmethod
    def get_by_id(cls, workout_id):
        """ returns a workout by primary key"""
        return cls.query.get(workout_id)
    
    @classmethod
    def all_workouts(cls):
        """returns all workouts"""
        return cls.query.all()
    
    
class Log(db.Model):
    
    __tablename__ = 'logs'
    
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=False)
    num_reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    weight_unit = db.Column(db.String)
    
    workout = db.relationship("Workout", backref="logs")
    exercise = db.relationship("Exercise", backref ="logs")

    def __repr__(self):
        return f'<Log id={self.log_id}, num_reps={self.num_reps}, weight={self.weight}, weight_unit={self.weight_unit}>'

    @classmethod
    def create(cls, workout, exercise, num_reps, weight, weight_unit):
        """ creates a new log"""
        return cls(workout=workout, exercise=exercise, num_reps=num_reps, weight=weight, weight_unit=weight_unit)
    
    @classmethod
    def get_by_id(cls, log_id):
        """ returns a single log"""
        return cls.query.get(log_id)
    
    @classmethod
    def update(cls, log_id, exercise_id, new_num_reps, new_weight, new_weight_unit):
        """update log"""
        log_update = cls.query.get(log_id)
        log_update.num_reps = new_num_reps
        log_update.weight = new_weight
        log_update.weight_unit = new_weight_unit
        
    @classmethod
    def all_logs(cls):
        """ returns all workouts"""
        return cls.query.all()


    
def connect_to_db(flask_app, db_uri="postgresql:///users", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
