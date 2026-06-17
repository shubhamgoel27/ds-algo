from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """All permutations of distinct nums. O(n * n!).

        Backtracking. Two knobs differ from Subsets:
          - record only at LEAVES (a permutation must use every number), and
          - choices are "any UNUSED element" (no start index), because order
            matters and we want both [1,2] and [2,1].
        `path` (list) carries the order and is what we record; `used` (set) is a
        fast-membership companion. They move in lockstep: add on choose, remove
        on un-choose.
        """
        result = []
        path = []
        used = set()

        def backtrack():
            if len(path) == len(nums):
                result.append(path[:])           # record the ordered list
                return
            for num in nums:
                if num in used:                  # O(1) instead of scanning path
                    continue
                path.append(num)
                used.add(num)
                backtrack()
                path.pop()                       # un-choose: restore both
                used.remove(num)

        backtrack()
        return result


if __name__ == "__main__":
    from itertools import permutations as iperm

    solution = Solution()

    def norm(p):
        return sorted(tuple(x) for x in p)

    for nums in ([1, 2, 3], [0, 1], [1], [5, 4, 6, 2]):
        got = solution.permute(nums[:])
        assert norm(got) == norm([list(p) for p in iperm(nums)]), f"{nums}"
        assert len(got) == len(set(map(tuple, got))), f"duplicates for {nums}"
    print("All tests passed.")
