from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        level_dict = {}
        def dfs(root,level):
            if root is None:
                return 
            if level not in level_dict:
                level_dict[level] = root.val
            right = dfs(root.right, level+1)
            left = dfs(root.left, level+1)
            
        dfs(root, 0)
        return list(level_dict.values())

def test_rightSideView():
    solution = Solution()

    # Test case 1: Empty tree
    root = None
    assert solution.rightSideView(root) == []

    # Test case 2: Single node tree
    root = TreeNode(1)
    assert solution.rightSideView(root) == [1]

    # Test case 3: Left-skewed tree
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    assert solution.rightSideView(root) == [1, 2, 3]

    # Test case 4: Right-skewed tree
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    assert solution.rightSideView(root) == [1, 2, 3]

    # Test case 5: Full binary tree
    root = TreeNode(1,
                    TreeNode(2, TreeNode(4), TreeNode(5)),
                    TreeNode(3, TreeNode(6), TreeNode(7)))
    assert solution.rightSideView(root) == [1, 3, 7]

    # Test case 6: Mixed skewed tree
    root = TreeNode(1,
                    TreeNode(2, None, TreeNode(5)),
                    TreeNode(3, None, TreeNode(4)))
    assert solution.rightSideView(root) == [1, 3, 4]

    print("All test cases passed!")

# Run the test cases
test_rightSideView()