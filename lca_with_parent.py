# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        """
        Find the lowest common ancestor of two nodes in a binary tree with parent pointers.

        Args:
            p (Node): First node
            q (Node): Second node

        Returns:
            Node: The lowest common ancestor of p and q

        Time complexity: O(h), where h is the height of the tree
        Space complexity: O(h), where h is the height of the tree
        """
        ancestors = set()
        
        # Traverse from p to root, adding all ancestors to the set
        while p:
            ancestors.add(p)
            p = p.parent
        
        # Traverse from q to root, checking if any node is in p's ancestors
        while q:
            if q in ancestors:
                return q
            q = q.parent
        
        # This line should never be reached if p and q are in the same tree
        return None

# Test cases
def test_lowest_common_ancestor():
    # Create a sample tree
    #       3
    #     /   \
    #    5     1
    #   / \   / \
    #  6   2 0   8
    #     / \
    #    7   4

    nodes = [Node(i) for i in range(9)]
    nodes[3].left, nodes[3].right = nodes[5], nodes[1]
    nodes[5].left, nodes[5].right, nodes[5].parent = nodes[6], nodes[2], nodes[3]
    nodes[1].left, nodes[1].right, nodes[1].parent = nodes[0], nodes[8], nodes[3]
    nodes[2].left, nodes[2].right, nodes[2].parent = nodes[7], nodes[4], nodes[5]
    nodes[6].parent = nodes[5]
    nodes[0].parent = nodes[1]
    nodes[8].parent = nodes[1]
    nodes[7].parent = nodes[2]
    nodes[4].parent = nodes[2]

    solution = Solution()

    # Test case 1: LCA of 5 and 1 should be 3
    assert solution.lowestCommonAncestor(nodes[5], nodes[1]) == nodes[3]

    # Test case 2: LCA of 5 and 4 should be 5
    assert solution.lowestCommonAncestor(nodes[5], nodes[4]) == nodes[5]

    # Test case 3: LCA of 6 and 4 should be 5
    assert solution.lowestCommonAncestor(nodes[6], nodes[4]) == nodes[5]

    # Test case 4: LCA of 7 and 8 should be 3
    assert solution.lowestCommonAncestor(nodes[7], nodes[8]) == nodes[3]

    print("All test cases passed!")

# Run the test cases
test_lowest_common_ancestor()