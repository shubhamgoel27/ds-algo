class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum element in constant time.

    This implementation uses two internal stacks: one for storing all elements and another
    for keeping track of the minimum values at each level of the main stack.

    Time Complexity: O(1) for all operations (push, pop, top, getMin)
    Space Complexity: O(n) where n is the number of elements in the stack
    """

    def __init__(self):
        """Initialize the MinStack with two lists: one for the stack and one for the minimums."""
        self.min_stack = []  # Stack to keep track of minimum values at each level
        self.main_stack = []  # Main stack to store all values

    def push(self, val: int) -> None:
        """
        Push a new value onto the stack and update the minimum stack.

        Args:
            val (int): The value to be pushed onto the stack.
        """
        self.main_stack.append(val)
        
        # Update min_stack: push val if it's the first element or smaller/equal to current min
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
        else:
            self.min_stack.append(self.min_stack[-1])

    def pop(self) -> None:
        """
        Remove the top element from the stack and the corresponding minimum.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self.main_stack:
            raise IndexError("pop from empty stack")
        
        self.main_stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        """
        Return the top element of the stack.

        Returns:
            int: The top element of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self.main_stack:
            raise IndexError("top from empty stack")
        return self.main_stack[-1]

    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack.

        Returns:
            int: The minimum element in the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self.min_stack:
            raise IndexError("getMin from empty stack")
        return self.min_stack[-1]


# Unit tests to validate the MinStack implementation
import unittest

class TestMinStack(unittest.TestCase):
    def test_min_stack_operations(self):
        stack = MinStack()
        stack.push(3)
        stack.push(5)
        self.assertEqual(stack.getMin(), 3)
        stack.push(2)
        stack.push(1)
        self.assertEqual(stack.getMin(), 1)
        stack.pop()
        self.assertEqual(stack.getMin(), 2)
        stack.pop()
        self.assertEqual(stack.top(), 5)
        self.assertEqual(stack.getMin(), 3)

    def test_empty_stack(self):
        stack = MinStack()
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.top()
        with self.assertRaises(IndexError):
            stack.getMin()

    def test_duplicate_min_values(self):
        stack = MinStack()
        stack.push(1)
        stack.push(2)
        stack.push(1)
        self.assertEqual(stack.getMin(), 1)
        stack.pop()
        self.assertEqual(stack.getMin(), 1)

if __name__ == "__main__":
    unittest.main()

# Hints for revisiting this problem in 6 months:
# 1. **Understand the stack operations**: Review how push, pop, and top work in a stack.
# 2. **Focus on maintaining the minimum**: The MinStack stores the minimum at each level of the main stack.
# 3. **Consider edge cases**: What happens when the stack is empty? How do you handle that?
# 4. **Optimize space**: Can you reduce the space complexity while maintaining O(1) time for all operations?
# 5. **Practice with variations**: Try implementing a similar structure with different constraints (e.g., MaxStack) or additional features.
# 6. **Review time and space complexity**: 
#    - Time Complexity: O(1) for push, pop, top, and getMin operations.
#    - Space Complexity: O(n) for storing elements in the stack and minimum stack.
# 7. **Understand the trade-offs**: Why use two stacks instead of one? What are the benefits and drawbacks?