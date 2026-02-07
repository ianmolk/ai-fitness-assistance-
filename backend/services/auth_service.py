import jwt
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


#this is a temp storage
users = {}

SECRET_KEY = os.getenv("secret_key")
ALGORITHM = "HS256"
TOKEN_EXPIRY_MINUTES = 60



#REGISTER logic for user 
def register_user(email, password):
    if email in users:
        return {"error": "User already exists"}
    hashed_password = generate_password_hash(password)

    users[email] = {
        "email": email,
        "password" : hashed_password
    }

    return {"message": "User registered successfully"}


# this for the login of the users
def login_user(email, password):
    user = users.get(email)

    if not user:
        return {"error": "Invalid credentials"}
    
    if not check_password_hash(user["password"], password):
        return {"error" : "Invalid credentials"}
    
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "token": token,
        "message": "login sucessful"
    }