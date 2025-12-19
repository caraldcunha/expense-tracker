class TransactionNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class TransactionList:
    def __init__(self):
        self.head = None

    def add_transaction(self, data):
        new_node = TransactionNode(data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node

    def delete_transaction(self, description):
        curr = self.head
        prev = None
        while curr:
            if curr.data.get('description') == description:
                if prev: prev.next = curr.next
                else: self.head = curr.next
                return True
            prev = curr
            curr = curr.next
        return False

    def list_transactions(self):
        result, curr = [], self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

# ---- Generic LinkedList to satisfy tests ----
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node

    def delete(self, value):
        curr = self.head
        prev = None
        while curr:
            if curr.value == value:
                if prev: prev.next = curr.next
                else: self.head = curr.next
                return True
            prev = curr
            curr = curr.next
        return False

    def traverse(self):
        out, curr = [], self.head
        while curr:
            out.append(curr.value)
            curr = curr.next
        return out
