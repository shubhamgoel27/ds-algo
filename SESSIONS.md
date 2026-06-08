# Session Journal — what tripped me, per attempt

> Auto-generated from `review.json` history by `review.py gen`. Newest first. Read this at the start of a session to target weak spots.

Total attempts logged: **6**.

---

### 2026-06-07 · LC20 Valid Parentheses · conf 5/5  (Stack, E)
`valid_parentheses.py`  
Remembered the whole solution unaided. Correct, clean, O(n)/O(n). Stated both failure modes (empty-on-close, top-mismatch) upfront. Used open->close map (equally valid); saved the close->open + 'not stack' idiom version to valid_parentheses.py.

### 2026-06-07 · LC33 Search in Rotated Sorted Array · conf 2/5  (Binary Search, M)
`search_rotated_array.py`  
Right approach (which-half-is-sorted) but needed ~4 iterations + heavy hints + final solution. Bug sequence (all classic rotated-array traps): missing pointer-move (hang), strict-vs-inclusive range bounds, slice-index offset, helper low=mid infinite loop, high=mid+1 wrong direction, mid==low misclassification (> vs >=), no final return -1, and -1 offset producing a FALSE-POSITIVE index. Also the two-level slice design is secretly O(n) (slice copies) -> fails O(log n). LESSON: single loop, check nums[mid]==target FIRST, detect sorted half with nums[lo]<=nums[mid] (INCLUSIVE), bracket target in that half. The <= that owns mid==low is the whole game. REDO SOON.

### 2026-06-07 · LC206 Reverse Linked List · conf 5/5  (Linked List, E)
`reverse_linked_list.py`  
Clean unaided iterative 3-pointer reversal, invariant (prev=reversed prefix) stated upfront. Correct O(n)/O(1). Minor: redundant 'if not head' guard (loop handles empty). Knows the pattern cold. Saved file includes recursive variant + one-liner swap idiom.

### 2026-06-07 · LC102 Binary Tree Level Order Traversal · conf 4/5  (Trees, M)
`level_order_traversal.py`  
Reconstructed level-BFS off one structural hint (the freeze-len(q) boundary). Clean execution after. Style nit: used 'q.append(x) if x else 0' ternary-as-statement -> plain if. Knows BFS; wanted to relearn DFS engine next.

### 2026-06-07 · LC146 LRU Cache · conf 3/5  (Design, M)
`lru_cache.py`  
Design 100% correct (hashmap+DLL, dummy sentinels, key stored on node). But 3 impl bugs, one fatal: (1) put created the node TWICE -> dict and list referenced different objects -> get crashed on None.prev. (2) remove_tail defined with stray 'node' param but called with none. (3) del self.cache[key] used undefined name; should be lru.key (this is WHY key is stored on node). Abstraction lesson: unlink surgery was duplicated in move_to_head AND remove_tail -> extract atomic _remove(node) primitive, compose everything from _remove + _add_front. Helpers were conceptually right, just redundant + buggy. WATCH: DLL pointer surgery, and 'stored the data but forgot to use it'.

### 2026-06-06 · LC56 Merge Intervals · conf 5/5  (Intervals, M)
`merged_intervals.py`  
Clean optimal solve, essentially identical to saved 2024 soln (sort → sweep → merge on curr_start<=prev_end, max of ends). Minor: loop ran from i=0 (redundant self-compare) — use intervals[1:]. Solid muscle memory.
