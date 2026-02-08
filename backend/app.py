from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from database import db
from routes.auth_routes import auth_bp
from routes.workout_routes import workout_bp
from routes.chat_routes import chat_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Basic config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fitness.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Extensions
    CORS(app)
    db.init_app(app)

    # Routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(chat_bp)

    return app


app = create_app()

# Create DB tables (TEMP – dev only)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8001)
