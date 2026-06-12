from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """Two numbers in a SORTED array summing to target, 1-based indices. O(n) / O(1).

        Converging pointers. If the pair sums too low, the left value paired with
        the largest available (right) is still short, so left can never reach
        target with any smaller partner -> advance left, never revisit. Too high
        -> retreat right. Sortedness is what replaces the hash map's O(n) space.
        """
        left, right = 0, len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]     # 1-based
            if total > target:
                right -= 1                        # sum too big, shrink it
            else:
                left += 1                         # sum too small, grow it
        return []                                 # defensive (problem guarantees a solution)


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([2, 7, 11, 15], 9, [1, 2]),
        ([2, 3, 4], 6, [1, 3]),
        ([-1, 0], -1, [1, 2]),
        ([1, 2, 3, 4, 4, 9, 56, 90], 8, [4, 5]),
        ([5, 25, 75], 100, [2, 3]),
    ]
    for numbers, target, expected in test_cases:
        result = solution.twoSum(numbers, target)
        assert result == expected, f"twoSum({numbers}, {target}) = {result}, expected {expected}"
    print("All tests passed.")
