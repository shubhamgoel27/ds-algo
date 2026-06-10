# Heap / Priority Queue

## The engine in one sentence
A binary heap is a "give me the extreme element, fast" box: O(log n) push and pop of the min (or max), O(1) peek — it fires whenever you repeatedly need *the smallest/largest right now* but don't need the whole thing sorted.

## The one question that unlocks it
Sorting gives you *every* order relationship for O(n log n). A heap asks: **"do I actually need the full order, or just the one extreme, again and again?"** If it's the latter, you're overpaying with a sort. Each `heappop` costs O(log n) and hands you exactly the next extreme — pay only for the extremes you consume.

And the idiom that trips everyone up: for **top-k**, the heap holds the *opposite* extreme of what you want. Want the k **largest**? Keep a **min**-heap of size k. The heap's root is the *smallest of your current winners* — your bouncer at the door. Any new element only earns a spot by beating that weakest winner.

## The mental model
Two axes. First: which extreme, and remember Python's `heapq` is **always a min-heap** — for a max-heap you push **negatives**.
```
heapq = MIN-heap          max-heap = push -x, negate on the way out
heap[0] = smallest        -heap[0] = largest
```
Second, and this is the load-bearing insight — the **bounded heap inversion** for top-k:
```
GOAL: k LARGEST          →  keep a MIN-heap of size k
   root = smallest winner (the threshold to beat)
   new x:  push x; if len > k: pop  →  evicts the smallest, keeps top-k

GOAL: k SMALLEST / closest →  keep a MAX-heap of size k  (push -x)
   root = largest winner (the worst of the keepers)
```
You keep the *enemy* of your goal at the root so it's cheap to evict the weakest survivor. After scanning n items, the size-k heap *is* your answer.

```visual
type: state-machine
title: Bounded min-heap for "k largest" (k=3)
shows: how a size-3 min-heap keeps the 3 largest of a stream by popping its own root (the smallest winner) whenever it overflows
elements: stream 5,1,8,3,9,2 entering left-to-right; a box labeled "min-heap, cap 3" with root highlighted as "threshold = smallest winner"; for each push show push-then-pop-if-overflow; final state {5,8,9} with root=5; caption "root is the kth largest"
```

## The universal template
**Bounded heap (top-k).** Want k largest → min-heap; want k smallest → max-heap (negate).
```python
import heapq

def top_k(nums, k):
    heap = []                          # ← MIN-heap; holds the k LARGEST so far
    for x in nums:                     # ← x = comparison key (could be a tuple)
        heapq.heappush(heap, x)        #    for k-smallest: push (-key) or use a max convention
        if len(heap) > k:              # ← invariant: never exceed k
            heapq.heappop(heap)        #    evict the smallest winner
    return heap                        # ← the k largest; heap[0] is the k-th largest
```
Three decisions: **which extreme** (min vs max → negate or not), **the key** you order by (raw number, or a tuple like `(dist, point)`), and **k** (the cap that makes it bounded).

**Two heaps (running median).** A max-heap for the lower half, a min-heap for the upper half, kept balanced so the median sits at one or both tops.
```python
class MedianFinder:
    def __init__(self):
        self.lo = []   # ← MAX-heap (push negatives): the smaller half
        self.hi = []   # ← MIN-heap: the larger half

    def addNum(self, x):
        heapq.heappush(self.lo, -x)                  # tentatively add to lower half
        heapq.heappush(self.hi, -heapq.heappop(self.lo))  # move lo's max → hi (keeps order)
        if len(self.hi) > len(self.lo):              # rebalance: lo may carry the extra
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]                        # odd count → lower half holds it
        return (-self.lo[0] + self.hi[0]) / 2         # even → average of both tops
```
Invariant: every element in `lo` ≤ every element in `hi`, and `len(lo) == len(hi)` or `len(lo) == len(hi)+1`.

## Variants / when to use
| Variant | Heap setup | Fires when |
|---|---|---|
| **k largest** | min-heap, cap k | "kth largest", "k largest", largest-k stream |
| **k smallest / closest** | max-heap (negate), cap k | "k closest", "k smallest" — invert the keys |
| **Greedy scheduling** | max-heap of counts | repeatedly grab the most-frequent available item |
| **Two heaps** | max-heap (low) + min-heap (high) | running median / split a stream at the middle |
| **Heap-select vs sort** | min-heap cap k | k ≪ n → O(n log k) beats O(n log n) sort |

## Worked example
**LC973 K Closest Points to Origin** — want the k *smallest* distances, so by the inversion you keep a **max-heap of size k** (push negative distance). Root = the *farthest* of your current keepers; a new point only stays if it's closer than that worst keeper.
```python
def kClosest(points, k):
    heap = []                                   # max-heap via negative distance
    for x, y in points:
        d = x*x + y*y                           # squared dist — no sqrt needed
        heapq.heappush(heap, (-d, x, y))        # negate → farthest sits at root
        if len(heap) > k:
            heapq.heappop(heap)                 # evict the farthest keeper
    return [[x, y] for _, x, y in heap]
```
Trace on `points = [(1,3),(−2,2),(2,−2),(5,5)]`, `k = 2`. Distances²: (1,3)=10, (−2,2)=8, (2,−2)=8, (5,5)=50. Heap shown as the negatives it actually stores (root = most-negative = farthest):
```
push (1,3) d=10      heap = [-10]                      (size 1)
push (-2,2) d=8      heap = [-10, -8]                  (size 2)
push (2,-2) d=8      heap = [-10, -8, -8] → size 3 > 2
                     pop root -10 (farthest)  heap = [-8, -8]
push (5,5) d=50      heap = [-50, -8, -8] → size 3 > 2
                     pop root -50 (farthest)  heap = [-8, -8]
result = (-2,2) and (2,-2)   ← the two closest
```
You never sorted all four points — each scan did one push and an O(log k) evict, total O(n log k).

For **LC215 / LC703** the inversion flips: those want k *largest*, so the same template runs as a **min-heap** cap k, and `heap[0]` is the kth largest (703 just keeps that heap alive across a stream of `add` calls).

## Greedy scheduling (max-heap)
**LC621 Task Scheduler** and **LC767 Reorganize String** share a shape: at each step, **emit the highest-frequency item still available**, then make it temporarily unavailable so you can't pick it twice in a row. Max-heap on counts.
```python
def reorganizeString(s):
    from collections import Counter
    heap = [(-c, ch) for ch, c in Counter(s).items()]  # max-heap by count
    heapq.heapify(heap)
    res, prev = [], None                # prev = the char we just used (cooling down)
    while heap:
        c, ch = heapq.heappop(heap)     # most frequent available
        res.append(ch)
        if prev: heapq.heappush(heap, prev)   # release the one cooled from last step
        prev = (c + 1, ch) if c + 1 != 0 else None  # decrement (c is negative)
    return "".join(res) if len(res) == len(s) else ""
```
The "hold one aside" trick enforces the no-adjacent-duplicates / cooldown gap: you can't re-push the just-used item until after the next pick.

## Two-heaps balance (median)
```visual
type: before-after
title: Two heaps keep the median pinned at the tops
shows: a stream split into a max-heap (lower half) and min-heap (upper half), balanced so the median is one top or the average of two tops
elements: left box "max-heap lo" containing {1,2} top=2; right box "min-heap hi" containing {3,4} top=3; arrow between tops labeled "median = (2+3)/2"; below show adding 5 → goes to hi, then rebalance so lo={1,2,3} hi={4,5}, median=3
```
ASCII of the same idea:
```
lo (max-heap)        hi (min-heap)
  [2, 1]      |        [3, 4]
   top=2      |         top=3
        median = (2 + 3) / 2 = 2.5
add 5 → hi, sizes uneven, rebalance:
  [3,2,1]     |        [4, 5]
   top=3      |              →  median = 3   (lo holds the extra)
```

## Gotchas
- **The inversion direction.** k largest → MIN-heap; k smallest/closest → MAX-heap. Pick the wrong one and you evict your winners. Burn in: *the heap holds the threshold, i.e. the weakest survivor, which is the opposite extreme of your goal.*
- **`heapq` is min-only.** No `max=True` flag. Max-heap = push `-x` (numbers) or `(-key, payload)` (tuples), and remember to negate back on the way out.
- **Tuple comparison ties.** Storing `(-d, x, y)` works because Python compares tuples lexicographically — but if a payload isn't comparable (e.g. a custom object after equal keys), it raises. Add a tie-breaker like an insertion counter.
- **Two-heaps off-by-one.** Decide which heap carries the extra element on odd counts (here: `lo`), and make `findMedian` consistent with it. Mismatched convention = wrong median on odd lengths.
- **`heapify` vs n pushes.** `heapq.heapify(list)` is O(n); pushing n items one by one is O(n log n). Heapify when you already have the whole list.

## Python idioms
- `heapq.heappush(h, x)` / `heapq.heappop(h)` — O(log n); `h[0]` peeks the min in O(1).
- `heapq.heapify(lst)` — O(n) in-place; turn a list into a heap.
- `heapq.heappushpop(h, x)` — push then pop in one O(log n) op; ideal for the bounded-heap loop (`heappushpop` when already at size k avoids a transient k+1).
- `heapq.nlargest(k, it, key=...)` / `nsmallest` — the bounded-heap pattern packaged: O(n log k), and they take a `key`.
- Max-heap: push `-x`; for objects, push `(-priority, tiebreak, obj)`.
- `collections.Counter(s)` → frequencies, then a list comprehension into a heap for greedy scheduling.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 703 | Kth Largest in a Stream | E | bounded MIN-heap cap k; `heap[0]` is the answer; `add` pushes + pops if >k |
| 215 | Kth Largest in an Array | M | bounded MIN-heap cap k → O(n log k); root = kth largest |
| 973 | K Closest Points | M | bounded MAX-heap cap k (push `(-dist, x, y)`); evict farthest; **inversion** |
| 621 | Task Scheduler | M | max-heap on counts; greedily emit most-frequent, hold cooling tasks aside |
| 767 | Reorganize String | M | max-heap on counts; emit most-frequent, re-push previous each step (no adjacency) |
| 295 | Find Median from Data Stream | H | two heaps: max-heap (lower) + min-heap (upper), kept balanced; median at top(s) |
