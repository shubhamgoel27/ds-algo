# Binary Search

## The engine in one sentence
Binary search isn't "search a sorted array" — it's "I have a monotonic yes/no predicate over a range, and I want the boundary where it flips." Every probe throws away half the range, so it fires whenever you can answer "is the answer ≤ mid?" in one shot.

## The one question that unlocks it
Stop thinking "where is my target?" Ask:
**"What's the predicate `feasible(mid)` that is False...False...True...True across my range, and which side of the flip do I want?"**
Once you can write a monotonic `feasible(x)`, the search space stops being an array — it can be the answer itself (a speed, a capacity, a count). That reframe is the entire reason Koko and Capacity-to-Ship are the same problem as LC704.

## The mental model
There are two flavors, but they're the same machine. The array is just the easy case where `feasible(i)` is `nums[i] >= target`.

```
 search-on-ARRAY:    indices 0..n-1, predicate = nums[mid] vs target
 search-on-ANSWER:   values lo..hi,  predicate = feasible(mid) ?

 The predicate is ALWAYS monotonic:
   index/value:   0   1   2   3   4   5   6   7   8
   feasible(x):   F   F   F   F   T   T   T   T   T
                              ^^^^^
                          the boundary you want
```
You are never "looking for a value." You are **finding the boundary between the F-region and the T-region.** `lo`/`hi` are walls closing in on that seam.

```visual
type: state-machine
title: The monotonic predicate boundary
shows: that binary search collapses a range onto the single point where a monotonic predicate flips False→True, and that lo/hi converge on the first True
elements: a horizontal strip of 9 cells indexed 0..8; cells 0-3 red labeled "False (not feasible / nums<target)"; cells 4-8 green labeled "True (feasible / nums>=target)"; a thick vertical seam between cell 3 and cell 4 labeled "answer = first True"; two arrows lo→ from the left and hi← from the right both converging on the seam; caption "we return lo, which lands on the first True"
```

## The universal template

**Template A — search on an array (find exact target / a boundary):**
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1          # ← inclusive bounds [lo, hi]
    while lo <= hi:                    # ← <= because hi is inclusive
        mid = (lo + hi) // 2           # ← in Python, no overflow worry
        if nums[mid] == target:        # ← the CLEAN hit check
            return mid
        elif nums[mid] < target:       # ← route: discard left half
            lo = mid + 1
        else:                          # ← route: discard right half
            hi = mid - 1
    return -1                          # ← lo is the insertion point if you need it
```

**Template B — search on the answer space (minimize-the-max / smallest feasible X):**
```python
def min_feasible(lo, hi):
    def feasible(x):                   # ← THE monotonic predicate (False→True)
        ...                            #   return True if x is "big/slow enough"
        return True

    while lo < hi:                     # ← < (not <=): collapse to one survivor
        mid = (lo + hi) // 2           # ← bias LOW; pairs with hi = mid
        if feasible(mid):
            hi = mid                   # ← mid might be the answer, KEEP it
        else:
            lo = mid + 1               # ← mid fails, discard it
    return lo                          # ← lo == hi == first True
```
Three decisions for B: the **[lo, hi] answer range**, the **`feasible` predicate**, and confirming it's **monotonic** (if `x` works, every `x' > x` works too). The loop never changes.

## Variants / when to use
| Variant | Predicate / signal | Loop & return | Catalog |
|---|---|---|---|
| Exact target | `nums[mid] == target` | `lo<=hi`, return mid | LC704 |
| Find boundary / min element | compare `mid` vs `hi` | `lo<hi`, return `lo` | LC153 |
| Rotated, find target | detect the **sorted half** first | `lo<=hi` | LC33 |
| Local condition (no global sort) | compare `mid` vs `mid+1` | `lo<hi` | LC162 |
| 2D as flattened 1D | map `mid → (r,c)` | `lo<=hi` | LC74 |
| On the answer | `feasible(mid)` monotonic | `lo<hi`, return `lo` | LC875, LC1011 |
| Prefix-sum + bisect | cumulative weights | `bisect_left` | LC528 |

## Worked example
**LC875 Koko Eating Bananas** — the canonical search-on-answer. Koko picks an eating speed `k`; with `piles`, eating each pile takes `ceil(pile/k)` hours. Find the **smallest** `k` that finishes within `h` hours.

The reframe: speed is monotonic. Faster `k` ⇒ fewer (or equal) hours. So `hours(k) <= h` is `False...False...True...True` over `k`. We want the **first True**.

```python
import math
def minEatingSpeed(piles, h):
    def feasible(k):                          # monotonic in k
        return sum(math.ceil(p / k) for p in piles) <= h
    lo, hi = 1, max(piles)                    # k=1 slowest, k=max finishes in len(piles)<=h hrs
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid                          # this speed works, maybe slower also works
        else:
            lo = mid + 1                      # too slow, need faster
    return lo
```
Trace on `piles=[3,6,7,11], h=8`. Predicate `feasible(k)` = total hours ≤ 8:
```
k :  1   2   3   4   5   6   7   8 ... 11
F?:  F   F   F   T   T   T   T   T ...  T     (boundary at k=4)

lo=1, hi=11
  mid=6  feasible(6)=ceil(3/6+6/6+7/6+11/6)=1+1+2+2=6<=8 → T  hi=6
lo=1, hi=6
  mid=3  hours=1+2+3+4=10<=8 → F            lo=4
lo=4, hi=6
  mid=5  hours=1+2+2+3=8<=8  → T            hi=5
lo=4, hi=5
  mid=4  hours=1+2+2+3=8<=8  → T            hi=4
lo=4, hi=4  → exit, return 4
```
You never sorted speeds or stored a range — you just asked `feasible(mid)` and routed. Same skeleton solves **LC1011** verbatim: range is `[max(weights), sum(weights)]`, and `feasible(cap)` = "greedily packing days at this capacity needs ≤ D days."

## Gotchas
These three own this pattern. Burn them in.

- **Inclusive vs strict in rotated search (LC33/LC153).** Detect the sorted half with `nums[lo] <= nums[mid]` — the `<=` is *load-bearing*. When the window shrinks to size 2 (`mid == lo`), `nums[lo] < nums[mid]` is false, so a strict `<` misclassifies the left half as unsorted and you branch wrong. Use inclusive `<=`:
  ```python
  if nums[lo] <= nums[mid]:        # left half [lo..mid] is sorted
      if nums[lo] <= target < nums[mid]: hi = mid - 1
      else:                              lo = mid + 1
  else:                            # right half [mid..hi] is sorted
      if nums[mid] < target <= nums[hi]: lo = mid + 1
      else:                              hi = mid - 1
  ```
- **Never slice.** `nums[lo:mid+1]` *copies* O(n) elements every iteration — that silently turns your O(log n) into O(n log n) and defeats the whole point. **Pass indices**, compare `nums[mid]` in place. The array never moves.
- **Boundaries should only ROUTE, never decide.** Keep the *answer* check clean and separate from the *which-half* check. In LC704 the hit is `nums[mid] == target` (decides), and `<`/`>` only route. In Template B, `feasible(mid)` decides; `lo`/`hi` updates only route. Mixing them is how you get the classic infinite loop.
- **Off-by-one in the loop shape.** `lo <= hi` with `mid±1` on *both* sides terminates (Template A). `lo < hi` with `hi = mid` (no −1!) is the convergence form (Template B/LC153) — if you write `hi = mid - 1` there you can skip the answer. Pick a template and don't blend them.

## Python idioms
- `mid = (lo + hi) // 2` — Python ints are bignum, so no C-style overflow. Still, `lo + (hi - lo) // 2` is the portable habit.
- `bisect` module is binary search as stdlib: `bisect_left(a, x)` = first index with `a[i] >= x` (the F→T boundary!), `bisect_right(a, x)` = first index `> x`. **LC528 Random Pick with Weight** is exactly this: build a prefix-sum array, draw `target = random.uniform(0, total)`, return `bisect.bisect_left(prefix, target)` — O(log n) per pick after O(n) setup.
  ```python
  import bisect, random
  class Solution:
      def __init__(self, w):
          self.prefix = list(itertools.accumulate(w))   # cumulative weights
      def pickIndex(self):
          x = random.uniform(0, self.prefix[-1])
          return bisect.bisect_left(self.prefix, x)      # heavier index = wider band
  ```
- `math.ceil(p / k)` for hours-style predicates — or integer `-(-p // k)` to dodge float error on huge inputs.
- 2D→1D flatten (LC74): `r, c = divmod(mid, cols)` lets you binary-search an `m×n` matrix as one length-`m*n` array.
- `random.choices(population, weights=w)` exists, but interviewers want the prefix-sum + bisect build for LC528 — show the mechanism.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 704 | Binary Search | E | Template A; predicate `nums[mid]==target`; `<`/`>` route; return mid |
| 33 | Search in Rotated Sorted Array | M | Template A; detect sorted half with inclusive `nums[lo]<=nums[mid]`, then range-check target |
| 74 | Search a 2D Matrix | M | Template A on flattened `[0, m*n-1]`; `divmod(mid, cols)` → `(r,c)` |
| 153 | Find Minimum in Rotated Sorted Array | M | Template B shape; predicate `nums[mid] > nums[hi]` (min is right); `lo<hi`, `hi=mid`, return `nums[lo]` |
| 162 | Find Peak Element | M | Template B; compare `nums[mid]` vs `nums[mid+1]`; ascending ⇒ peak right (`lo=mid+1`), else `hi=mid` |
| 528 | Random Pick with Weight | M | prefix-sum array + `bisect_left(prefix, uniform(0,total))`; heavier weight = wider band = higher pick odds |
| 875 | Koko Eating Bananas | M | Template B on speed `[1, max(piles)]`; `feasible(k)=sum(ceil(p/k))<=h`; return smallest True |
| 1011 | Capacity To Ship Packages Within D Days | M | Template B on capacity `[max(w), sum(w)]`; `feasible(cap)`=greedy day-count `<= D`; return smallest True |
