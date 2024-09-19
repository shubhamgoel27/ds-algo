class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find the length of the longest substring without repeating characters.

        Args:
            s (str): The input string.

        Returns:
            int: The length of the longest substring without repeating characters.

        Time complexity: O(n), where n is the length of the string.
        Space complexity: O(min(m, n)), where m is the size of the character set.
        """
        d = {}  # Dictionary to store characters in the current window
        longest = 0
        i, j = 0, 0
        n = len(s)
        
        while i < n and j < n:
            if s[j] not in d:
                # Add new character to the window
                d[s[j]] = 1
                longest = max(longest, j - i + 1)
                j += 1
            else:
                # Remove characters from the start until the repeating character is gone
                while s[j] in d:
                    del d[s[i]]
                    i += 1
        return longest

# Test cases
def test_solution():
    sol = Solution()
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    assert sol.lengthOfLongestSubstring("pwwkew") == 3
    assert sol.lengthOfLongestSubstring("") == 0
    assert sol.lengthOfLongestSubstring("dvdf") == 3
    print("All test cases passed!")

test_solution()

# Hints for solving this problem:
# 1. Use two pointers (i and j) to represent the window of non-repeating characters.
# 2. Use a dictionary to keep track of characters in the current window.
# 3. Expand the window (j) when encountering new characters.
# 4. Contract the window (i) when encountering a repeating character.
# 5. Keep track of the maximum window size as you go.
# 6. Remember to handle edge cases like empty strings.
