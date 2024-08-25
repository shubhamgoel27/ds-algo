import heapq
from typing import List

class MedianOfStream:
    def __init__(self):
        # Min-heap for the larger half of the numbers
        self.minheap: List[int] = []
        # Max-heap (using negative values) for the smaller half of the numbers
        self.maxheap: List[int] = []

    def insert_num(self, num: int) -> None:
        if not self.maxheap or num <= -self.maxheap[0]:
            heapq.heappush(self.maxheap, -num)
        else:
            heapq.heappush(self.minheap, num)
        
        # Rebalance the heaps if necessary
        if len(self.maxheap) > len(self.minheap) + 1:
            heapq.heappush(self.minheap, -heapq.heappop(self.maxheap))
        elif len(self.minheap) > len(self.maxheap):
            heapq.heappush(self.maxheap, -heapq.heappop(self.minheap))

    def find_median(self) -> float:
        if len(self.maxheap) == len(self.minheap):
            return (-self.maxheap[0] + self.minheap[0]) / 2.0
        else:
            return float(-self.maxheap[0])

def run_median_tests():
    # Test case 1: Simple case with one element
    median_stream = MedianOfStream()
    median_stream.insert_num(1)
    assert median_stream.find_median() == 1.0, "Test case 1 failed"

    # Test case 2: Two elements
    median_stream.insert_num(5)
    assert median_stream.find_median() == 3.0, "Test case 2 failed"

    # Test case 3: Three elements
    median_stream.insert_num(3)
    assert median_stream.find_median() == 3.0, "Test case 3 failed"

    # Test case 4: Four elements
    median_stream.insert_num(8)
    assert median_stream.find_median() == 4.0, "Test case 4 failed"

    # Test case 5: Negative numbers
    median_stream = MedianOfStream()
    median_stream.insert_num(-3)
    median_stream.insert_num(-1)
    assert median_stream.find_median() == -2.0, "Test case 5 failed"
    median_stream.insert_num(-2)
    assert median_stream.find_median() == -2.0, "Test case 5 failed"

    # Test case 6: Mixed positive and negative numbers
    median_stream = MedianOfStream()
    median_stream.insert_num(-10)
    median_stream.insert_num(10)
    assert median_stream.find_median() == 0.0, "Test case 6 failed"
    median_stream.insert_num(0)
    assert median_stream.find_median() == 0.0, "Test case 6 failed"

    # Test case 7: Large number of elements
    median_stream = MedianOfStream()
    for num in range(1, 101):  # Insert numbers from 1 to 100
        median_stream.insert_num(num)
    assert median_stream.find_median() == 50.5, "Test case 7 failed"

    # Test case 8: Even number of elements
    median_stream = MedianOfStream()
    for num in [10, 20, 30, 40]:
        median_stream.insert_num(num)
    assert median_stream.find_median() == 25.0, "Test case 8 failed"

    # Test case 9: Odd number of elements
    median_stream = MedianOfStream()
    for num in [10, 20, 30, 40, 50]:
        median_stream.insert_num(num)
    assert median_stream.find_median() == 30.0, "Test case 9 failed"

    # Test case 10: All elements are the same
    median_stream = MedianOfStream()
    for _ in range(10):
        median_stream.insert_num(5)
    assert median_stream.find_median() == 5.0, "Test case 10 failed"

    print("All test cases passed!")

# Run the test cases
run_median_tests()
