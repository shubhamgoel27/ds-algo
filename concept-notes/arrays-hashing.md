# Arrays & Hashing

## The engine in one sentence
A hash map/set turns "search the array again" (O(n) per lookup) into "ask the dict" (O(1)) — so you trade O(n) memory for O(n²)→O(n) time whenever a problem makes you repeatedly ask *"have I seen X?"*, *"how many X?"*, or *"which things share a key?"*

## The one question that unlocks it
Stop thinking about the array. Ask:
**"What do I wish I could look up in O(1) at each element?"**
The answer is almost always one of four things, and it tells you exactly what the dict's *key* is:
- the **complement** I still need → `key = value` (Two Sum)
- whether I've **seen** this before → `key = value`, set membership (Contains Duplicate)
- a **count** of each thing → `key = item, val = freq` (Anagram, Top-K)
- a **canonical signature** so look-alikes collide → `key = signature` (Group Anagrams)
- a running **prefix sum's frequency** → `key = prefix, val = count` (Subarray Sum = K)

Pick the key, and the loop writes itself: one pass, look up, then insert.

## The mental model
Every problem here is a single linear scan where each element does two things against a dict: **probe** (was the answer already deposited by an earlier element?) then **deposit** (leave something for a later element to find).

```
        scan left → right, dict carries memory of the past
   ┌──────────────────────────────────────────────────────┐
   │  for x in arr:                                        │
   │      PROBE:   answer = dict.get(f(x))   ← past speaks │
   │      DEPOSIT: dict[g(x)] = something    ← leave a clue│
   └──────────────────────────────────────────────────────┘
   The whole trick is choosing f (what you ask) and g (what you key on).
```
Probe-before-deposit vs deposit-before-probe is the entire bug surface: Two Sum must probe for the complement *before* inserting `x`, or `x` matches itself.

```visual
type: pointer-walk
title: Two Sum — probe the complement, then deposit
shows: a single left-to-right pass where each element first looks up (target - x) in the dict, and only if absent inserts itself, so the dict only ever holds strictly-earlier indices
elements: array [2,7,11,15] with target 9; a "seen" dict box growing below; arrow at index 0 shows "need 7? no → put 2:0"; arrow at index 1 shows "need 2? YES → found (0,1)"; highlight that 2 was deposited before 7 probed
```

## The universal template
```python
def solve(arr):
    table = {}                      # ← dict or set; key = the thing you look up
    result = init                   # ← accumulator (count, list, best, ...)
    for i, x in enumerate(arr):
        key   = f(x)                # ← what you PROBE for (complement / signature / x)
        if key in table:            # ← the O(1) win: "have I seen the answer?"
            result = combine(result, table[key], i)   # ← use the past hit
        table[g(x)] = h(x, i)       # ← what you DEPOSIT (value→index, ++count, ...)
    return result
```
Three decisions: **the key** `f`/`g` (value? count? signature? prefix?), **probe vs deposit order**, and **what each entry stores** (an index, a count, a list to group into).

## Variants / when to use
| Sub-pattern | Dict shape | Fires when |
|---|---|---|
| Complement lookup | `value → index` | "find a pair that hits a target" (Two Sum) |
| Seen-set | `set()` membership | "any duplicate / does X exist" (Contains Duplicate, Longest Consecutive) |
| Frequency map | `item → count` | counting, multiset-equality, "top K" (Valid Anagram, Top K Frequent) |
| Canonical-key grouping | `signature → list` | "bucket things that are equivalent" (Group Anagrams, Shifted Strings, Special-Equiv) |
| Grid bucketing | `set` per row/col/box | "no repeats within a region" (Valid Sudoku) |
| **Prefix-sum + map** | `prefix → count` | "subarray summing to K" (Subarray Sum = K) |
| No-dict array trick | prefix/suffix passes | "product/aggregate except self" (Product Except Self) |

## Worked example
**LC560 Subarray Sum Equals K** — the prefix-sum trick that people miss. A subarray `(j, i]` sums to `k` iff `prefix[i] - prefix[j] = k`, i.e. `prefix[j] = prefix[i] - k`. So as you scan, keep a **count of every prefix sum seen so far**; at each `i`, the number of valid subarrays ending here is exactly how many earlier prefixes equal `prefix[i] - k`.

Key = a prefix sum, value = how many times it occurred. Seed `{0: 1}` so a subarray starting at index 0 counts.

```python
def subarraySum(nums, k):
    count = {0: 1}          # prefix sum 0 has occurred once (empty prefix)
    prefix = 0
    res = 0
    for x in nums:
        prefix += x
        res += count.get(prefix - k, 0)   # PROBE: earlier prefixes that complete a k-subarray
        count[prefix] = count.get(prefix, 0) + 1   # DEPOSIT this prefix
    return res
```
Trace on `nums=[1,2,3], k=3`:
```
start: count={0:1}  prefix=0  res=0
x=1: prefix=1  need 1-3=-2 → count[-2]=0   res=0   deposit→ count={0:1,1:1}
x=2: prefix=3  need 3-3= 0 → count[0]=1    res=1   deposit→ count={0:1,1:1,3:1}   (subarray [1,2])
x=3: prefix=6  need 6-3= 3 → count[3]=1    res=2   deposit→ count={0:1,1:1,3:1,6:1} (subarray [3])
answer = 2
```
You never enumerated subarrays — each element asked the dict "how many of my past selves are k behind me?" and trusted the count. O(n) time, O(n) space.

## Gotchas
- **Probe order in Two Sum.** Check for the complement *before* inserting the current value, else a single element pairs with itself.
- **Seed `{0:1}` in prefix-sum-count problems.** Forgetting it drops every subarray that starts at index 0 (the prefix that equals `k` exactly).
- **Wrong canonical key.** For Group Anagrams use a *count signature* `tuple(26 counts)` (O(n)) or `sorted(s)` (O(n log n)) — but `set(s)` is wrong (`"aab"` vs `"abb"` collide). For Group Shifted Strings the key is the tuple of **adjacent diffs mod 26**, so `"abc"` and `"bcd"` match.
- **Longest Consecutive Sequence: only start counting from a left edge.** Put all nums in a set, but begin a streak walk *only* when `num-1` is absent. That guard is what keeps it O(n) instead of O(n²) — without it you re-walk the same run from every element.
- **`max get(...,0)` vs `[ ]`.** Use `.get(key, 0)` / `defaultdict` when probing keys that may not exist; bare `dict[key]` raises `KeyError`.

## Python idioms
- `collections.Counter(s)` builds a frequency map in one line; `Counter(a) == Counter(b)` is the cleanest Valid Anagram. `Counter(...).most_common(k)` gives Top-K directly.
- `collections.defaultdict(list)` for grouping — `groups[key].append(s)` with no existence check.
- Canonical keys must be **hashable**: use `tuple(...)`, not `list(...)`, as a dict key (e.g. `tuple(counts)` for anagrams).
- `heapq.nlargest(k, count, key=count.get)` or **bucket sort** by frequency solves Top-K Frequent; bucket sort is O(n) vs a heap's O(n log k).
- `set` for membership tests is O(1) average; `x in some_list` is O(n) — never scan a list inside a loop when a set will do.
- Prefix/suffix product passes (Product Except Self) avoid division and run O(n) with O(1) extra space by writing the prefix into the output then folding suffix in a second pass.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 1 | Two Sum | E | `value→index`; probe `target-x` before depositing `x` |
| 217 | Contains Duplicate | E | seen-set; `if x in seen: True` else add |
| 242 | Valid Anagram | E | frequency map; `Counter(a)==Counter(b)` (or one map, ++ then --) |
| 628 | Max Product of Three | E | no dict — sort (or track 3 max + 2 min); answer = `max(a·b·c, min1·min2·maxc)` |
| 893 | Groups of Special-Equiv Strings | E | canonical key = `(sorted even-idx chars, sorted odd-idx chars)`; count distinct keys in a set |
| 36 | Valid Sudoku | M | grid bucketing: a `set` per row, per col, per 3×3 box; reject on re-insert |
| 49 | Group Anagrams | M | key = count signature `tuple(26)` (or `sorted(s)`); `defaultdict(list)` buckets |
| 128 | Longest Consecutive Sequence | M | set of nums; start streak only when `num-1 ∉ set`; walk up counting |
| 238 | Product Except Self | M | prefix-product pass then suffix-product pass; O(n), no division |
| 249 | Group Shifted Strings | M | key = tuple of adjacent diffs `(ord-ord)%26`; `defaultdict(list)` buckets |
| 271 | Encode and Decode Strings | M | length-prefix framing `f"{len(s)}#{s}"`; decode by reading count then slicing |
| 347 | Top K Frequent Elements | M | frequency map → bucket sort by count (O(n)) or `most_common(k)` |
| 560 | Subarray Sum Equals K | M | prefix-sum→count map seeded `{0:1}`; add `count[prefix-k]` each step |
| 791 | Custom Sort String | M | freq map of `s`; emit chars in `order`'s sequence ×count, then the rest |
