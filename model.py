"""Models for workout application"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    
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
        """query by user email"""
        return cls.query(User.email == email).first()
    
    
    @classmethod
    def all_users(cls):
        """return a list of all users"""
        return cls.query.all()
    
class Exercise(db.Model):
    
    tablename = "exercises"
    
    exercise_id = db.Column(db.Integer, autoincrement=True, primary_key= True)
    exercise_name = db.Column(db.Text)
    exercise_description = db.Column(db.String)
    exercise_pic_url = db.Column(db.String)
    
    def __repr__(self):
        return f'<Exercise id={self.exercise_id} exercise name={self.exercise_name} description={self.exercise_description}>'

    @classmethod
    def create(cls, exercise_name, exercise_description, exercise_pic_url):
        """Creates an exercise for the exercise database"""
        return cls(
            exercise_name=exercise_name, 
            exercise_description=exercise_description, 
            exercise_pic_url=exercise_pic_url
        )
        
    @classmethod
    def all_exercises(cls):
        """ return all exercises """
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls,exercise_id):
        """Return an exercise by primary key"""
        return cls.query.get(exercise_id)
    
# class Workout(db.Model):
    
#     tablename = "workouts"
    
#     workout_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     date_of_scheduled_workout= db.Column(db.Date, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'))
    
    
#     user = db.relationship("User", backref="workouts")
#     exercise = db.relationship("Exercise", backref = "workouts")




    
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
