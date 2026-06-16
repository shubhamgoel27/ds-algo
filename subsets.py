from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """All subsets (the power set) of distinct nums. O(n * 2^n).

        Backtracking / DFS over a decision tree. Every node of the tree is a
        valid subset, so we record at EVERY node, not just leaves. The `start`
        index means we only ever extend rightward, which is what prevents
        duplicate subsets ([1,2] but never [2,1]).
        """
        result = []

        def backtrack(start, path):
            result.append(path[:])                 # record a COPY (path keeps mutating)
            for i in range(start, len(nums)):
                path.append(nums[i])               # choose
                backtrack(i + 1, path)             # explore (i+1 = no reuse, no duplicates)
                path.pop()                         # un-choose (restore for the next sibling)

        backtrack(0, [])
        return result


if __name__ == "__main__":
    solution = Solution()

    def norm(subs):
        return sorted(sorted(s) for s in subs)

    assert norm(solution.subsets([1, 2, 3])) == norm(
        [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    )
    assert norm(solution.subsets([0])) == norm([[], [0]])
    assert len(solution.subsets([1, 2, 3, 4])) == 16      # 2^n subsets
    print("All tests passed.")
