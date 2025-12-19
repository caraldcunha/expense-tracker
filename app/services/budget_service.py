from app.models import Budget, db

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
    budgets = get_user_budgets(user_id)
    for budget in budgets:
        spent = category_totals.get(budget.category.name, 0)
        if spent > budget.amount:
            alerts.append({'category': budget.category.name, 'spent': spent, 'limit': budget.amount})
    return alerts

