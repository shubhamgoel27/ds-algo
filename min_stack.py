class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum element in constant time.
    """

    def __init__(self):
        """Initialize the MinStack with two lists: one for the stack and one for the minimums."""
        self.min = []  # Stack to keep track of minimum values
        self.stack = []  # Main stack to store values

    def push(self, val: int) -> None:
        """
        Push a new value onto the stack.
        If the new value is less than or equal to the current minimum, update the minimum stack.
        """
        if not self.min:
            self.min.append(val)
        else:
            # Append the new minimum if the current value is less than the last minimum
            if val < self.min[-1]:
                self.min.append(val)
            else:
                self.min.append(self.min[-1])

        self.stack.append(val)

    def pop(self) -> None:
        """Remove the top element from the stack and the corresponding minimum."""
        if self.stack:
            self.stack.pop()
            self.min.pop()

    def top(self) -> int:
        """Return the top element of the stack."""
        return self.stack[-1]

    def getMin(self) -> int:
        """Retrieve the minimum element in the stack."""
        return self.min[-1]


# Unit tests to validate the MinStack implementation
import unittest

class TestMinStack(unittest.TestCase):
    def test_min_stack(self):
        obj = MinStack()
        obj.push(3)
        obj.push(5)
        self.assertEqual(obj.getMin(), 3)  # Should print 3
        obj.push(2)
        obj.push(1)
        self.assertEqual(obj.getMin(), 1)  # Should print 1
        obj.pop()
        self.assertEqual(obj.getMin(), 2)  # Should print 2
        obj.pop()
        self.assertEqual(obj.top(), 5)     # Should print 5
        self.assertEqual(obj.getMin(), 3)  # Should print 3

if __name__ == "__main__":
    unittest.main()

# Hints for revisiting this problem in 6 months:
# 1. **Understand the stack operations**: Review how push, pop, and top work in a stack.
# 2. **Focus on maintaining the minimum**: The MinStack stores the minimum at each level of the main stack.
# 3. **Consider edge cases**: What happens when the stack is empty? How do you handle that?
# 4. **Practice with variations**: Try implementing a similar structure with different constraints or additional features.
# 5. **Review time and space complexity**: 
#    - Time Complexity: O(1) for push, pop, top, and getMin operations.
#    - Space Complexity: O(n) for storing elements in the stack and minimum stack.