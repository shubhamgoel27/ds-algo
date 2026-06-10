from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """Bounds-down recursion. Each node must lie strictly inside (low, high);
        recurse left with a tightened high, right with a tightened low.

        Info flows DOWN as (low, high) params and UP as the bool. The strict
        `<=`/`>=` checks reject duplicates (BST values are strictly ordered).
        O(n) time, O(h) stack.
        """
        def dfs(node, low, high):
            if not node:
                return True
            if node.val <= low or node.val >= high:
                return False
            return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)

        return dfs(root, -float("inf"), float("inf"))

    def isValidBST_inorder(self, root: Optional[TreeNode]) -> bool:
        """Alternative: in-order traversal of a BST is strictly increasing."""
        prev = -float("inf")

        def inorder(node):
            nonlocal prev
            if not node:
                return True
            if not inorder(node.left):
                return False
            if node.val <= prev:
                return False
            prev = node.val
            return inorder(node.right)

        return inorder(root)


def _build(vals):
    if not vals:
        return None
    it = iter(vals)
    root = TreeNode(next(it))
    q = deque([root])
    for v in it:
        node = q[0]
        if not hasattr(node, "_filled_left"):
            if v is not None:
                node.left = TreeNode(v)
                q.append(node.left)
            node._filled_left = True
        else:
            if v is not None:
                node.right = TreeNode(v)
                q.append(node.right)
            q.popleft()
    return root


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([2, 1, 3], True),
        ([5, 1, 4, None, None, 3, 6], False),
        ([5, 4, 6, None, None, 3, 7], False),    # the ancestor-bound trap
        ([], True),
        ([1], True),
        ([2, 2], False),                          # duplicate (strict bound)
        ([1, 1], False),
        ([3, 1, 5, 0, 2, 4, 6], True),
        ([-2147483648], True),                    # int-min edge
    ]
    for vals, expected in test_cases:
        assert solution.isValidBST(_build(vals)) == expected, f"bounds failed on {vals}"
        assert solution.isValidBST_inorder(_build(vals)) == expected, f"inorder failed on {vals}"
    print("All tests passed.")
