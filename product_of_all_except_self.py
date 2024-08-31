from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Calculate the product of all elements in the list except self.

        For each index i, compute the product of all numbers in the list except nums[i].

        Args:
        nums (List[int]): A list of integers.

        Returns:
        List[int]: A list where each element at index i is the product of all numbers in nums except nums[i].

        Time complexity: O(n)
        Space complexity: O(n)
        """
        left_prod = []
        right_prod = [0]*len(nums)
        n = len(nums)
        curr_prod = 1
        for i in range(n):
            curr_prod = curr_prod*nums[i]
            left_prod.append(curr_prod)
        curr_prod = 1
        for i in range(n-1, -1, -1):
            curr_prod = curr_prod*nums[i]
            right_prod[i] = curr_prod
        final = [0]*n
        print(left_prod, right_prod)
        final[0] = right_prod[1]
        final[n-1] = left_prod[n-2]
        for i in range(1,n-1):
            final[i] = left_prod[i-1]*right_prod[i+1]

        #solution that uses no extra space 
        # n = len(nums)
        # left_prod = [1]*n
        # right_cum = 1
        # for i in range(0, n-1):
        #     left_prod[i+1] = nums[i]*left_prod[i]
           
        # for i in range(n-1,-1,-1):
        #     left_prod[i] = right_cum*left_prod[i]
        #     right_cum = right_cum*nums[i]
        return final 

# Test cases
def test_productExceptSelf():
    sol = Solution()
    assert sol.productExceptSelf([1,2,3,4]) == [24,12,8,6]
    assert sol.productExceptSelf([1,2]) == [2,1]
    assert sol.productExceptSelf([-1,1,0,-3,3]) == [0,0,9,0,0]
    print("All test cases passed!")

test_productExceptSelf()

