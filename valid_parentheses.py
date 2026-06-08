class Solution:
    def isValid(self, s: str) -> bool:
        """Return True iff every bracket is closed by the same type in the right order.

        Stack of open brackets. Map each *closer* to its matching *opener* so a
        close is valid only when it pops exactly that opener off the top.

        Three failure modes, one check each:
          - closer with an empty stack      -> unmatched close
          - top opener != expected opener   -> wrong type / wrong order
          - stack non-empty at the end      -> unmatched open

        Time: O(n). Space: O(n) for the stack.
        """
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for c in s:
            if c in pairs:                              # c is a closing bracket
                if not stack or stack.pop() != pairs[c]:
                    return False
            else:                                       # c is an opening bracket
                stack.append(c)
        return not stack


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),          # classic ordering trap
        ("{[]}", True),
        ("(", False),             # unmatched open
        ("", True),               # empty is valid
        (")", False),             # unmatched close
        ("((", False),
        ("([{}])", True),
        ("[({})](]", False),
        ("(" * 5000 + ")" * 5000, True),   # deep nesting stress
    ]
    for s, expected in test_cases:
        result = solution.isValid(s)
        label = s if len(s) <= 12 else f"{s[:6]}...(len {len(s)})"
        assert result == expected, f"Test failed for {label!r}: expected {expected}, got {result}"
    print("All tests passed.")
