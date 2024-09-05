from typing import List
import heapq
from collections import defaultdict

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Find the k most frequent elements in the given list of numbers.

        Args:
            nums (List[int]): A list of integers.
            k (int): The number of most frequent elements to return.

        Returns:
            List[int]: A list containing the k most frequent elements.

        Time complexity: O(n log k), where n is the length of nums.
        Space complexity: O(n) for the dictionary and heap.
        """
        d: defaultdict[int, int] = defaultdict(int)
        for num in nums:
            d[num] += 1
        
        heap: List[tuple[int, int]] = []
        for key, value in d.items():
            heapq.heappush(heap, (value, key))
            if len(heap) > k:
                heapq.heappop(heap)
        
        return [item[1] for item in heap]

# Test cases
def test_topKFrequent():
    solution = Solution()
    
    # Test case 1
    assert set(solution.topKFrequent([1,1,1,2,2,3], 2)) == {1, 2}, "Test case 1 failed"
    
    # Test case 2
    assert solution.topKFrequent([1], 1) == [1], "Test case 2 failed"
    
    # Test case 3
    assert set(solution.topKFrequent([1,2,2,3,3,3], 2)) == {2, 3}, "Test case 3 failed"
    
    # Test case 4
    assert solution.topKFrequent([4,1,-1,2,-1,2,3], 2) == [-1, 2], "Test case 4 failed"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_topKFrequent()
