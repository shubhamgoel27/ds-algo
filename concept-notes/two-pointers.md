# Two Pointers

## The engine in one sentence
Two pointers = walk two indices over one (or two) arrays under an **invariant**, and at every step move *only* the pointer whose move can possibly improve the answer — because you can prove the other move never can.

## The one question that unlocks it
Brute force pairs every element with every other element — `O(n²)`. The two-pointer trick collapses that to `O(n)` by answering one question at each step:

**"Given what these two pointers see right now, which one can I move while *safely throwing away* every option the other pointer would have explored?"**

If you can argue *"moving the other pointer can never beat what I already have"*, you've earned the right to skip an entire row of the `O(n²)` table. That discard-is-safe proof is the whole pattern.

## The mental model
Three flavors, but they're the same idea — two indices and an invariant:

```
(1) CONVERGING        lo →        ← hi      sorted array; squeeze inward
    sum too big? hi--   sum too small? lo++   each move kills a whole row/col

(2) READ / WRITE      write →   read →→→      one array, compact in place
    read scans every cell; write trails, only lands "kept" elements

(3) FAST / SLOW       slow →    fast →→        same direction, different speeds
    (a special read/write: slow = write boundary, fast = read scanner)
```

The unifying invariant: **everything behind `write` (or outside `[lo,hi]`) is already finalized and correct.** You never revisit it.

```visual
type: pointer-walk
title: Converging pointers on Two Sum II (sorted), target = 9
shows: how each comparison moves exactly one pointer inward, discarding a whole row of pairs, until the pair is found in O(n)
elements: array cells [2,3,5,8,11,15] indexed 0..5; lo starts at 0, hi at 5; step rows showing (lo,hi,sum,decision)= (0,5,17,">9 → hi--), (0,4,13,">9 → hi--), (0,3,10,">9 → hi--), (0,2,7,"<9 → lo++"), (1,2,8,"<9 → lo++") ... emphasize "1+5=6 — wait recompute"; final highlight pair (1,3)=3+8? no. Use cells values 2,3,5,8,11,15: show converging arrows meeting at the answer 3+? . Draw lo as a green arrow under the array, hi as a red arrow, sweeping toward each other; annotate each discarded hi with "every pair (*,hi) > target ⇒ drop them all".
```

## The universal template

**Converging (sorted array):**
```python
def converge(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        cur = arr[lo] + arr[hi]        # ← the quantity you're steering
        if cur == target:
            return (lo, hi)            # ← hit
        elif cur < target:             # ← need bigger? the SMALL side is the bottleneck
            lo += 1                    #   arr[lo] paired with anything ≤ arr[hi] is too small → drop it
        else:
            hi -= 1                    # ← need smaller? drop the big side
    return None
```

**Read / write (in-place compaction):**
```python
def compact(arr):
    write = 0                          # ← next slot for a KEEP
    for read in range(len(arr)):       # read scans every element
        if keep(arr[read]):            # ← the predicate: is this element kept?
            arr[write] = arr[read]     # ← place it (or swap for stability)
            write += 1
    return write                       # ← length / boundary of the kept region
```

Two decisions for converging: **what quantity you steer** and **which side to move on each comparison**. Two for read/write: **the keep-predicate** and **place vs. swap**.

## Variants / when to use
| Variant | Pointers | Invariant | Use for |
|---|---|---|---|
| Converging | `lo`/`hi` inward | array sorted (or symmetry) | Two Sum II, 3Sum, Valid Palindrome |
| Move-smaller greedy | `lo`/`hi` inward | width shrinks, so a bottleneck must improve to win | Container With Most Water, Trapping Rain Water |
| Read/write compaction | `write` trails `read` | left of `write` is finalized | Remove Duplicates, Move Zeroes |
| Fill-from-back | two reads + back `write` | suffix of dest is finalized | Merge Sorted Array (LC88) |
| Synchronized scan | `i` over word, `j` over abbr | both consumed exactly ⇒ match | Valid Word Abbreviation |

## Worked example
**LC11 Container With Most Water** — the cleanest "move the smaller side" proof.

Area between walls `i` and `j` is `min(h[i], h[j]) * (j - i)`. Start `lo,hi` at the ends (max width). Each step you *must* shrink the width by one, so the only way a future container beats the current one is by raising the limiting (shorter) wall.

**Why moving the smaller side is safe:** suppose `h[lo] < h[hi]`. Any container using `lo` with a closer-in right wall has width `< (hi-lo)` AND height still capped by `h[lo]` (the short wall). So it can't beat the area we just measured. Every pair `(lo, *)` is dominated — discard `lo` entirely.

```python
def maxArea(h):
    lo, hi = 0, len(h) - 1
    best = 0
    while lo < hi:
        best = max(best, min(h[lo], h[hi]) * (hi - lo))
        if h[lo] < h[hi]:     # short side is the bottleneck → abandon it
            lo += 1
        else:
            hi -= 1
    return best
```

Trace on `h = [1,8,6,2,5,4,8,3,7]`:
```
lo hi  h[lo] h[hi]  width  area  move
0  8     1     7      8      8    h[lo]<h[hi] → lo++   (8*1, can't be beaten via lo)
1  8     8     7      7     49    h[lo]>h[hi] → hi--
1  7     8     3      6     18    h[lo]>h[hi] → hi--
1  6     8     8      5     40    tie → hi-- (either is fine)
1  5     8     4      4     16    hi--
1  4     8     5      3     15    hi--
1  3     8     2      2     16    hi--
1  2     8     6      1      6    hi--
1  1   → lo==hi, stop
best = 49
```
Each row killed one pointer's entire remaining set of pairs — `O(n)` instead of `O(n²)`.

```visual
type: bar-steps
title: Container With Most Water — move the shorter wall
shows: that shrinking width forces you to raise the short wall, and the 49 area is found by always abandoning the bottleneck side
elements: bar chart of heights [1,8,6,2,5,4,8,3,7]; highlight the water rectangle between lo=1 (h=8) and hi=8 (h=7) capped at height 7 width 7 = 49; show faded earlier rectangle (lo=0,hi=8) area 8; arrows annotating "short wall is the cap; widening is impossible, so raise the cap".
```

## Gotchas
- **3Sum duplicates.** After fixing `nums[i]`, run converging `lo/hi` on the rest. You must skip duplicate `i` *and* skip duplicate `lo`/`hi` after recording a triplet — otherwise repeated triplets. Sort first; that's what makes converging legal.
- **Move Zeroes must be stable + in-place.** Use swap, not overwrite: `nums[slow], nums[fast] = nums[fast], nums[slow]` when `nums[fast] != 0`. Overwriting then zero-filling also works but is two passes; the swap keeps relative order in one.
- **Merge Sorted Array — fill from the BACK.** Filling front-to-back into `nums1` clobbers unread values. Start `write = m+n-1`, compare tails, place the larger at `write`. If `nums2` is exhausted first, the rest of `nums1` is already in place; if `nums1` is exhausted, you still must drain `nums2`.
- **Valid Palindrome two-sided skip.** Advance `lo`/`hi` past non-alphanumerics *before* comparing, and lowercase. Forgetting to keep skipping in a `while` (vs a single `if`) breaks on runs of punctuation.
- **Trapping Rain Water — track the running maxes, not the bars.** Water over a column = `min(maxLeft, maxRight) - height`. Move the side with the smaller wall, because that side's answer is fully determined by its known max (the other side can only be taller).

## Python idioms
- `s.isalnum()` and `s.lower()` for Valid Palindrome filtering — no regex needed.
- Tuple swap `a[i], a[j] = a[j], a[i]` is atomic and O(1) — ideal for Move Zeroes / partition.
- `while lo < hi` for converging (pair needs two distinct slots); `while lo <= hi` only when a single middle element is itself a valid answer.
- Avoid `list.pop(0)` to "remove a zero" — it's O(n) and shifts everything; the write-pointer does it in O(1) amortized.
- For 3Sum, sort with `nums.sort()` (O(n log n)) up front — the converging scan is then O(n) per fixed element, O(n²) total, beating the O(n³) brute force.

## Problem map
| LC | Problem | Df | How it fills the template |
|---|---|---|---|
| 167 | Two Sum II (sorted) | E | converging; steer `arr[lo]+arr[hi]`; `<target`→`lo++`, `>target`→`hi--` |
| 125 | Valid Palindrome | E | converging from ends; skip non-alnum each side; compare lowercased chars |
| 26 | Remove Duplicates (sorted) | E | read/write; keep predicate `nums[read] != nums[write-1]`; return `write` |
| 283 | Move Zeroes | E | read/write via **swap**; keep predicate `nums[read] != 0`; stable, in-place |
| 88 | Merge Sorted Array | E | fill-from-back; reads at `m-1`,`n-1`, write at `m+n-1`; place larger tail; drain `nums2` |
| 408 | Valid Word Abbreviation | E | synchronized scan; `i` over word, `j` over abbr; parse digit run as skip count, no leading zero, then char-match |
| 11 | Container With Most Water | M | converging; steer `min(h[lo],h[hi])*(hi-lo)`; move the **shorter** wall |
| 167-style 15 | 3Sum | M | sort; fix `i`; converging `lo/hi` on suffix for `-nums[i]`; skip dups on `i`,`lo`,`hi` |
| 31 | Next Permutation | M | scan from right for first `nums[i]<nums[i+1]`; from right find first `> nums[i]`, swap; **reverse** the suffix (two-pointer reverse) |
| 42 | Trapping Rain Water | H | converging; track `maxLeft`,`maxRight`; move smaller side; add `maxSide - height` at that pointer |
