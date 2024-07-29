class BSTClosestValue:
    def __init__(self):
        self.global_diff = float("inf")
        self.closest_node = None

    def traverse(self, root, target):
        if root is None:
            return
        curr_diff = abs(root.val - target)
        if self.global_diff > curr_diff:
            self.global_diff = curr_diff
            self.closest_node = root

        if target < root.val:
            self.traverse(root.left, target)
        else:
            self.traverse(root.right, target)

        return self.closest_node

# Example usage:
# Assuming you have a TreeNode class and a BST already created
# bst_closest = BSTClosestValue()
# closest_node = bst_closest.traverse(root, target)
# print(closest_node.val)  # or however you want to access the value
