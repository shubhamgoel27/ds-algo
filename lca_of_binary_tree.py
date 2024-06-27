class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:    
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is None:
            return None 
        if root == p or root == q:
            return root
        
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root
        if left:
            return left
        if right:
            return right
        
def test_lowestCommonAncestor():
    solution = Solution()

    # Test Case 1: LCA of nodes in different subtrees
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)
    
    p = root.left  # Node 5
    q = root.right  # Node 1
    assert solution.lowestCommonAncestor(root, p, q).val == 3, "Test Case 1 Failed"

    # Test Case 2: LCA of nodes in the same subtree
    p = root.left  # Node 5
    q = root.left.right.right  # Node 4
    assert solution.lowestCommonAncestor(root, p, q).val == 5, "Test Case 2 Failed"

    # Test Case 3: LCA where one node is the root
    p = root  # Node 3
    q = root.left.right.right  # Node 4
    assert solution.lowestCommonAncestor(root, p, q).val == 3, "Test Case 3 Failed"

    # Test Case 4: LCA where nodes are the same
    p = root.left  # Node 5
    q = root.left  # Node 5
    assert solution.lowestCommonAncestor(root, p, q).val == 5, "Test Case 4 Failed"

    # Test Case 5: LCA in a linear tree (linked list style)
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.left.left = TreeNode(4)
    
    p = root.left.left  # Node 3
    q = root.left.left.left  # Node 4
    assert solution.lowestCommonAncestor(root, p, q).val == 3, "Test Case 5 Failed"

    # Test Case 6: LCA in an unbalanced tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(4)
    root.left.left.left = TreeNode(8)
    root.left.left.right = TreeNode(9)
    root.right = TreeNode(3)
    root.right.right = TreeNode(7)
    root.right.right.left = TreeNode(10)
    
    p = root.left.left.right  # Node 9
    q = root.right.right.left  # Node 10
    assert solution.lowestCommonAncestor(root, p, q).val == 1, "Test Case 6 Failed"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_lowestCommonAncestor()