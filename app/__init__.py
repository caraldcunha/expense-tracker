from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/expense_tracker.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure instance folder exists
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'instance'), exist_ok=True)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import User  # import after db init

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes, models
