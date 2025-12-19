class NotificationQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, message):
        self.queue.append(message)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def peek(self):
        return self.queue[0] if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

