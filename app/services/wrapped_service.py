from datetime import datetime, timedelta
from collections import defaultdict

def get_weekly_summary(user_id):
    from app.models import Transaction
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    txns = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()

    category_totals = defaultdict(float)
    total = 0
    for txn in txns:
        category_totals[txn.category] += txn.amount
        total += txn.amount

    return {
        'total': total,
        'category_totals': dict(category_totals)
    }

