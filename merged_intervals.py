from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])
        merged_intervals = [intervals[0]]

        for curr_start, curr_end in intervals[1:]:
            prev_start, prev_end = merged_intervals[-1]
            if prev_end >= curr_start:
                merged_intervals[-1][1] = max(prev_end, curr_end)
            else:
                merged_intervals.append([curr_start, curr_end])

        return merged_intervals

# Test cases
if __name__ == "__main__":
    solution = Solution()
    
    test_cases = [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[1, 4], [2, 3]], [[1, 4]]),
        ([[1, 4], [0, 4]], [[0, 4]]),
        ([[1, 4], [0, 1]], [[0, 4]]),
        ([], []),
        ([[1, 4]], [[1, 4]])
    ]
    
    for intervals, expected in test_cases:
        result = solution.merge(intervals)
        assert result == expected, f"Test failed for input {intervals}. Expected {expected}, got {result}"
    
    print("All tests passed.")
