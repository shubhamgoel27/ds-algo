from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """Return-value style: each call returns its inverted subtree. O(n) time, O(h) stack.

        Read it as: "the inverted tree has, as its left child, the inverted RIGHT
        subtree, and vice versa." Trust the recursion to invert each side.
        """
        if root is None:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root

    def invertTree_helper(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """Helper / mutation style: walk the tree, swap children in place."""
        def dfs(node):
            if node is None:
                return
            node.left, node.right = node.right, node.left   # swap sticks to the node
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return root


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


def _level(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        n = q.popleft()
        if n:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]),
        ([2, 1, 3], [2, 3, 1]),
        ([], []),
        ([1], [1]),
    ]
    for vals, expected in test_cases:
        assert _level(solution.invertTree(_build(vals))) == expected, f"return-value failed on {vals}"
        assert _level(solution.invertTree_helper(_build(vals))) == expected, f"helper failed on {vals}"
    print("All tests passed.")
