from typing import List
from collections import Counter

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        """
        Find all start indices of anagrams of p in s.

        Args:
            s (str): The string to search in.
            p (str): The string to find anagrams of.

        Returns:
            List[int]: A list of start indices of anagrams of p in s.

        Time complexity: O(n), where n is the length of s.
        Space complexity: O(1), as the Counter size is limited by the alphabet size.
        """
        if len(p) > len(s):
            return []  # Edge case: if p is longer than s, no anagrams are possible

        # Initialize the frequency counters for p and the sliding window in s
        p_count = Counter(p)
        s_count = Counter()

        result = []
        k = len(p)  # Length of the anagram we are looking for
        
        # First, populate the sliding window with the first k characters of s
        for i in range(k):
            s_count[s[i]] += 1

        # Check if the first window is an anagram
        if s_count == p_count:
            result.append(0)

        # Now slide the window across the rest of the string s
        for i in range(k, len(s)):
            # Add the new character to the window
            s_count[s[i]] += 1
            # Remove the old character from the window
            s_count[s[i - k]] -= 1

            # If the count of the old character is 0, remove it from the Counter
            if s_count[s[i - k]] == 0:
                del s_count[s[i - k]]
            
            # Check if the current window is an anagram
            if s_count == p_count:
                result.append(i - k + 1)

        return result

# Test cases
def test_findAnagrams():
    solution = Solution()
    
    # Test case 1: Normal case
    assert solution.findAnagrams("cbaebabacd", "abc") == [0, 6]
    
    # Test case 2: No anagrams
    assert solution.findAnagrams("abab", "cd") == []
    
    # Test case 3: Multiple overlapping anagrams
    assert solution.findAnagrams("abacbabc", "abc") == [1, 2, 3, 5]
    
    # Test case 4: Empty string s
    assert solution.findAnagrams("", "a") == []
    
    # Test case 5: Empty string p
    assert solution.findAnagrams("abc", "qcf") == []
    
    print("All test cases passed!")

# Run the tests
test_findAnagrams()

"""
Hints for future self (6 months from now):

1. Sliding Window Technique:
   - This problem is a perfect candidate for the sliding window approach.
   - Maintain a window of size len(p) and slide it across s.

2. Character Frequency:
   - Use Counter or a dictionary to keep track of character frequencies.
   - Compare the frequency of characters in the current window with p.

3. Optimization:
   - Instead of creating a new Counter for each window, update the existing one.
   - Add the new character and remove the old one in each step.

4. Edge Cases:
   - Remember to handle cases where len(p) > len(s).
   - Consider empty strings for both s and p.

5. Time Complexity:
   - Aim for O(n) time complexity, where n is the length of s.
   - Avoid nested loops that might lead to O(n^2) complexity.

6. Space Complexity:
   - Try to use O(1) extra space, as the Counter size is limited by the alphabet size.

7. Testing:
   - Include various test cases to cover different scenarios.
   - Test with large inputs to ensure efficiency.

Remember: The key is to efficiently update and compare character frequencies
as you slide the window across the string.
"""