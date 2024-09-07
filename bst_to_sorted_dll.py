# Definition for a Node.
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def treeToDoublyList(self, root: 'Optional[Node]') -> 'Optional[Node]':
        """
        Convert a Binary Search Tree (BST) to a sorted circular Doubly Linked List (DLL) in-place.

        Args:
            root (Optional[Node]): The root of the BST.

        Returns:
            Optional[Node]: The head of the sorted circular DLL.

        Time complexity: O(n), where n is the number of nodes in the tree.
        Space complexity: O(h), where h is the height of the tree (due to recursion stack).
        """
        if not root:
            return None

        # Initialize head and prev pointers
        self.head = None
        self.prev = None

        def inorder_traverse(node):
            if not node:
                return

            # Traverse left subtree
            inorder_traverse(node.left)

            # Process current node
            if self.prev:
                # Connect current node with previous node
                self.prev.right = node
                node.left = self.prev
            else:
                # First node (leftmost) becomes the head
                self.head = node
            self.prev = node

            # Traverse right subtree
            inorder_traverse(node.right)

        # Perform inorder traversal
        inorder_traverse(root)

        # Connect the first and last nodes to make it circular
        if self.head and self.prev:
            self.head.left = self.prev
            self.prev.right = self.head

        return self.head

# Test cases
def test_treeToDoublyList():
    # Helper function to create a BST
    def create_bst(values):
        if not values:
            return None
        root = Node(values[0])
        for val in values[1:]:
            insert_bst(root, val)
        return root

    def insert_bst(node, val):
        if val < node.val:
            if node.left:
                insert_bst(node.left, val)
            else:
                node.left = Node(val)
        else:
            if node.right:
                insert_bst(node.right, val)
            else:
                node.right = Node(val)

    # Helper function to verify the circular DLL
    def verify_dll(head):
        if not head:
            return True
        curr = head
        values = []
        while True:
            values.append(curr.val)
            curr = curr.right
            if curr == head:
                break
        return values == sorted(values) and len(values) == len(set(values))

    solution = Solution()

    # Test case 1: Empty tree
    assert solution.treeToDoublyList(None) == None

    # Test case 2: Single node tree
    single_node = Node(1)
    result = solution.treeToDoublyList(single_node)
    assert result.val == 1 and result.left == result and result.right == result

    # Test case 3: Normal BST
    bst = create_bst([4, 2, 5, 1, 3])
    result = solution.treeToDoublyList(bst)
    assert verify_dll(result)

    print("All test cases passed!")

# Run the tests
test_treeToDoublyList()

# Hints:
# 1. Use inorder traversal to visit nodes in sorted order.
# 2. Keep track of the previously visited node to establish links.
# 3. Remember to handle the connection between the first and last nodes.
# 4. Be careful with edge cases like empty trees or single-node trees.

