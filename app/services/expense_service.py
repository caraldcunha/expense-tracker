from app.models import Transaction, db
from datetime import datetime

def add_expense(user_id, description, category, amount, date=None):
    txn = Transaction(
        user_id=user_id,
        description=description,
        category=category,
        amount=amount,
        date=date or datetime.utcnow()
    )
    db.session.add(txn)
    db.session.commit()

def get_user_transactions(user_id):
    return Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()

def delete_transaction(txn_id):
    txn = Transaction.query.get(txn_id)
    if txn:
        db.session.delete(txn)
        db.session.commit()

def update_transaction(txn_id, description, category, amount):
    txn = Transaction.query.get(txn_id)
    if txn:
        txn.description = description
        txn.category = category
        txn.amount = amount
        db.session.commit()

