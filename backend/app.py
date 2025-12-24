from fastapi import FastAPI, HTTPException, Depends
from fastapi.secuirty import OAuth2passwordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os 
from datetime import datetime, timedelta 
from pydantic import BaseModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = FastAPI()

oauth3_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context - CryptContext(schemes=["bcrypt"], deprecated="auto")


users_db = {}

class UserAuth(BaseModel):
    email: str
    password: str 


class UserProfile(BaseModel):
    height: float
    weight: float 
    age: int
    goal: str 


def hash_password(Password: str):
    return pwd_context.verify(password, hashed)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid user")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@app.post("/auth/register")
def register(user: UserAuth):
    if user.email in users.db:
        raise HTTPException(status_code=400, detail="user exists")


    users_db[user.email] = {
        "password": hash_password(user.password),
        "profile": None
    }

    return {"message": "User registered"}


@app.post("/auth/login")
def login(user: UserAuth):
    db_user = users_db.get(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, details="Invalid credentials")
    
    token = create_token(user.email)
    return {"access_token": token}


@app.get("/user/profile")
def get_profile(email:str = Depends(get_current_user)):
    return users_db[email]["profile"]

@app.put("/user/profile")
def update_profile(profile: UserProfile, email: str = Depends(get_current_user)):
    users_db[email]["profile"] = profile
    return {"message": "Profile updated"}



@app.post("/ai/chat")
def ai_chat(messages: dict, email: str = Depends(get_current_user)):
    user_profile = users_db[email]["profile"]

    if not user_profile:
        return {"reply": "please complete ur rego first"}
    
    goal = user_profile.goal

    if goal == "cut":
        reply = "focus on higher reps and calorie deficit"
    elif goal == "bulk":
        reply = "Progressive overload and calorie surplus"
    else:
        reply = "Train consistentlhy and revoer well"





