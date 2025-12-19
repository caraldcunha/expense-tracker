class UndoStack:
    def __init__(self):
        self.stack = []

    def push_action(self, action_type, data):
        self.stack.append((action_type, data))

    def pop_action(self):
        if self.stack:
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

# ---- Generic Stack to satisfy tests ----
class Stack:
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()

    def peek(self):
        if not self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[-1]

    def is_empty(self):
        return len(self._stack) == 0
