from flask import Blueprint, request, jsonify
from utils.jwt_utils import token_requred
from services.workout_service import create_workout, get_workouts


workout_bp = Blueprint("workouts", __name__, url_prefix="/workouts")

@workout_bp.route("/", methods=["POST"])
@token_requred
def create(current_user):
    data = request.get_json()

    goal = data.get("goal")
    experience = data.get("experience")

    if not goal or not experience:
        return jsonify({"error": "missing workout information"}), 400
    
    return jsonify(create_workout(current_user, goal, experience)), 201

@workout_bp.route("/", methods=["GET"])
@token_requred
def get_all(current_user):
    return jsonify(get_workouts(current_user)), 200

