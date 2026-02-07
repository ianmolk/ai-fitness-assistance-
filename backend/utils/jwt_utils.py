import jwt
import os
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def token_requred(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorisation")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401
        

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_user = payload["email"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "expired token"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated