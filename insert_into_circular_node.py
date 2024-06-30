from typing import Optional 
# Definition for a Node.
class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

class Solution:
    
    def insert(self, head: 'Optional[Node]', insertVal: int) -> 'Node':
        new_node = Node(insertVal)
        
        if head is None:
            new_node.next = new_node
            return new_node
        
        current = head

        while True:
            if current.val <= insertVal <= current.next.val:
                break
            
            if current.val > current.next.val:
                if insertVal >= current.val or insertVal <= current.next.val:
                    break
            
            current = current.next
            
            if current == head:
                break
        new_node.next = current.next
        current.next = new_node
        
        return head