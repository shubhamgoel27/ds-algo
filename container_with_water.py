from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """Most water between two vertical lines. O(n) time, O(1) space.

        Converging pointers. Area = width * min(left, right); the shorter wall
        caps the height. Moving the TALLER wall inward only loses width while
        the cap stays the same or drops, so it can never improve -> always move
        the SHORTER wall (the exchange argument that makes the greedy correct).
        """
        max_area = 0
        left, right = 0, len(height) - 1
        while left < right:
            width = right - left
            max_area = max(max_area, width * min(height[left], height[right]))
            if height[left] < height[right]:
                left += 1                    # left is the limiting (shorter) wall
            else:
                right -= 1                   # right is shorter-or-equal; ties are safe either way
        return max_area


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        ([2, 3, 4, 5, 18, 17, 6], 17),
    ]
    for height, expected in test_cases:
        result = solution.maxArea(height)
        assert result == expected, f"maxArea({height}) = {result}, expected {expected}"
    print("All tests passed.")
