# test/test_linked_list.py

import pytest
from dsa.linked_list import LinkedList

def test_insert_and_traverse():
    ll = LinkedList()
    ll.insert(10)
    ll.insert(20)
    ll.insert(30)
    assert ll.traverse() == [10, 20, 30]

def test_delete_existing_node():
    ll = LinkedList()
    ll.insert(1)
    ll.insert(2)
    ll.insert(3)
    ll.delete(2)
    assert ll.traverse() == [1, 3]

def test_delete_nonexistent_node():
    ll = LinkedList()
    ll.insert(5)
    ll.insert(6)
    ll.delete(10)  # Should not crash
    assert ll.traverse() == [5, 6]

def test_empty_list_traverse():
    ll = LinkedList()
    assert ll.traverse() == []


