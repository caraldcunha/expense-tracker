from datetime import datetime, timedelta
from app.models import Transaction, Category
from app.dsa.hash_map import CategoryMap
from app.dsa.heap import WeeklyWrapped

def get_weekly_summary(user_id):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    txns = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()

    cmap = CategoryMap()
    total = 0.0

    for txn in txns:
        # txn.category is a Category object; use its name
        cname = txn.category.name if isinstance(txn.category, Category) else txn.category
        cmap.add_expense(cname, txn.amount)
        total += txn.amount

    return {
        'total': total,
        'category_totals': cmap.get_all_categories()
    }

def get_wrapped_insights(user_id):
    end = datetime.utcnow()
    start = end - timedelta(days=7)

    txns = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start,
        Transaction.date <= end
    ).all()

    total = sum(t.amount for t in txns)
    ww = WeeklyWrapped()

    for t in txns:
        cname = t.category.name if isinstance(t.category, Category) else t.category
        ww.add_expense(cname, t.amount)

    top_categories = ww.get_top_categories(n=3)
    top_category = top_categories[0] if top_categories else ("None", 0)

    most_spent = max(txns, key=lambda t: t.amount, default=None)

    # Day of week counts
    from collections import Counter
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
