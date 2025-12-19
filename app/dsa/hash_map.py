class CategoryMap:
    def __init__(self):
        self.map = {}

    def add_expense(self, category, amount):
        if category not in self.map:
            self.map[category] = 0
        self.map[category] += amount

    def get_total_by_category(self, category):
        return self.map.get(category, 0)

    def get_all_categories(self):
        return self.map

