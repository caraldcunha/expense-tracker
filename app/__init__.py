from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/expense_tracker.sqlite'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes, models
