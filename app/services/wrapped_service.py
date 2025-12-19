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
def get_wrapped_insights(user_id):
    from app.models import Transaction
    from collections import Counter

    end = datetime.utcnow()
    start = end - timedelta(days=7)

    txns = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start,
        Transaction.date <= end
    ).all()

    total = sum(t.amount for t in txns)
    category_counter = Counter(t.category for t in txns)
    top_category = category_counter.most_common(1)[0] if category_counter else ("None", 0)
    most_spent = max(txns, key=lambda t: t.amount, default=None)
    day_counter = Counter(t.date.strftime('%A') for t in txns)
    top_day = day_counter.most_common(1)[0] if day_counter else ("None", 0)

    return {
        "total": total,
        "transaction_count": len(txns),
        "top_category": top_category,
        "biggest_splurge": most_spent,
        "top_day": top_day,
        "start": start,
        "end": end
    }

