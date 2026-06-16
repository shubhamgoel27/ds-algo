# Session Journal — what tripped me, per attempt

> Auto-generated from `review.json` history by `review.py gen`. Newest first (timestamped). Read this at the start of a session to target weak spots.

Total attempts logged: **30**.

---

### 2026-06-16 16:26 · LC78 Subsets · conf 3/5  (Backtracking, M)
`LC78`  
First backtracking problem. Wrote it correctly but leaned on the template I provided (-> honest 3). Got a deep step-by-step instrumented trace to understand the execution: DFS dives leftmost-deep first, path 'breathes' (append descending, pop ascending), empty for-loop = natural base case, start index = forward-only = no duplicates, record at EVERY node for subsets. Mental model: backtracking = DFS on a decision tree; design knob = the next-state passed down (i+1 no-reuse, i reuse, used[] permutations). Vocab: labyrinthine.

### 2026-06-15 19:12 · LC347 Top K Frequent Elements · conf 5/5  (Arrays & Hashing, M)
`k_most_frequent.py`  
Top K Frequent: Counter + bounded MIN-heap of size k on frequency (keep k largest freqs -> evict the least frequent). Clean unaided, applied the inversion rule correctly a 3rd time -> locked in. Refreshed k_most_frequent.py with the heap version. Taught (not stored) the O(n) bucket-sort alternative (counting-sort idea: bound the key, skip comparison sort) and Counter.most_common(k) prod one-liner. Vocab: preponderance (and mode/modal). Strong.

### 2026-06-15 19:03 · LC973 K Closest Points to Origin · conf 5/5  (Heap / PQ, M)
`k_closest_to_origin.py`  
Bounded MAX-heap of size k for k-closest (k smallest distances). Clean unaided, and TRANSFERRED the bounded-heap idiom from LC215 AND correctly flipped min->max (k smallest needs max-heap, evict the farthest). Beat his own 2024 version (which heaped all n then popped k, O(n log n)). Drilled the inversion fundamentally: heap root = the one on the chopping block = the anti-goal extreme; you keep the goal extreme by always being ready to evict the worst-kept. Skipped sqrt (x^2+y^2 monotonic). Index tiebreaker in (-dist,i). Vocab: parsimonious. Replaced k_closest_to_origin.py with the bounded version.

### 2026-06-15 18:48 · LC215 Kth Largest Element in an Array · conf 4/5  (Heap / PQ, M)
`kth_largest.py`  
First heap problem. Correct unaided with a heap, but used full-heap-then-trim (push all n, pop while >k) = O(n log n). One tip: pop INSIDE the loop to keep the heap bounded at size k -> O(n log k), the actual idiom (and stream-friendly). Self-applied the fix immediately. Concept lock: min-heap of size k holds the k LARGEST; root = k-th largest (the inversion). Toolkit: heappushpop, heapq.nlargest, heapify O(n), quickselect alt. History: binary heap = Williams + Floyd 1964 (from heapsort).

### 2026-06-15 18:39 · LC567 Permutation in String · conf 3/5  (Sliding Window, M)
`permutation_in_string.py`  
Fixed-size sliding window (new shape). First version recomputed Counter(slice) every step (O(n*m)) AND missed the last window (while right < len(s2), classic fencepost again). Two hints: (1) off-by-one on the loop bound, (2) restructure to ONE incremental counter (add entering, drop leaving). Restructuring fixed both at once. Nailed the Counter zero-key gotcha (del keys at 0 or == breaks). Clean O(n) after. Lesson: real sliding window keeps one counter alive, never rebuilds.

### 2026-06-14 20:29 · LC424 Longest Repeating Character Replacement · conf 3/5  (Sliding Window, M)
`longest_repeating_char_replacement.py`  
Longest-valid window with a RICHER state (frequency map, not a single counter). Got the basic shape unaided but first tried an incremental 'changes' counter that drifted because d_max keeps moving (overcounted AABABBA). One conceptual hint: drop the counter, compute replacements directly as window_length - max(d.values()); decrement d on shrink; always advance left. Then clean. LESSON: if a running counter depends on a value that itself changes, recompute don't increment. Also learned the never-decrease-max_freq O(n) optimization (subtle but correct) and why the clear O(26n) version is better to store.

### 2026-06-14 19:50 · LC1004 Max Consecutive Ones III · conf 4/5  (Sliding Window, M)
`max_consecutive_ones.py`  
COLD RE-REVIEW, huge jump from conf-1 (needed full skeleton) to writing the entire thing from first principles unaided. Correct expand/shrink structure. Only bug: recorded max BEFORE expand+shrink (measured un-validated windows -> [0] k=0 gave 1 not 0). Self-fixed off a single failing-case hint by moving record to the BOTTOM. Lesson now owned: order is EXPAND -> SHRINK-while-invalid -> RECORD-when-valid. Sliding window finally clicking. Biggest improvement of any pattern.

### 2026-06-14 19:26 · LC1011 Capacity To Ship Packages Within D Days · conf 4/5  (Binary Search, M)
`capacity_to_ship_packages.py`  
The one that got away at a Meta interview, now owned. Wrote it from the predicate idea (primed: had just seen Koko + the mapping). Binary search on the answer: space [max(weights), sum(weights)], greedy can_ship day-count, keep-mid. Self-caught the numDays=0->1 fencepost (days = resets + 1, already on day 1). Same machine as Koko 875; only feasible() differs. Pattern (binary-search-on-answer / parametric search) finally clicked. Canonical cousins: Split Array Largest Sum 410.

### 2026-06-14 00:04 · LC875 Koko Eating Bananas · conf 3/5  (Binary Search, M)
`koko_bananas.py`  
Binary search on the answer. Got the CONCEPTUAL LEAP unaided: recognized it as searching the answer space, built [1,max(piles)] range and the feasible() predicate himself (the hard part). One hint on the strict-vs-inclusive boundary AGAIN (curr_time < h -> <= h; 'within h hours' includes exactly h). Recurring signature bug: strict vs inclusive. Improvements taught: integer ceil (a+b-1)//b not float (precision at 1e9), name predicate feasible()->bool. History: parametric search (Megiddo 1983). Wants Capacity to Ship next (same pattern, missed the trick in a past Meta interview).

### 2026-06-13 21:54 · LC153 Find Minimum in Rotated Sorted Array · conf 4/5  (Binary Search, M)
`find_min_rotated.py`  
Correct unaided code (boundary/keep-mid convention: while low<high, high=mid not mid-1, low=mid+1, compare nums[mid] vs nums[high]). Correctly reached for the harder keep-mid convention. BUT picked the nums[high] anchor partly from my hint, not derived -> honest 4. Taught the FUNDAMENTAL view: binary search finds the first True in a monotonic F...T predicate; here P(i)=nums[i]<=nums[high] (i in tail run with the min). Anchor rule: compare to the endpoint guaranteed to be on the side of what you seek. This predicate framing sets up binary-search-on-answer next.

### 2026-06-12 16:16 · LC704 Binary Search · conf 5/5  (Binary Search, E)
`binary_search.py`  
Vanilla binary search, clean airtight unaided solve. Closed-interval [low,high] used consistently: while low<=high, low=mid+1/high=mid-1, return -1. All boundary decisions correct (empty array, single element, both ends). Deliberately drilling binary search to lock margin discipline after the LC33 saga. Tip taught: pick ONE interval convention and never mix. Toolkit: bisect_left for prod. Next escalate to Find Min Rotated (153) then binary-search-on-answer (Koko).

### 2026-06-12 16:04 · LC33 Search in Rotated Sorted Array · conf 3/5  (Binary Search, M)
`search_rotated_array.py`  
COLD RE-REVIEW, big improvement from the conf-2 4-iteration saga last time. Mechanics now in muscle memory unaided: single loop, mid==target first, inclusive <=, no slicing, return -1. Needed ONE hint: missed the 'which half is sorted' branch (nums[low]<=nums[mid]) -- had collapsed to left-sorted-only. Then SELF-CORRECTED the right-half boundary < nums[high] -> <= nums[high] before I ran it. Spaced-rep payoff visible. User rates the floor (conservative) on purpose. Two-level template (which-half-sorted, then range-check) is landing.

### 2026-06-11 23:43 · LC11 Container With Most Water · conf 5/5  (Two Pointers, M)
`container_with_water.py`  
Clean unaided solve, the trickier converging problem. Converging pointers, area=(hi-lo)*min(walls), move the shorter wall. Correct O(n)/O(1) vs brute O(n^2). Got the greedy instinct right. Tip taught: exchange argument (moving the taller wall loses width with same cap -> can't improve -> move shorter). Toolkit: ties safe either way, micro-opt skip-shorter exists but not needed. History: modern problem; proof technique is the exchange argument behind Huffman 1952 / Kruskal 1956. Two-pointer converging flavor solid (167 and 11 both clean 5s).

### 2026-06-11 22:42 · LC167 Two Sum II — Input Array Is Sorted · conf 5/5  (Two Pointers, M)
`two_sum_sorted.py`  
First two-pointer problem, clean unaided solve. Converging pointers on sorted array: total>target -> hi--, else lo++, equal -> return 1-based. Correct, O(n)/O(1). Stated the move logic. Tip taught: the safety argument (lo paired with largest still short -> lo never reaches target -> discard). Toolkit: defensive return [], sorted->two-pointer vs unsorted->hashmap. History: merge-sort merge (von Neumann 1945) is the ancestor; Floyd tortoise-hare for fast/slow. Strong start to the pattern.

### 2026-06-11 22:18 · LC207 Course Schedule · conf 3/5  (Graphs, M)
`course_scheduler.py`  
First-ever attempt at topological sort. Wrote the entire Kahn's BFS loop correctly and unaided (pop, completed++, decrement neighbors, enqueue on 0, completed==numCourses). Needed 2 setup nudges: (1) edge direction (wrote adj[a].append(b) instead of adj[b].append(a) -> decremented prereqs not dependents), (2) seed list iterated indeg VALUES not indices (needs enumerate). Both setup, not algorithmic. Clean canonical solution. Now one line from Course Schedule II / 210 (append to order list instead of counting). Strong first exposure.

### 2026-06-11 18:33 · LC994 Rotting Oranges · conf 3/5  (Graphs, M)
`rotten_oranges.py`  
Multi-source BFS STRUCTURE correct on first attempt, unaided: seeded all rotten sources, level-snapshot per minute, fresh counter, impossible-check at end. That conceptual design is the hard part and it was solid. But output was -1 (fully wrong) due to 4 execution bugs needing hints: used current (i,j) instead of neighbor (ni,nj) in 3 spots (the check, the rot, the enqueue), == instead of = for the rot assignment, and >1 instead of >0 in the final impossible-check. Cleaner idiom to internalize: 'while q and fresh > 0' guard removes the off-by-one (no early return + unconditional tim+=1). Tired-slip cluster; redo cold in ~1 week.

### 2026-06-11 11:28 · LC695 Max Area of Island · conf 5/5  (Graphs, M)
`max_area_of_island.py`  
Solved correctly first try, unaided, using mutate-as-visited + accumulator style. Then proactively proposed a cleaner refactor: explicit max_area var + double loop + dfs returning the blob area (1 + sum of neighbor dfs), preferring readability over the generator one-liner. Good code-clarity judgment emerging. Graphs transferring well from tree DFS; return-value flood-fill is the idiom to keep using.

### 2026-06-10 22:23 · LC200 Number of Islands · conf 3/5  (Graphs, M)
`no_of_islands.py`  
Flood-fill structure (scan -> count unvisited land -> flood rest) was theirs from the start. 2 hints, both same root: visited stores COORDINATES not cell values -> used grid[i][j] (the char) where (i,j) was needed, in BOTH the outer scan and valid(). Crash was the classic missing-visited-guard cycle (graph vs tree). Count-in-outer-loop, flood-marks-rest: correct. Asked for boilerplate-efficiency tricks (felt their version verbose: passed grid around, separate valid()).

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
