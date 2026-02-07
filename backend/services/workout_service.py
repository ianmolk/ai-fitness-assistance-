from datetime import datetime

workouts = {}

def create_workout(user_email, goal, experience):
    workout = {
        "goal": goal,
        "experience": experience,
        "created_at": datetime.utcnow().isoformat(),
        "plan": generate_workout_plan(goal, experience)
    }

    if users_email not in workouts:
        workouts[user_email] = []


    workouts[user_email].append(workout)

    return workout

def get_workouts(user_email):
    return workouts.get(user_email, [])

#this is a hardcoded workout plan basic using NO ai

def generate_basic_plan(goal, experience):
    if goal == "cut":
        return ["Squats", "bench press", "Deadlifts", "cardio"]
    elif goal == "bulk":
        return ["Heavy Squats", "Bench press", "rows", "overhead press"]
    else:
        return["full body workout", "light cardio"]