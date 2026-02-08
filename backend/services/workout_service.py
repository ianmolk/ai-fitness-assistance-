from models.workout import Workout
from database import db
from datetime import datetime

def create_workout(user_email, goal, experience):
    workout = Workout(
        user_email=user_email,
        goal=goal,
        experience=experience,
        created_at=datetime.utcnow()
    )

    db.session.add(workout)
    db.session.commit()

    return workout.to_dict()


def get_workouts(user_email):
    workouts = Workout.query.filter_by(user_email=user_email).all()
    return [w.to_dict() for w in workouts]
