from app import app
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from app.models import Transaction, Category, db
from app.services import get_weekly_summary, check_budget_alerts

from app.services.wrapped_service import get_wrapped_insights


# ------------------ Static Pages ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("edit_expense.html")  # or login.html

@app.route("/signup")
def signup():
    return render_template("add_expense.html")  # or signup.html

# ------------------ Dashboard ------------------

@app.route("/dashboard")
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()

    # Weekly summary and budget alerts
    summary = get_weekly_summary(current_user.id)
    category_totals = summary['category_totals']
    budget_alerts = check_budget_alerts(current_user.id, category_totals)

    return render_template(
        "dashboard.html",
        transactions=transactions,
        budget_alerts=budget_alerts
    )

# ------------------ Category Management ------------------

@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        name = request.form['category_name']
        new_cat = Category(name=name, user_id=current_user.id)
        db.session.add(new_cat)
        db.session.commit()
        return redirect(url_for('manage_categories'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_categories.html', categories=categories)

@app.route('/delete_category/<int:id>')
def delete_category(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('manage_categories'))
    @app.route('/wrapped')
@login_required
def wrapped():
    insights = get_wrapped_insights(current_user.id)
    return render_template('wrapped.html', **insights)

