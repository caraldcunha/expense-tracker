import heapq

class WeeklyWrapped:
    def __init__(self):
        self.category_totals = {}

    def add_expense(self, category, amount):
        if category not in self.category_totals:
            self.category_totals[category] = 0
        self.category_totals[category] += amount

    def get_top_categories(self, n=3):
        heap = [(-amount, cat) for cat, amount in self.category_totals.items()]
        heapq.heapify(heap)
        return [(cat, -amount) for amount, cat in heapq.nsmallest(n, heap)]
