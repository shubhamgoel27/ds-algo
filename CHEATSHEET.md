# Interview Cheat-Sheet — patterns & solved problems

Concise, scannable revision notes. **Read this before interviews.** One block per problem:
the key insight, the approach, complexity, the gotcha that bites, and the Python idiom worth
knowing. Grouped by pattern. Updated every review session.

> Companion files: `REVIEW.md` (what's due) · `SESSIONS.md` (what tripped me last time) · this (how to solve).

---

## Backtracking
**Reach for it when:** "generate all / list every / find all combinations-permutations-partitions." It is **DFS over a decision tree**: each node = a partial solution (`path`), each edge = a choice. Skeleton: **record → for each choice: append (choose), recurse (explore), pop (un-choose)**. The `pop` restores state so the next sibling starts clean (the maze: walk back to the junction). Always record a **copy** `path[:]`. Exponential output is expected.

The one knob that changes everything = **what limits the choices / the next state passed down:**
- **Subsets / Combinations:** a `start` index, recurse `i+1` (only go rightward) → no duplicates.
- **Combination Sum (reuse ok):** `start` index but recurse `i` (not `i+1`).
- **Permutations:** a `used[]`/set, any unused element, record at leaves (`len(path)==len(nums)`).
- **Grid (Word Search):** the 4 neighbors + mark/unmark visited.

### LC78 · Subsets · M
- **Idea:** every node of the tree is a subset → record at every node. `start` index forward-only.
- **Body:** `result.append(path[:]); for i in range(start,n): path.append(nums[i]); backtrack(i+1); path.pop()`.

## Heap / Priority Queue
**Reach for it when:** "top k", "k closest/largest/smallest", running median, or repeatedly pulling the min/max. Python `heapq` is a **MIN-heap**; for max-heap push negatives.

### LC215 · Kth Largest Element · M
- **Idea:** bounded **min-heap of size k**. Push each num; pop the smallest when size > k. The k largest survive; the root is the k-th largest.
- **Complexity:** O(n log k) (vs O(n log n) if you heap all n then trim). Works on a stream (LC703).
- **The inversion:** a *min*-heap tracks the *largest* k. Root = smallest of the k largest = k-th largest.
- **Python:** `heappush`/`heappop`; `heappushpop(h,x)` (push+pop in one) once full; `heapq.nlargest(k, nums)[-1]` is the stdlib one-liner; `heapify(lst)` is O(n). Quickselect is the O(n)-average alternative.

### LC621 · Task Scheduler · M  (ready-set + waiting-set)
- **Reach for two containers when:** picking an item **benches it for a while, then it returns**. One heap can't model "hide, then bring back" (it's ordered by priority, not by wake-time). So split: **ready** = max-heap by count; **waiting** = deque of `(count, ready_time)`.
- **Loop:** `while heap or q` (stop only when BOTH empty — the `and`→`or` De Morgan flip). Each tick: wake `q`'s front if `ready_time == sec`, then pop heap top, `+1` (neg counts), requeue with `ready_time = sec + n + 1`; empty heap + non-empty q = **idle**.
- **Why FIFO deque works:** equal cooldowns → tasks wake in insertion order. **Unequal durations (bank/N-agents) → waiting set becomes a HEAP by finish-time.** Same skeleton.
- **Alt:** greedy formula `max((m-1)*(n+1) + k, len(tasks))`, m=max freq, k=#tasks at max. O(n), watch the `max()`.
- **Complexity:** O(T log K), K distinct ≤ 26.

## Sliding Window
**Reach for it when:** longest/shortest/fixed contiguous subarray or substring under a constraint. Rigid loop: **expand always · shrink while invalid · record when valid · no `else` on the current element.** Element updates the state; state drives the decision. O(n) because both pointers only move forward (amortized).

Three shapes:
- **Longest-valid** (LC1004 ≤k zeros, LC424 ≤k replacements): shrink *while invalid*, record *every* step. State can be a counter or a freq map (`window_len - max_freq` for 424).
- **Shortest-valid** (Min Window): expand to valid, then shrink *while valid*, record *when valid*.
- **Fixed-size** (LC567 Permutation in String, LC438 Anagrams): constant width = `len(pattern)`; slide and update **one** counter incrementally (add entering, drop leaving), match when `window == need`.

### LC567 · Permutation in String · M
- **Idea:** fixed window of width `len(s1)`; `need = Counter(s1)`; slide a live `window` Counter, `window == need` means a permutation.
- **Gotcha:** on decrement, **`del` keys that hit 0** or `Counter ==` breaks (`{'a':1,'b':0} != {'a':1}`). Incremental update is O(1)/step; rebuilding `Counter(slice)` each step is O(n·m).

## Arrays & Hashing
**Reach for it when:** you keep re-asking "have I seen X / how many X / which things share a key / what's the complement". A dict/set turns O(n) re-scans into O(1) lookups. Ask: **"what do I wish I could look up in O(1)?"** -> the key is a complement (Two Sum), seen-set (dedup), count (frequency), or a canonical signature (grouping).

### LC49 · Group Anagrams · M
- **Idea:** canonical signature -> bucket. Anagrams share an identical 26-letter count tuple (O(k)) or sorted string (O(k log k)); group by it in `defaultdict(list)`.
- **Gotcha:** a `Counter`/list is unhashable -> use a **tuple** as the dict key. `ord(ch)-ord('a')` for the index.

## Two Pointers
**Reach for it when:** sorted arrays or palindromes (converging from both ends), in-place compaction (read/write), or cycle/middle (fast/slow). The skill is arguing the pointer you *don't* move can be safely discarded.

### LC167 · Two Sum II (sorted) · M
- **Idea:** converging pointers on a sorted array. `total = a[lo] + a[hi]`; too big -> `hi -= 1`, too small -> `lo += 1`, equal -> done.
- **Complexity:** O(n) time, O(1) space (sortedness replaces the hash map's O(n) space).
- **Safety argument:** if `total < target`, `a[lo]` paired with the largest available still falls short, so `lo` can never reach target -> advance it, never revisit. Say this out loud in interviews.
- **Gotcha:** return **1-based** indices here; add a defensive `return []` after the loop.
- **Family:** 3Sum (fix one, two-pointer the rest), Container With Most Water (move the shorter wall), Valid Palindrome, Trapping Rain Water.

### LC11 · Container With Most Water · M
- **Idea:** converging pointers; area = `(hi-lo) * min(h[lo], h[hi])`. Move the **shorter** wall inward each step.
- **Complexity:** O(n) time, O(1) space (vs brute O(n^2)).
- **Why move the shorter wall (exchange argument):** moving the taller wall loses width while the height stays capped by the shorter, so it can never improve. The only hope of a bigger area is replacing the shorter wall. Ties: move either.
- **Family:** the "advance the limiting side" greedy; cousin of Trapping Rain Water.

## Greedy
**Reach for it when:** "max/min contiguous", "fewest/most non-overlapping", "can you reach", "minimum number of". Greedy = DP collapsed to ONE candidate (commit to the local best, never reconsider). Code is trivial; the work is **proving** it. Practical method: **propose a greedy rule, then try to break it with a tiny counterexample.** If it survives, trust it; if not, it's a DP problem (e.g. Coin Change [1,3,4] target 6).

Shapes: running accumulator (Max Subarray, Gas Station) | sort-then-sweep (intervals) | always-take-extreme (heap) | furthest-reach (Jump Game).

### LC53 · Maximum Subarray (Kadane's) · M
- **Idea:** running sum; reset to 0 when it goes negative (a negative prefix only hurts). `best` = max running seen.
- **Gotcha:** record `best` BEFORE the reset, else all-negative arrays wrongly return 0. Seed `best = -inf`.
- **Why safe (exchange):** an optimal subarray never carries a negative-sum prefix; deleting it only raises the sum.
- **= DP** `dp[i]=max(nums[i], dp[i-1]+nums[i])` in O(1) space.


### LC55 · Jump Game · M
- **Idea:** furthest-reach greedy. Track `furthest`; if ever `i > furthest` you hit an uncrossable gap -> False. Else extend `furthest = max(furthest, i+nums[i])`.
- **Why one number suffices:** reachability is **contiguous** (you can jump short), so there are no holes below `furthest`; the only failure is a gap. O(n)/O(1) vs O(n^2) DP.

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

### LC252 · Meeting Rooms · E  (can attend all?)
- **Idea:** sort by start; any conflict is an **adjacent** pair. One scan comparing each start to the previous end. Half-open → strict `<`. Empty/single → True.
- **Complexity:** O(n log n), O(1) extra. Return a count instead of a bool → Meeting Rooms II.

### LC253 · Meeting Rooms II · M  (min rooms = peak concurrency)
- **Idea:** process meetings by **start**, but the only question you ever ask is about **end** — "did the earliest-freeing room free up yet?" That "min of a changing set" = a **min-heap of end times**.
- **Approach:** `sort by start`; `heap=[first.end]`; for each next: if `heap[0] <= start` → `heappop` (reuse room); always `heappush(end)`; answer = `len(heap)`.
- **Why `len(heap)` works:** each iter pushes once, pops at most once → size **never decreases** → final size = peak overlap. Pop at most one because you place one meeting → free at most one room.
- **Complexity:** O(n log n), O(n).
- **Boundary:** half-open `[s,e)` → touching shares a room → strict `rooms[0] <= start`.
- **Alt engine (know both):** +1 at each start, −1 at each end, sort events, running max = concurrency. Generalizes to "how many active at time t." Ties: process −1 before +1.
- **Family:** this IS the reported Pinterest "engagements per interval" question; register allocation / gate scheduling are the same problem.

---

## Binary Search
**Reach for it when:** sorted (or rotated-sorted) data + need better than O(n). The art is the loop invariant and inclusive-vs-strict boundaries.

### LC704 · Binary Search · E  (the template)
- **Idea:** closed interval `[low, high]`, used consistently. Margins come from never mixing conventions.
- **The three decisions:** `while low <= high` (check the 1-element window) · `low=mid+1` / `high=mid-1` (mid already checked; guarantees progress, no infinite loop) · `return -1` when interval empties.
- **Python:** `bisect_left(nums, x)` gives the leftmost insertion index; `i if i<len(nums) and nums[i]==x else -1`. Use it in prod, hand-write in interviews.
- **Rule:** pick `[low, high]` (closed) OR `[low, high)` (half-open) and never mix; mixing = off-by-one / infinite loop.

### LC153 · Find Minimum in Rotated Sorted Array · M
- **Idea:** no target -> binary-search the **boundary of a predicate**. P(i) = `nums[i] <= nums[high]` (i is in the tail run that holds the min). Array reads `F...F T...T`; first True = the minimum.
- **Convention (keep-mid):** `while low < high`; `nums[mid] > nums[high]` -> upper run -> `low = mid+1`; else `high = mid` (mid might BE the min, don't discard). Return `nums[low]`.
- **Anchor rule:** compare against the endpoint guaranteed to be on the side of what you seek (the min lives in the tail, which ends at `high`, so anchor on `nums[high]`, not `nums[low]`).
- **Fundamental:** binary search = find the first True in a monotonic `F...T`. Every BS problem is "what is the predicate?"

### Binary search ON THE ANSWER (LC875 Koko, LC1011 Capacity to Ship)
- **The leap:** no array to search. Search the **space of possible answers**; test a `feasible(x)` predicate at each. Turns an optimization ("min speed / min capacity") into repeated yes/no feasibility checks (parametric search, Megiddo 1983).
- **Koko 875:** space `[1, max(piles)]`; `feasible(speed) = sum(ceil(pile/speed)) <= h`. Answer = smallest feasible speed.
- **Capacity to Ship 1011:** space `[max(weights), sum(weights)]` (low = must fit heaviest; high = ship all in one day); `feasible(cap) = greedy_days(cap) <= days`. Answer = smallest feasible capacity.
- **Shape:** keep-mid (`while low < high`, `if feasible(mid): high=mid else low=mid+1`), return `low` = first feasible.
- **Gotcha:** "within / at most" is **inclusive** (`<= h`). Use **integer ceil** `(a+b-1)//b`, not float `ceil(a/b)`, for big values.

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

## Trees
**Reach for it when:** anything hierarchical. Two engines: **BFS** (level-by-level, queue) and **DFS** (recursion, return value up). Pick by whether you need *levels* (BFS) or *subtree aggregates* (DFS).

### LC102 · Binary Tree Level Order Traversal · M
- **Idea:** BFS, but process **one level at a time** by snapshotting the queue length at each level's start.
- **Approach:** `q=deque([root])`; while q: `n=len(q)` (freeze!), loop `n` times popping left + enqueuing children, collect into a per-level list.
- **Complexity:** O(n) time, O(n) space (widest level).
- **Gotcha:** capture `n=len(q)` **before** the inner loop — you're adding next level's children into the same queue. Empty root → `[]`.
- **Python:** **`deque`** for O(1) `popleft` (a list is O(n)). DFS alt: recurse with `depth`, append to `result[depth]`.
- **Parent pattern for:** Right Side View (199, last per level), Zigzag, Average of Levels, Largest per Level.

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

_Last updated: 2026-07-02 (session: Meeting Rooms I+II, Task Scheduler heap-sim / Pinterest prep)._
