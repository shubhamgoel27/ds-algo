from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)
        read, write = 0, 0
        while read < n:
            if nums[read] == nums[write]:
                read += 1
            else:
                write += 1
                nums[write] = nums[read]
        return write + 1
