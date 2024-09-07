from collections import Counter

class Solution:
    def customSortString(self, order: str, s: str) -> str:
        """
        Customizes the order of characters in string s based on the order string.

        Args:
            order (str): A string defining the custom order of characters.
            s (str): The string to be sorted according to the custom order.

        Returns:
            str: A new string with characters from s sorted according to order.

        Example:
            >>> sol = Solution()
            >>> sol.customSortString("cba", "abcd")
            'cbad'
        """
        # Count occurrences of each character in s
        char_count = Counter(s)
        
        result = []
        
        # Add characters in the specified order
        for char in order:
            result.extend([char] * char_count.pop(char, 0))
        
        # Add remaining characters not in order
        for char, count in char_count.items():
            result.extend([char] * count)
        
        return "".join(result)

def check_custom_order(result: str, order: str, s: str) -> bool:
    """
    Check if the result string follows the custom order for the specified characters.
    """
    order_index = 0
    for char in result:
        if order_index < len(order) and char == order[order_index]:
            order_index += 1
    
    # Check if all characters from 'order' that are in 's' are in the correct order
    return order_index == len([c for c in order if c in s])

# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ("cba", "abcd"),
        ("cbafg", "abcd"),
        ("kqep", "pekeq"),
        ("hucw", "utzoampdgkalexslxoqfkdjoczajxtuhqyxvlfatmptqdsochtdzgypsfkgqwbgqbcamdqnqztaqhqanirikahtmalzqjjxtqfnh")
    ]
    
    for i, (order, s) in enumerate(test_cases, 1):
        result = sol.customSortString(order, s)
        is_correct = check_custom_order(result, order, s)
        print(f"Test case {i}:")
        print(f"Order: {order}")
        print(f"Input: {s}")
        print(f"Result: {result}")
        print(f"Correct order: {is_correct}")
        print(f"All characters present: {sorted(result) == sorted(s)}\n")
    
    print("All test cases completed.")
