from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Merge two sorted arrays in-place.

        This function merges nums2 into nums1. The first m elements of nums1 are to be merged with nums2.
        nums1 has a total length of m + n, where the last n elements are set to 0 and should be ignored.
        nums2 has a length of n.

        Args:
        nums1 (List[int]): The first sorted array with additional space at the end.
        m (int): The number of elements in nums1 to be merged.
        nums2 (List[int]): The second sorted array to be merged into nums1.
        n (int): The number of elements in nums2.

        Returns:
        None: The function modifies nums1 in-place and doesn't return anything.
        """
        # Start from the end of the arrays
        k = m + n - 1
        i, j = m - 1, n - 1

        while j >= 0:  # We only need to continue while there are elements in nums2
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1

# Test cases
def test_merge():
    solution = Solution()

    # Test case 1: Basic merge
    nums1 = [1, 2, 3, 0, 0, 0]
    solution.merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6], f"Test case 1 failed: {nums1}"

    # Test case 2: One empty array
    nums1 = [1]
    solution.merge(nums1, 1, [], 0)
    assert nums1 == [1], f"Test case 2 failed: {nums1}"

    # Test case 3: Both arrays non-empty, no overlap
    nums1 = [4, 5, 6, 0, 0, 0]
    solution.merge(nums1, 3, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6], f"Test case 3 failed: {nums1}"

    # Test case 4: Arrays with duplicate elements
    nums1 = [1, 2, 2, 0, 0, 0]
    solution.merge(nums1, 3, [2, 2, 3], 3)
    assert nums1 == [1, 2, 2, 2, 2, 3], f"Test case 4 failed: {nums1}"

    print("All test cases passed!")

# Run the tests
if __name__ == "__main__":
    test_merge()
