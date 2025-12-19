class UndoStack:
    def __init__(self):
        self.stack = []

    def push_action(self, action_type, data):
        self.stack.append((action_type, data))  # e.g., ("add", transaction_data)

    def pop_action(self):
        if self.stack:
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

