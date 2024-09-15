class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        """
        Remove the minimum number of parentheses to make the input string valid.
        
        Args:
        s (str): Input string containing parentheses and other characters.
        
        Returns:
        str: The string after removing invalid parentheses.
        
        Time complexity: O(n), where n is the length of the input string.
        Space complexity: O(n) in the worst case.
        """
        # Stack to keep track of indices of unmatched opening parentheses
        incorrect_openings = []
        # List to store indices of unmatched closing parentheses
        incorrect_closings = []
        
        # Iterate through the string, identifying mismatched parentheses
        for i, char in enumerate(s):
            if char not in ("(", ")"):
                continue 
            if char == "(":
                incorrect_openings.append(i)
            elif char == ")":
                if not incorrect_openings:
                    incorrect_closings.append(i)
                else:
                    incorrect_openings.pop()
        
        # Combine all indices of parentheses to be removed
        all_incorrect = set(incorrect_openings + incorrect_closings)
        
        # Construct the final string, excluding characters at incorrect indices
        final = "".join(char for i, char in enumerate(s) if i not in all_incorrect)
        return final 

# Test cases
def test_solution():
    sol = Solution()
    assert sol.minRemoveToMakeValid("lee(t(c)o)de)") == "lee(t(c)o)de"
    assert sol.minRemoveToMakeValid("a)b(c)d") == "ab(c)d"
    assert sol.minRemoveToMakeValid("))((") == ""
    assert sol.minRemoveToMakeValid("(a(b(c)d)") == "a(b(c)d)"
    print("All test cases passed!")

test_solution()

# Hints for future self:
# 1. Use a stack-like approach to match parentheses.
# 2. Keep track of indices, not just the characters themselves.
# 3. Process the string in one pass to identify mismatched parentheses.
# 4. Use a set for efficient lookup when reconstructing the final string.
# 5. Remember to handle both unmatched opening and closing parentheses.