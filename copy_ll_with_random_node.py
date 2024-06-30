
from typing import Optional
# Definition for a Node.

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None
        h = {}
        curr = head
        while curr is not None:
            if curr not in h:
                h[curr] = Node(curr.val)
                curr = curr.next 
        curr = head 
        while curr is not None:
            copy_curr = h[curr]
            if curr.next:
                copy_curr.next = h[curr.next]
            if curr.random:
                copy_curr.random = h[curr.random]
            curr = curr.next 

        return h[head]

def printList(head: 'Optional[Node]'):
    curr = head
    result = []
    while curr:
        random_val = curr.random.val if curr.random else None
        result.append((curr.val, random_val))
        curr = curr.next
    return result

def test_copyRandomList():
    solution = Solution()
    
    # Test Case 1: Single Node with No Random Pointer
    node1 = Node(1)
    assert printList(solution.copyRandomList(node1)) == [(1, None)]
    
    # Test Case 2: Single Node with Random Pointer to Itself
    node1 = Node(1)
    node1.random = node1
    assert printList(solution.copyRandomList(node1)) == [(1, 1)]
    
    # Test Case 3: Two Nodes with No Random Pointers
    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    assert printList(solution.copyRandomList(node1)) == [(1, None), (2, None)]
    
    # Test Case 4: Two Nodes with Random Pointers
    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    node1.random = node2
    node2.random = node1
    assert printList(solution.copyRandomList(node1)) == [(1, 2), (2, 1)]
    
    # Test Case 5: Complex Case with Multiple Nodes and Random Pointers
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node1.random = node3
    node2.random = node1
    node3.random = node4
    node4.random = node2
    assert printList(solution.copyRandomList(node1)) == [(1, 3), (2, 1), (3, 4), (4, 2)]
    
    print("All test cases pass")

test_copyRandomList()
