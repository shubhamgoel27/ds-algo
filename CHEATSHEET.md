# Interview Cheat-Sheet — patterns & solved problems

Concise, scannable revision notes. **Read this before interviews.** One block per problem:
the key insight, the approach, complexity, the gotcha that bites, and the Python idiom worth
knowing. Grouped by pattern. Updated every review session.

> Companion files: `REVIEW.md` (what's due) · `SESSIONS.md` (what tripped me last time) · this (how to solve).

---

## Stack
**Reach for it when:** nesting / matching, "most-recently-seen" semantics, or monotonic-stack range problems. LIFO mirrors nesting.

### LC20 · Valid Parentheses · E
- **Idea:** push every opener; on a closer, pop and check it matches. Valid ⟺ stack empty at the end.
- **Approach:** map `closer → opener`. `for c: if closer → (stack empty or pop != match) ⇒ False, else push`. Return `not stack`.
- **Complexity:** O(n) time, O(n) space.
- **Gotcha:** closer on an empty stack ⇒ False. Three rules = three checks (empty-on-close, top-mismatch, leftover-at-end).
- **Python:** a `list` *is* a stack (`append`/`pop` O(1) at tail; `pop(0)` is O(n) — never). `not stack` for empty. `dict(zip(a,b))` to build a map. Membership → dict/set (O(1)), not list (O(n)).
- **Deeper:** balanced parens is *not regular* — regex can't do unbounded nesting; you need a stack (→ context-free / pushdown automaton).

---

## Intervals
**Reach for it when:** overlapping ranges. **Almost always sort by start first**, then sweep keeping minimal state (sweep-line).

### LC56 · Merge Intervals · M
- **Idea:** after sorting by start, you only ever compare against the **last** merged interval — nothing earlier can overlap if that one doesn't.
- **Approach:** `sort by start`; `final=[first]`; for each, if `cur.start <= final[-1].end` → `final[-1].end = max(end, cur.end)`, else append.
- **Complexity:** O(n log n) (sort dominates), O(n) space.
- **Gotcha:** touching endpoints count as overlap → use `<=`. Clarify this out loud.
- **Python:** `sorted()` returns a copy (no input mutation); `.sort()` mutates the arg — mention you avoid mutating inputs. Timsort is adaptive (≈O(n) on sorted data) + stable.
- **Family (same skeleton):** Insert Interval (57), Non-overlapping Intervals (435), Meeting Rooms II (253).

---

## Binary Search
**Reach for it when:** sorted (or rotated-sorted) data + need better than O(n). The art is the loop invariant and inclusive-vs-strict boundaries.

### LC33 · Search in Rotated Sorted Array · M  ⚠️ high-miss
- **Idea:** one binary search. At each `mid`, **at least one half `[lo..mid]` / `[mid..hi]` is cleanly sorted** (pivot is in the other). Find the sorted half; if target is in its range, go there, else the other half.
- **Approach:** check `nums[mid]==target` first. Then `if nums[lo] <= nums[mid]:` left sorted → go left iff `nums[lo] <= target < nums[mid]`, else right. Else right sorted → go right iff `nums[mid] < target <= nums[hi]`, else left.
- **Complexity:** O(log n) time, O(1) space.
- **Gotcha #1 (the one that bites):** detect the sorted half with **`<=` (inclusive)** — when the window is 1–2 elements `mid==lo`, strict `>` misclassifies and you miss present targets.
- **Gotcha #2:** **never slice** (`nums[lo:mid+1]`) — it copies O(n), silently breaking the O(log n) bound. Pass indices.
- **Gotcha #3:** check `nums[mid]==target` at the top so the boundary comparisons only *route*, never *find* → kills off-by-ones. End with `return -1`.
- **Python:** `(lo+hi)//2` is overflow-safe in Python (bigints); write `lo+(hi-lo)//2` in C++/Java. Chained `a <= x < b` is one-shot and idiomatic.

---

## Linked List
**Reach for it when:** pointer manipulation. The universal rule: **save `next` before you overwrite it.** Most hard problems decompose into reverse + two-pointer (fast/slow).

### LC206 · Reverse Linked List · E
- **Idea:** three pointers. Invariant: `prev` = already-reversed prefix, `curr` = untouched suffix. Peel one node at a time.
- **Approach:** `prev=None, curr=head`; loop: `temp=curr.next; curr.next=prev; prev=curr; curr=temp`. Return `prev`.
- **Complexity:** O(n) time, O(1) space. (Recursive: O(n) stack.)
- **Gotcha:** must save `curr.next` *before* `curr.next=prev`, else the suffix is lost. Empty list handled naturally (returns `None`).
- **Python:** one-liner `curr.next, prev, curr = prev, curr, curr.next` (RHS evaluated first). Use `while curr is not None` for pointer checks.
- **Builds:** Reverse in k-Groups (25), Reverse Sublist (92), Palindrome List, Reorder List.

---

## Design
**Reach for it when:** "implement X with O(1) operations." Usually = combine a hashmap (O(1) lookup) with a structure that gives O(1) ordering.

### LC146 · LRU Cache · M
- **Idea:** hashmap `key→node` (O(1) lookup) + **doubly-linked list** ordered by recency (O(1) move/evict). Each covers the other's weakness.
- **Approach:** dummy head (MRU) & tail (LRU) sentinels. `get`/`put` → move node to front; over capacity → evict `tail.prev`. **Node stores its key** so eviction can `del cache[node.key]` in O(1).
- **Complexity:** O(1) get and put.
- **Gotcha:** build the node **once** (same object in dict *and* list, or `get` crashes on a node with null pointers). Extract one atomic `_remove(node)` + `_add_front(node)`; compose everything — don't duplicate pointer surgery.
- **Python:** `OrderedDict` gives a ~10-line LRU (`move_to_end`, `popitem(last=False)`, both O(1)). `functools.lru_cache` is this in C. Plain dict is insertion-ordered (3.7+) but has no O(1) bump-to-end.
- **Why doubly linked:** need the predecessor pointer to unlink an arbitrary node in O(1).

---

_Last updated: 2026-06-07 (session: Merge Intervals, LRU Cache, Valid Parentheses)._
