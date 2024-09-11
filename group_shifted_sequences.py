from collections import defaultdict
from typing import List

class Solution:
    """
    A class to group strings that belong to the same shifting sequence.
    """

    def get_sequence(self, string: str) -> str:
        """
        Generate a unique sequence identifier for a given string.

        Args:
            string (str): The input string.

        Returns:
            str: A comma-separated string of differences between adjacent characters.
        """
        if len(string) == 1:
            return "-1"  # Special case for single-character strings
        
        seq = []
        for i in range(1, len(string)):
            # Calculate the difference between adjacent characters (circular)
            diff = (ord(string[i]) - ord(string[i-1]) + 26) % 26
            seq.append(str(diff))
        
        return ",".join(seq)

    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        """
        Group strings that belong to the same shifting sequence.

        Args:
            strings (List[str]): A list of strings to be grouped.

        Returns:
            List[List[str]]: A list of groups, where each group is a list of strings
            that belong to the same shifting sequence.
        """
        seq_dict = defaultdict(list)
        
        # Group strings by their sequence identifier
        for s in strings:
            seq = self.get_sequence(s)
            seq_dict[seq].append(s)
        
        # Convert the dictionary values to a list of lists
        return list(seq_dict.values())

# Test cases
def test_solution():
    sol = Solution()
    
    # Test case 1: Basic grouping
    assert sol.groupStrings(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]) == [
        ["abc","bcd","xyz"],
        ["acef"],
        ["az","ba"],
        ["a","z"]
    ]
    
    # Test case 2: Empty input
    assert sol.groupStrings([]) == []
    
    # Test case 3: All single-character strings
    assert sol.groupStrings(["a", "b", "c"]) == [["a", "b", "c"]]
    
    print("All test cases passed!")

# Run the test cases
test_solution()

"""
Hints for solving this problem:

1. The key insight is to find a way to represent strings in the same shifting sequence
   with a unique identifier.

2. Consider the differences between adjacent characters instead of the absolute values.
   This makes the representation shift-invariant.

3. Use modular arithmetic to handle wraparound cases (e.g., 'z' to 'a').

4. Single-character strings are a special case and should be handled separately.

5. Use a hash map (dictionary) to group strings with the same sequence identifier.

6. Time complexity: O(N * K), where N is the number of strings and K is the average
   length of the strings.

7. Space complexity: O(N * K) to store the grouped strings.

Remember to handle edge cases like empty inputs and single-character strings!
"""
