# Code Notes

## Array and String Manipulation

### Reorganize String
- Use max-heap to prioritize characters with higher frequencies
- Alternate characters to ensure no adjacent characters are the same
- Time complexity: O(n log k), where k is the number of unique characters
- [Code reference](reorganize_string.py)

### Simplify Path
- Use stack to process path components
- Handle special cases: "..", ".", and empty components
- Time complexity: O(n), Space complexity: O(n)
- [Code reference](simplify_path.py)

### Custom Sort String
- Use counter to track character frequencies
- Build result string based on custom order
- Time complexity: O(n + k), where k is the length of the order string
- [Code reference](custom_sort_string.py)

### Move Zeros
- Two-pointer approach to swap elements
- Maintain order of non-zero elements
- Time complexity: O(n), Space complexity: O(1)
- [Code reference](move_zeros.py)

### Product of Array Except Self
- Two-pass approach: left products and right products
- Alternative solution with O(1) extra space
- Time complexity: O(n), Space complexity: O(1) (for the optimized version)
- [Code reference](product_of_all_except_self.py)

### Valid Word Abbreviation
- Two-pointer approach to compare word and abbreviation
- Handle numeric abbreviations and character matches
- Check for invalid cases like leading zeros
- Time complexity: O(n), where n is the length of the longer string
- [Code reference](valid_word_abbr.py)

## Tree Operations

### BST to Sorted Doubly Linked List
- In-order traversal to maintain sorted order
- Connect nodes to form circular doubly linked list
- Time complexity: O(n), Space complexity: O(h) for recursion stack
- [Code reference](bst_to_sorted_dll.py)

### Right View of Binary Tree
- Depth-first search, prioritizing rightmost nodes
- Use level tracking to identify rightmost node at each level
- Time complexity: O(n), Space complexity: O(h)
- [Code reference](right_view_of_tree.py)

### Range Sum of BST
- Recursive traversal with pruning
- Skip subtrees outside the given range
- Time complexity: O(n), Space complexity: O(h)
- [Code reference](range_sum_of_bst.py)

### Lowest Common Ancestor in Binary Tree
- Recursive approach to find LCA
- Return node if it matches either target or if its subtrees contain targets
- Time complexity: O(n), Space complexity: O(h)
- [Code reference](lca_of_binary_tree.py)

### Binary Tree Vertical Traversal
- Level-order traversal with column tracking
- Use hash map to group nodes by column
- Time complexity: O(n log n), Space complexity: O(n)
- [Code reference](binary_tree_vertical_traversal.py)

### Diameter of Binary Tree
- Recursive approach to calculate height and diameter simultaneously
- Update diameter during height calculation
- Time complexity: O(n), Space complexity: O(h)
- [Code reference](diameter_of_tree.py)

### Closest Value in BST
- Recursive traversal, updating closest value
- Use BST property to optimize search
- Time complexity: O(log n) average, O(n) worst case
- [Code reference](return_closest_in_bst.py)

## Linked List Operations

### LCA with Parent Pointers
- Use set to store ancestors of one node
- Traverse up from other node to find first common ancestor
- Time complexity: O(h), Space complexity: O(h)
- [Code reference](lca_with_parent.py)

### Delete Nth Node from End
- Two-pointer approach: fast and slow pointers
- Move fast pointer n steps ahead, then move both until fast reaches end
- Time complexity: O(n), Space complexity: O(1)
- [Code reference](delete_nth_from_last.py)

### Insert into Circular Linked List
- Handle edge cases: empty list, insertion at beginning/end
- Traverse to find correct insertion point
- Time complexity: O(n), Space complexity: O(1)
- [Code reference](insert_into_circular_node.py)

### Copy List with Random Pointer
- Use hash map to store mapping between original and copied nodes
- Two-pass algorithm: create nodes, then set pointers
- Time complexity: O(n), Space complexity: O(n)
- [Code reference](copy_ll_with_random_node.py)

## Heap and Priority Queue

### K Most Frequent Elements
- Use hash map for frequency counting
- Use min-heap to maintain k most frequent elements
- Time complexity: O(n log k), Space complexity: O(n)
- [Code reference](k_most_frequent.py)

### Median of Data Stream
- Use two heaps: max-heap for lower half, min-heap for upper half
- Balance heaps after each insertion
- Time complexity: O(log n) per insertion, O(1) for finding median
- [Code reference](median_of_stream.py)

### K Closest Points to Origin
- Use min-heap to maintain k closest points
- Calculate distance using Euclidean formula
- Time complexity: O(n log k), Space complexity: O(k)
- [Code reference](k_closest_to_origin.py)

## Graph and Matrix Problems

### Number of Islands
- Implement both BFS and DFS approaches
- Mark visited land cells to avoid revisiting
- Time complexity: O(m * n), Space complexity: O(min(m, n)) for BFS
- [Code reference](no_of_islands.py)

### Shortest Path in Binary Matrix
- Use BFS to explore grid and find shortest path
- Keep track of distance for each cell
- Time complexity: O(m * n), Space complexity: O(m * n)
- [Code reference](shortest_path_in_binary_grid.py)

## Interval Problems

### Merge Intervals
- Sort intervals by start time
- Merge overlapping intervals in a single pass
- Time complexity: O(n log n), Space complexity: O(n)
- [Code reference](merged_intervals.py)

### Interval Intersection
- Two-pointer approach to compare intervals
- Find overlapping parts and add to result
- Time complexity: O(m + n), Space complexity: O(min(m, n))
- [Code reference](interval_intersection.py)

## Dynamic Programming and Sliding Window

### Max Consecutive Ones III
- Sliding window approach with at most K zeros
- Expand window and contract when zero count exceeds K
- Time complexity: O(n), Space complexity: O(1)
- [Code reference](max_consecutive_ones.py)

## Miscellaneous

### LRU Cache
- Use hash map and doubly linked list
- O(1) time complexity for both get and put operations
- Maintain capacity by removing least recently used item
- [Code reference](lru_cache.py)

### Subarray Sum Equals K
- Use cumulative sum approach with hash map
- Track frequency of cumulative sums
- Time complexity: O(n), Space complexity: O(n)
- [Code reference](subarray_sum_k.py)

### Group Shifted Strings
- Use hash map to group strings by relative character differences
- Calculate difference sequence for each string
- Time complexity: O(n * k), where k is the average string length
- [Code reference](group_shifted_sequences.py)

### Find Peak Element
- Binary search approach to find peak efficiently
- Compare middle element with its neighbors
- Time complexity: O(log n), Space complexity: O(1)
- [Code reference](peak_in_array.py)

### Merge Sorted Arrays
- Two-pointer approach, starting from the end
- Fill larger array from back to front
- Time complexity: O(m + n), Space complexity: O(1)
- [Code reference](merge_sorted_arrays.py)
