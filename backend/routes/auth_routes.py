from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


#this is for registering the user.
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400
    
    result = register_user(email, password)
    return jsonify(result), 201


#this is for the login of the user 
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    result = login_user(email, password)
    return jsonify(result), 200
