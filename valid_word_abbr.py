class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        """
        Validate if the given abbreviation is valid for the word.

        Args:
        word (str): The original word.
        abbr (str): The abbreviation to validate.

        Returns:
        bool: True if the abbreviation is valid, False otherwise.
        """
        i = 0  # Pointer for word
        j = 0  # Pointer for abbr
        n = len(word)
        m = len(abbr)

        while i < n and j < m:
            if abbr[j].isalpha():
                # Match the character
                if word[i] != abbr[j]:
                    return False
                i += 1
                j += 1
            else:
                # Handle numeric abbreviation
                num = 0
                if abbr[j] == "0":
                    # Leading zeros are not allowed
                    return False 
                else:
                    # Parse the number in the abbreviation
                    while j < m and abbr[j].isnumeric():
                        num = num * 10 + int(abbr[j])
                        j += 1
                i += num  # Skip 'num' characters in the word

        # Check if both pointers have reached the end
        return i == n and j == m

# Test cases
def test_valid_word_abbr():
    solution = Solution()
    
    # Test case 1: Valid abbreviation
    assert solution.validWordAbbreviation("internationalization", "i12iz4n") == True
    
    # Test case 2: Invalid abbreviation (character mismatch)
    assert solution.validWordAbbreviation("apple", "a2e") == False
    
    # Test case 3: Invalid abbreviation (leading zero)
    assert solution.validWordAbbreviation("internationalization", "i0n") == False
    
    # Test case 4: Valid abbreviation (no numeric part)
    assert solution.validWordAbbreviation("hi", "hi") == True
    
    # Test case 5: Invalid abbreviation (exceeds word length)
    assert solution.validWordAbbreviation("hi", "hi2") == False
    
    print("All test cases passed!")

# Run the test cases
test_valid_word_abbr()
