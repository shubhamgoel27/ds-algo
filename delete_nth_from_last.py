from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        if head is None:
            return head 
        curr = head 
        for i in range(n):
            curr = curr.next 
        prev = head 
        if curr is None:
            return head.next 
        while curr.next is not None:
            curr = curr.next 
            prev = prev.next 
        
        prev.next = prev.next.next 
        return head 
    
def print_linked_list(head):
    elements = []
    while head:
        elements.append(head.val)
        head = head.next
    return elements


def test_removeNthFromEnd():
    solution = Solution()

    # Test Case 1: Remove the last element (n=1)
    head1 = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    n1 = 1
    result1 = solution.removeNthFromEnd(head1, n1)
    assert print_linked_list(result1) == [1, 2, 3, 4], "Test Case 1 Failed"

    # Test Case 2: Remove the first element (n=5)
    head2 = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    n2 = 5
    result2 = solution.removeNthFromEnd(head2, n2)
    assert print_linked_list(result2) == [2, 3, 4, 5], "Test Case 2 Failed"

    # Test Case 3: Remove an element in the middle (n=3)
    head3 = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    n3 = 3
    result3 = solution.removeNthFromEnd(head3, n3)
    assert print_linked_list(result3) == [1, 2, 4, 5], "Test Case 3 Failed"

    # Test Case 4: Single element list (n=1)
    head4 = ListNode(1)
    n4 = 1
    result4 = solution.removeNthFromEnd(head4, n4)
    assert print_linked_list(result4) == [], "Test Case 4 Failed"

    # Test Case 5: Two element list, remove the second element (n=1)
    head5 = ListNode(1, ListNode(2))
    n5 = 1
    result5 = solution.removeNthFromEnd(head5, n5)
    assert print_linked_list(result5) == [1], "Test Case 5 Failed"

    # Test Case 6: Two element list, remove the first element (n=2)
    head6 = ListNode(1, ListNode(2))
    n6 = 2
    result6 = solution.removeNthFromEnd(head6, n6)
    assert print_linked_list(result6) == [2], "Test Case 6 Failed"

    print("All test cases passed!")

if __name__ == "__main__":
    test_removeNthFromEnd()