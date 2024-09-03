from typing import Optional
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Calculate the diameter of a binary tree.

        The diameter of a binary tree is the length of the longest path between any two nodes
        in a tree. This path may or may not pass through the root.

        Args:
            root (Optional[TreeNode]): The root node of the binary tree.

        Returns:
            int: The diameter of the binary tree.
        """
        self.max_diameter = 0

        def dfs(node: TreeNode) -> int:
            if not node:
                return 0
            # Get the heights of the left and right subtrees
            left_height = dfs(node.left)
            right_height = dfs(node.right)

            # Update the maximum diameter if the current diameter is larger
            self.max_diameter = max(self.max_diameter, left_height + right_height)

            # Return the height of the current node
            return max(left_height, right_height) + 1

        dfs(root)
        return self.max_diameter

# Test cases
import unittest

class TestDiameterOfBinaryTree(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_empty_tree(self):
        self.assertEqual(self.solution.diameterOfBinaryTree(None), 0)

    def test_single_node(self):
        root = TreeNode(1)
        self.assertEqual(self.solution.diameterOfBinaryTree(root), 0)

    def test_linear_tree(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)
        self.assertEqual(self.solution.diameterOfBinaryTree(root), 2)

    def test_balanced_tree(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        self.assertEqual(self.solution.diameterOfBinaryTree(root), 3)

    def test_unbalanced_tree(self):
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        root.left.right.right = TreeNode(6)
        root.right = TreeNode(3)
        self.assertEqual(self.solution.diameterOfBinaryTree(root), 4)

if __name__ == '__main__':
    unittest.main()