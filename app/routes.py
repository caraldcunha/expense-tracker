from app import app
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("edit_expense.html")  # or login.html if you have it

@app.route("/signup")
def signup():
    return render_template("add_expense.html")  # or signup.html if you have it
