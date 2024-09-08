# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

from typing import Optional
from collections import deque

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        """
        Clone a given undirected graph.
        
        Args:
            node (Optional['Node']): The root node of the graph to be cloned.
        
        Returns:
            Optional['Node']: The root node of the cloned graph.
        """
        if not node:
            return node
        
        # Dictionary to map original nodes to their clones
        clones = {}
        
        # Create the clone of the first node
        clones[node] = Node(node.val)
        
        # Use BFS to traverse the graph
        queue = deque([node])
        while queue:
            curr = queue.popleft()
            for neighbor in curr.neighbors:
                if neighbor not in clones:
                    # Create a new clone for this neighbor
                    clones[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)
                
                # Connect the current clone to its neighbor's clone
                clones[curr].neighbors.append(clones[neighbor])
        
        return clones[node]

# Test cases
def test_clone_graph():
    # Test case 1: Single node
    node1 = Node(1)
    assert Solution().cloneGraph(node1).val == 1
    assert len(Solution().cloneGraph(node1).neighbors) == 0

    # Test case 2: Two connected nodes
    node1 = Node(1)
    node2 = Node(2)
    node1.neighbors = [node2]
    node2.neighbors = [node1]
    cloned = Solution().cloneGraph(node1)
    assert cloned.val == 1
    assert len(cloned.neighbors) == 1
    assert cloned.neighbors[0].val == 2
    assert cloned.neighbors[0].neighbors[0] == cloned

    # Test case 3: Empty graph
    assert Solution().cloneGraph(None) == None

    print("All test cases passed!")

test_clone_graph()

"""
Hints for solving this problem:

1. Use a hash map to keep track of the cloned nodes. The key will be the original node, and the value will be its clone.
2. Implement a breadth-first search (BFS) using a queue to traverse the graph.
3. When creating new clones, add them to both the hash map and the queue.
4. Remember to handle the case of an empty graph (null input).
5. Be careful not to create duplicate clones or connections.
6. Think about how to maintain the connections between cloned nodes.
7. Consider edge cases like self-loops and disconnected components.

Time Complexity: O(N + E), where N is the number of nodes and E is the number of edges.
Space Complexity: O(N) for the hash map and queue.

Remember: Practice with different graph structures to ensure your solution works for all cases!
"""
