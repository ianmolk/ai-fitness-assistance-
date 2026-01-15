from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

# Simple in-memory database for now (will use SQLite later if needed)
users_db = {}

def hash_password(password: str):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "Missing token"}), 401
        
        try:
            token = token.split(" ")[1]  # Remove "Bearer "
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email not in users_db:
                return jsonify({"detail": "Invalid user"}), 401
        except:
            return jsonify({"detail": "Invalid token"}), 401
        
        return f(email, *args, **kwargs)
    return decorated

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Backend is running!", "message": "Connection successful"})

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"detail": "Email and password required"}), 400
    
    if email in users_db:
        return jsonify({"detail": "User already exists"}), 400
    
    users_db[email] = {
        "password": hash_password(password),
        "profile": None
    }
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"detail": "Email and password required"}), 400
    
    db_user = users_db.get(email)
    if not db_user or not verify_password(password, db_user["password"]):
        return jsonify({"detail": "Invalid credentials"}), 401
    
    token = create_token(email)
    return jsonify({"access_token": token, "token_type": "bearer"}), 200

@app.route("/user/profile", methods=["GET"])
@token_required
def get_profile(email):
    profile = users_db[email]["profile"]
    if not profile:
        return jsonify({"message": "Profile not set"}), 200
    return jsonify(profile), 200

@app.route("/user/profile", methods=["PUT"])
@token_required
def update_profile(email):
    data = request.json
    users_db[email]["profile"] = {
        "height": data.get("height"),
        "weight": data.get("weight"),
        "age": data.get("age"),
        "goal": data.get("goal")
    }
    return jsonify({"message": "Profile updated"}), 200

@app.route("/ai/chat", methods=["POST"])
@token_required
def ai_chat(email):
    data = request.json
    user_profile = users_db[email]["profile"]
    
    if not user_profile:
        return jsonify({"reply": "Please complete your profile first"}), 200
    
    goal = user_profile.get("goal")
    
    if goal == "cut":
        reply = "Focus on higher reps and calorie deficit"
    elif goal == "bulk":
        reply = "Progressive overload and calorie surplus"
    else:
        reply = "Tell me more about your fitness goal!"
    
    return jsonify({"reply": reply}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8001)






