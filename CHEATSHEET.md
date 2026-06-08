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
