from typing import List 

class Solution:

    def findPeakElement(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:

            mid = (left+right)//2
            if nums[mid] < nums[mid+1]:
                left = mid + 1 
            else:
                right = mid 
        
        return left
    
def test_findPeakElement():
    # Test case 1: Single peak in the middle
    solution = Solution()
    nums1 = [1, 2, 3, 1]
    assert solution.findPeakElement(nums1) == 2  # The peak element is at index 2 (value 3)
    
    # Test case 2: Multiple peaks
    nums2 = [1, 2, 1, 3, 5, 6, 4]
    peak2 = solution.findPeakElement(nums2)
    assert peak2 in [1, 5]  # The peak elements are at index 1 (value 2) or index 5 (value 6)
    
    # Test case 3: Ascending order
    nums3 = [1, 2, 3, 4, 5]
    assert solution.findPeakElement(nums3) == 4  # The peak element is at index 4 (value 5)
    
    # Test case 4: Descending order
    nums4 = [5, 4, 3, 2, 1]
    assert solution.findPeakElement(nums4) == 0  # The peak element is at index 0 (value 5)
    
    # Test case 5: Peak at the start
    nums5 = [10, 2, 1]
    assert solution.findPeakElement(nums5) == 0  # The peak element is at index 0 (value 10)
    
    # Test case 6: Peak at the end
    nums6 = [1, 2, 10]
    assert solution.findPeakElement(nums6) == 2  # The peak element is at index 2 (value 10)
    
    # Test case 7: Two elements
    nums7 = [2, 1]
    assert solution.findPeakElement(nums7) == 0  # The peak element is at index 0 (value 2)
    
    nums8 = [1, 2]
    assert solution.findPeakElement(nums8) == 1  # The peak element is at index 1 (value 2)
    
    # Test case 8: Single element
    nums9 = [1]
    assert solution.findPeakElement(nums9) == 0  # The peak element is at index 0 (value 1)
    
    # Test case 9: Flat peak
    nums10 = [1, 1, 1, 1, 1]
    peak10 = solution.findPeakElement(nums10)
    assert peak10 in [0, 1, 2, 3, 4]  # Any index is valid because all elements are the same
    
    print("All test cases pass")

# Run the tests
test_findPeakElement()