from typing import Optional, List
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Level-order (BFS) traversal, values grouped by depth. O(n) time/space.

        The level boundary trick: snapshot len(queue) BEFORE draining, so the
        children enqueued during this level don't inflate the count.
        """
        if root is None:
            return []
        q = deque([root])
        result = []
        while q:
            level_size = len(q)            # freeze: # nodes on this level
            level = []
            for _ in range(level_size):
                node = q.popleft()
                level.append(node.val)
                for child in (node.left, node.right):
                    if child:
                        q.append(child)
            result.append(level)
        return result

    def levelOrder_dfs(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Same result via DFS carrying depth -- no queue."""
        result: List[List[int]] = []

        def visit(node, depth):
            if node is None:
                return
            if depth == len(result):       # first node seen at this depth
                result.append([])
            result[depth].append(node.val)
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)

        visit(root, 0)
        return result


def _build(vals):
    """LeetCode-style level-order list (with None gaps) -> tree."""
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
        ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
        ([], []),
        ([1], [[1]]),
        ([1, 2, 3, 4, 5, 6, 7], [[1], [2, 3], [4, 5, 6, 7]]),
        ([1, 2, None, 3, None, 4], [[1], [2], [3], [4]]),   # left-skewed
    ]
    for vals, expected in test_cases:
        assert solution.levelOrder(_build(vals)) == expected, f"BFS failed on {vals}"
        assert solution.levelOrder_dfs(_build(vals)) == expected, f"DFS failed on {vals}"
    print("All tests passed.")
