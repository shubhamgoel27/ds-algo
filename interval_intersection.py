from typing import List

class Solution:
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        final = []
        if not firstList:
            return []
        if not secondList:
            return []
        m, n = len(firstList), len(secondList)
        i,j = 0, 0 
        while i<m and j<n:
            first_start, first_end = firstList[i]
            second_start, second_end = secondList[j]
            if first_start <= second_end and first_end >= second_start:
                interval = [max(first_start, second_start), min(first_end, second_end)]
                final.append(interval)

            if first_end < second_end:
                i+=1
            else:
                j+=1

        return final 



def test_interval_intersection():
    solution = Solution()

    test_cases = [
        (
            [[0, 2], [5, 10], [13, 23], [24, 25]],
            [[1, 5], [8, 12], [15, 24], [25, 26]],
            [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
        ),
        (
            [[1, 3], [5, 9]],
            [[4, 5], [7, 10]],
            [[5, 5], [7, 9]]
        ),
        (
            [[1, 2], [5, 6]],
            [[3, 4], [7, 8]],
            []
        ),
        (
            [],
            [[1, 5], [8, 12], [15, 24], [25, 26]],
            []
        ),
        (
            [[1, 5], [8, 12], [15, 24], [25, 26]],
            [],
            []
        ),
        (
            [[1, 5], [10, 14]],
            [[1, 5], [10, 14]],
            [[1, 5], [10, 14]]
        ),
        (
            [[1, 10]],
            [[2, 3], [4, 5], [6, 7]],
            [[2, 3], [4, 5], [6, 7]]
        )
    ]

    for i, (firstList, secondList, expected) in enumerate(test_cases):
        result = solution.intervalIntersection(firstList, secondList)
        assert result == expected, f"Test case {i+1} failed: expected {expected}, got {result}"
        print(f"Test case {i+1} passed")

if __name__ == "__main__":
    test_interval_intersection()