from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.dsa.stack import UndoStack  
undo_stack = UndoStack() 
from app.models import Transaction, Category, User
from app.services.wrapped_service import get_wrapped_insights, get_weekly_summary
from app.services.budget_service import check_budget_alerts

# ------------------ Static Pages ------------------

@app.route("/")
def home():
    # Index uses frontend JS for charts and table; add welcome text in template
    return render_template("index.html")

# ------------------ Auth ------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials. Please try again.", "error")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("signup.html")

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Account already exists. Please log in.", "error")
            return redirect(url_for('login'))

        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ------------------ Dashboard ------------------

@app.route("/dashboard")
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    summary = get_weekly_summary(current_user.id)  # uses CategoryMap
    category_totals = summary['category_totals']
    budget_alerts = check_budget_alerts(current_user.id, category_totals)
    return render_template("dashboard.html", transactions=transactions, budget_alerts=budget_alerts)

# ------------------ Category Management ------------------

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if request.method == 'POST':
        name = request.form['category_name'].strip()
        if name:
            new_cat = Category(name=name, user_id=current_user.id)
            db.session.add(new_cat)
            db.session.commit()
        return redirect(url_for('manage_categories'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_categories.html', categories=categories)

@app.route('/delete_category/<int:id>')
@login_required
def delete_category(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('manage_categories'))

# ------------------ Wrapped ------------------

@app.route('/wrapped')
@login_required
def wrapped():
    insights = get_wrapped_insights(current_user.id)  # uses heap
    return render_template('wrapped.html', **insights)
    # ------------------ Edit Transaction ------------------

@app.route('/edit_transaction/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    txn = Transaction.query.get_or_404(id)

    if txn.user_id != current_user.id:
        flash("You are not authorized to edit this transaction.", "error")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Save previous state before editing
        previous_data = {
            'id': txn.id,
            'date': txn.date,
            'description': txn.description,
            'amount': txn.amount,
            'category_id': txn.category_id,
            'user_id': txn.user_id
        }
        undo_stack.push_action("edit", previous_data)

        # Apply new changes
        txn.date = request.form['date']
        txn.description = request.form['description']
        txn.amount = float(request.form['amount'])
        txn.category_id = int(request.form['category'])
        db.session.commit()
        flash("Transaction updated successfully! You can undo this.", "success")
        return redirect(url_for('dashboard'))

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('edit_transaction.html', txn=txn, categories=categories)
    # ------------------ Delete Transaction ------------------

@app.route('/delete_transaction/<int:id>')
@login_required
def delete_transaction(id):
    txn = Transaction.query.get_or_404(id)
    if txn.user_id != current_user.id:
        flash("Unauthorized", "error")
        return redirect(url_for('dashboard'))

    # Save transaction data before deleting
    undo_stack.push_action("delete", {
        'id': txn.id,
        'date': txn.date,
        'description': txn.description,
        'amount': txn.amount,
        'category_id': txn.category_id,
        'user_id': txn.user_id
    })

    db.session.delete(txn)
    db.session.commit()
    flash("Transaction deleted. You can undo this.", "info")
    return redirect(url_for('dashboard'))
    # ------------------ Undo Last Action ------------------

@app.route('/undo')
@login_required
def undo():
    if undo_stack.is_empty():
        flash("Nothing to undo.", "warning")
        return redirect(url_for('dashboard'))

    action_type, data = undo_stack.pop_action()

    if action_type == "delete":
        restored = Transaction(
            id=data['id'],
            date=data['date'],
            description=data['description'],
            amount=data['amount'],
            category_id=data['category_id'],
            user_id=data['user_id']
        )
        db.session.add(restored)
        db.session.commit()
        flash("Undo successful. Transaction restored.", "success")

    elif action_type == "edit":
        txn = Transaction.query.get(data['id'])
        if txn and txn.user_id == current_user.id:
            txn.date = data['date']
            txn.description = data['description']
            txn.amount = data['amount']
            txn.category_id = data['category_id']
            db.session.commit()
            flash("Undo successful. Transaction reverted to previous state.", "success")
        else:
            flash("Unable to undo edit. Transaction not found or unauthorized.", "error")

    return redirect(url_for('dashboard'))




