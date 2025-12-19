from app.models import Budget, db
from app.dsa.queue import NotificationQueue

def set_budget(user_id, category_id, amount):
    budget = Budget.query.filter_by(user_id=user_id, category_id=category_id).first()
    if budget:
        budget.amount = amount
    else:
        budget = Budget(user_id=user_id, category_id=category_id, amount=amount)
        db.session.add(budget)
    db.session.commit()

def get_user_budgets(user_id):
    return Budget.query.filter_by(user_id=user_id).all()

def check_budget_alerts(user_id, category_totals):
    alerts = []
    queue = NotificationQueue()

    budgets = get_user_budgets(user_id)
    for budget in budgets:
        cname = budget.category.name
        spent = category_totals.get(cname, 0)
        if spent > budget.amount:
            msg = {'category': cname, 'spent': spent, 'limit': budget.amount}
            queue.enqueue(msg)

    while not queue.is_empty():
        alerts.append(queue.dequeue())

    return alerts
