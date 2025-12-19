# test/test_heap.py

import pytest
from dsa.heap import MinHeap  # or MaxHeap, depending on your implementation

def test_insert_and_peek():
    heap = MinHeap()
    heap.insert(10)
    heap.insert(5)
    heap.insert(20)
    assert heap.peek() == 5

def test_extract_min():
    heap = MinHeap()
    heap.insert(15)
    heap.insert(3)
    heap.insert(8)
    assert heap.extract_min() == 3
    assert heap.extract_min() == 8
    assert heap.extract_min() == 15

def test_empty_extract():
    heap = MinHeap()
    with pytest.raises(IndexError):
        heap.extract_min()


