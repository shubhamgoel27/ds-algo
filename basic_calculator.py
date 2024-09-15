class Solution:
    def calculate(self, s: str) -> int:
        """
        Evaluate a string expression containing basic arithmetic operations.

        This method supports addition, subtraction, multiplication, and division
        of non-negative integers. It handles spaces and follows standard operator precedence.

        Args:
            s (str): The input string expression.

        Returns:
            int: The result of the evaluated expression.

        Time complexity: O(n), where n is the length of the input string.
        Space complexity: O(n) in the worst case, where the expression consists of only additions.
        """
        stack = [0]  # Initialize stack with 0 to handle expressions starting with negative numbers
        pre_op = "+"
        curr_num = 0
        s += "+"  # Add a '+' at the end to process the last number

        for char in s:
            if char.isdigit():
                curr_num = curr_num * 10 + int(char)
            elif char in set(["+", "-", "*", "/", " "]):
                if char == " ":
                    continue  # Skip spaces
                
                # Process the previous operation
                if pre_op == "+":
                    stack.append(curr_num)
                elif pre_op == "-":
                    stack.append(-curr_num)
                elif pre_op == "*":
                    stack.append(stack.pop() * curr_num)
                elif pre_op == "/":
                    # Handle division by zero and negative numbers
                    prev_num = stack.pop()
                    if curr_num == 0:
                        raise ValueError("Division by zero")
                    stack.append(int(prev_num / curr_num))  # Use int() for consistent behavior
                
                pre_op = char 
                curr_num = 0

        return sum(stack)

# Test cases
def test_calculate():
    solution = Solution()
    
    assert solution.calculate("3+2*2") == 7
    assert solution.calculate(" 3/2 ") == 1
    assert solution.calculate(" 3+5 / 2 ") == 5
    assert solution.calculate("42") == 42
    assert solution.calculate("1-1+1") == 1
    assert solution.calculate("0-2147483647") == -2147483647
    
    print("All test cases passed!")

# Run the test cases
test_calculate()

# Broad hints for solving this problem:
# 1. Use a stack to keep track of numbers and handle operator precedence.
# 2. Process the input string character by character.
# 3. Use a variable to build multi-digit numbers.
# 4. Handle each operator separately, considering the previous operator, and apply BODMAS rules for immediate operations.
# 5. Be careful with edge cases like spaces, negative numbers, and division by zero.
# 6. Consider adding a dummy operator at the end to process the last number.
# 7. Remember that integer division in Python always rounds down for negative numbers.
