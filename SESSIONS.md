# Session Journal — what tripped me, per attempt

> Auto-generated from `review.json` history by `review.py gen`. Newest first. Read this at the start of a session to target weak spots.

Total attempts logged: **2**.

---

### 2026-06-07 · LC146 LRU Cache · conf 3/5  (Design, M)
`lru_cache.py`  
Design 100% correct (hashmap+DLL, dummy sentinels, key stored on node). But 3 impl bugs, one fatal: (1) put created the node TWICE -> dict and list referenced different objects -> get crashed on None.prev. (2) remove_tail defined with stray 'node' param but called with none. (3) del self.cache[key] used undefined name; should be lru.key (this is WHY key is stored on node). Abstraction lesson: unlink surgery was duplicated in move_to_head AND remove_tail -> extract atomic _remove(node) primitive, compose everything from _remove + _add_front. Helpers were conceptually right, just redundant + buggy. WATCH: DLL pointer surgery, and 'stored the data but forgot to use it'.

### 2026-06-06 · LC56 Merge Intervals · conf 5/5  (Intervals, M)
`merged_intervals.py`  
Clean optimal solve, essentially identical to saved 2024 soln (sort → sweep → merge on curr_start<=prev_end, max of ends). Minor: loop ran from i=0 (redundant self-compare) — use intervals[1:]. Solid muscle memory.
