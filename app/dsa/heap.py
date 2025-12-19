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

# ---- Generic MinHeap to satisfy tests ----
class MinHeap:
    def __init__(self):
        self._heap = []

    def insert(self, value):
        heapq.heappush(self._heap, value)

    def peek(self):
        if not self._heap:
            raise IndexError("peek from empty heap")
        return self._heap[0]

    def extract_min(self):
        if not self._heap:
            raise IndexError("extract_min from empty heap")
        return heapq.heappop(self._heap)

    def is_empty(self):
        return len(self._heap) == 0
