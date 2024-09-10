from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find the middle node of a singly-linked list.
        
        If the list has an even number of nodes, return the second middle node.
        
        Args:
            head (Optional[ListNode]): The head of the linked list.
        
        Returns:
            Optional[ListNode]: The middle node of the linked list.
        """
        # Edge case: if the list has only one node, return it
        if not head.next:
            return head
        
        # Use two pointers: slow and fast
        slow = fast = head
        
        # Move slow pointer by one step and fast pointer by two steps
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # When fast reaches the end, slow will be at the middle
        return slow

# Test cases
def test_middleNode():
    # Helper function to create a linked list from a list of values
    def create_linked_list(values):
        dummy = ListNode(0)
        current = dummy
        for val in values:
            current.next = ListNode(val)
            current = current.next
        return dummy.next

    # Test case 1: Odd number of nodes
    head1 = create_linked_list([1, 2, 3, 4, 5])
    assert Solution().middleNode(head1).val == 3

    # Test case 2: Even number of nodes
    head2 = create_linked_list([1, 2, 3, 4, 5, 6])
    assert Solution().middleNode(head2).val == 4

    # Test case 3: Single node
    head3 = create_linked_list([1])
    assert Solution().middleNode(head3).val == 1

    print("All test cases passed!")

# Uncomment the line below to run the test cases
test_middleNode()

# Hints for solving this problem:
# 1. Use the "tortoise and hare" approach (slow and fast pointers).
# 2. The fast pointer moves twice as fast as the slow pointer.
# 3. When the fast pointer reaches the end, the slow pointer will be at the middle.
# 4. This method works for both odd and even number of nodes.
# 5. Time complexity: O(n), where n is the number of nodes in the linked list.
# 6. Space complexity: O(1), as we only use two pointers regardless of list size.