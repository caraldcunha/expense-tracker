# test/test_stack.py

import pytest
from dsa.stack import Stack

def test_push_and_peek():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.peek() == 2

def test_pop():
    stack = Stack()
    stack.push('a')
    stack.push('b')
    assert stack.pop() == 'b'
    assert stack.pop() == 'a'

def test_empty_pop():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_is_empty():
    stack = Stack()
    assert stack.is_empty()
    stack.push(42)
    assert not stack.is_empty()


