# Session Journal — what tripped me, per attempt

> Auto-generated from `review.json` history by `review.py gen`. Newest first. Read this at the start of a session to target weak spots.

Total attempts logged: **12**.

---

### 2026-06-10 · LC3 Longest Substring Without Repeating Chars · conf 2/5  (Sliding Window, M)
`longest_substring_without_repeating.py`  
First rep in sliding-window, needed the full structure handed over. Root bug: split into if(duplicate)=shrink vs else=add+record, so the current char was never added and answer never recorded on duplicate steps -> set drifted out of sync with window -> KeyError. Fix: shrink FIRST (while char in window), THEN add + record UNCONDITIONALLY every iteration. Learned the dict-jump upgrade (last[char]+1) and the critical max(left, last[char]+1) guard so left never moves backward (the abba case). Pattern not yet in muscle memory; needs more longest-valid reps.

### 2026-06-10 · LC1004 Max Consecutive Ones III · conf 1/5  (Sliding Window, M)
`max_consecutive_ones.py`  
Second sliding-window rep, same longest-valid shape. Still needed the full 5-slot skeleton handed over; fell back into the if(current element)/else branching anti-pattern again (the exact LC3 mistake). Once given the template, assembled and ran it correctly. The blocker is structural: not yet separating 'element updates state' from 'state drives the shrink decision'. Pattern needs 2-3 more reps; SR will resurface tomorrow. Element->state->decision separation is the thing to drill.

### 2026-06-10 · LC236 Lowest Common Ancestor of Binary Tree · conf 5/5  (Trees, M)
`lca_of_binary_tree.py`  
Algorithm correct on first attempt, fully unaided: post-order, return the found node up; both-sides-non-null means this node is the LCA, else pass up the non-null side. Got the self-ancestor short-circuit right too. Only nits were mechanical (compared node.val to a node object; trailing comma was a paste artifact). Different idiom from diameter: return value IS the answer, no nonlocal. Strong solve. Refinements noted: 'return left or right', and identity comparison (node is p) is the bulletproof form.

### 2026-06-09 · LC226 Invert Binary Tree · conf 4/5  (Trees, E)
`invert_binary_tree.py`  
DFS warm-up after a long gap. Conceptual answers right (base None, op=swap, mutate-in-place). 2 hints, both EXECUTION slips: (1) swapped local vars instead of node.left/node.right attributes, (2) defined dfs but never called it. Recursion reflex returning. META: user is comfortable with the helper-fn/mutation style but wants fluency with return-value recursion ('trust the call, define what the subtree returns'). Coach the return-value framing on tree problems.

### 2026-06-09 · LC543 Diameter of Binary Tree · conf 3/5  (Trees, E)
`diameter_of_tree.py`  
Reconstructed the 'return one thing, track another' idiom (return height, track diameter=left_h+right_h via nonlocal). 2 hints: (1) capture child heights into vars (don't call dfs twice), (2) drop the +1 (left_h+right_h already counts both arms meeting at the node). Concept landed; matches 2024 saved soln exactly. Now primed for Max Path Sum 124 (same idiom + max(0,..)). Boundary/formula precision still needs reps.

### 2026-06-09 · LC98 Validate Binary Search Tree · conf 5/5  (Trees, M)
`validate_bst.py`  
Strong solve. Nailed the hard insight UNAIDED: pass (low,high) bounds DOWN and tighten per node (not naive local left<node<right) — caught the ancestor-bound trap [5,4,6,null,null,3,7] first try. One nudge: strict boundary, used < / > so duplicates [2,2]/[1,1] slipped -> fixed to <= / >= (same strict-vs-inclusive lesson as LC33 rotated search). RECURSION-COMFORT WIN: clean DOWN-params/UP-bool recursion, trusted the dfs calls — exactly the fluency goal. Knows in-order-sorted alt too now.

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
