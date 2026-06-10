# Backtracking

## The engine in one sentence
Backtracking is DFS over a tree of decisions: at each node you **make a choice, recurse, then undo it** — exploring every path but only carrying one partial solution at a time. It fires whenever the answer is "all/any ways to build something from a sequence of choices" — subsets, permutations, combinations, partitions, grid paths.

## The one question that unlocks it
Don't think about the final answer. Think about **one decision**: "Standing here with a half-built `path`, what are my choices for the *next* slot, and after I try one, how do I rewind to try the others?"

Every backtracking problem is the same loop — `for choice in choices: choose → recurse → un-choose`. The ONLY thing that changes between problems is the answer to a single question:

**What limits the choices at each level?**

Get that one decision right and the template writes itself.

## The mental model
A backtracking search IS a tree. The root is the empty solution; each edge is "I picked this choice"; each leaf (or qualifying node) is a recorded answer. DFS walks it. The `path` is your current root-to-here trail; `choose`/`un-choose` keep `path` in sync as you descend and climb.
```
                       path=[]                    ← root: nothing chosen
            choose 1 /    | choose 2  \ choose 3
              [1]        [2]           [3]
          /2  |3         |3                        ← choices SHRINK as you go down
        [1,2] [1,3]    [2,3]
         |3
       [1,2,3]                                     ← leaf: a complete solution
```
The whole trick is the symmetry: **whatever you do on the way DOWN (append, mark used, flip a cell), you must reverse on the way UP**, so each sibling branch starts from a clean slate.

```visual
type: tree
title: Backtracking = DFS over a decision tree (Subsets of [1,2,3])
shows: how each node is a partial solution, each downward edge a choice, and every node is recorded as a subset; emphasize that path is appended on descent and popped on ascent
elements: root node "[]"; three children via edges labeled "+1","+2","+3" → "[1]","[2]","[3]"; "[1]" has children "[1,2]","[1,3]"; "[1,2]" has child "[1,2,3]"; "[2]" has child "[2,3]"; annotate one path with green "append" arrows going down and red "pop" arrows going up; caption "start index keeps choices to the RIGHT only — no reuse, no reorder"
```

## The universal template
Burn this into memory. Every problem below is a fill-in of these four blanks.
```python
def solve(nums):
    res = []
    def backtrack(start, path):          # ← state: what's chosen + what limits next choices
        if is_complete(path):            # ← BLANK 1: when is `path` a finished answer?
            res.append(path[:])          #   record a COPY (path keeps mutating)
            return
        for i in range(start, len(nums)):  # ← BLANK 2: which choices are legal here?
            path.append(nums[i])         #   CHOOSE
            backtrack(i + 1, path)       # ← BLANK 3: how do choices shrink for the child?
            path.pop()                   #   UN-CHOOSE (mirror the choose, exactly)
    backtrack(0, [])
    return res
```
Four decisions only:
1. **When is `path` complete** → record (sometimes *every* node counts, e.g. Subsets).
2. **What are the legal choices** at this level (the `for` range / candidate set).
3. **How choices shrink** for the recursive call — this is the heart, see below.
4. **Choose / un-choose** must be exact mirrors.

**The one decision that distinguishes the problems — what limits the choices:**

| Limiter | Pass to child | Why | Problems |
|---|---|---|---|
| `start` index | `backtrack(i + 1, ...)` | combinations: never reuse or reorder | Subsets 78, Comb. Sum 39 |
| `start` index, **reusable** | `backtrack(i, ...)` (note: `i`, not `i+1`) | may pick same element again | Combination Sum 39 |
| `used[]` boolean array | mark `used[i]=True` / unmark | permutations: order matters, each element once, all positions open | Permutations 46 |
| grid neighbors + visited | mark cell, recurse 4 dirs, unmark | path through a 2-D grid | Word Search 79 |
| valid split points | for each `end`, recurse on suffix if prefix qualifies | partition a string | Palindrome Partitioning 131 |

## Variants / when to use
| Sub-pattern | Choices limited by | Child call | Record when |
|---|---|---|---|
| **Subsets** (78) | `start` (no reuse, no reorder) | `backtrack(i+1)` | at *every* node |
| **Combinations / Comb. Sum** (39) | `start`, but **`i`** to allow reuse | `backtrack(i)` | when `remaining == 0` |
| **Permutations** (46) | `used[]` — all unused indices | mark/unmark `used[i]` | when `len(path)==n` |
| **Fixed-set choices** (17) | digit → its letters, advance index | `backtrack(idx+1)` | when `idx == len(digits)` |
| **String partition** (131) | every prefix that is valid | recurse on `s[end:]` | when suffix empty |
| **Grid DFS** (79) | 4 neighbors, in-bounds, unvisited | recurse, mark/unmark cell | when whole word matched |

## Worked example
**LC78 Subsets** — the cleanest backtracking skeleton. Every node *is* an answer, so record at the top of every call. Choices are limited by a `start` index so we only ever look rightward — that's what prevents `[1,2]` and `[2,1]` from both appearing.
```python
def subsets(nums):
    res = []
    def backtrack(start, path):
        res.append(path[:])              # every partial path is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])         # CHOOSE nums[i]
            backtrack(i + 1, path)       # only choices to the RIGHT of i
            path.pop()                   # UN-CHOOSE
    backtrack(0, [])
    return res
```
Trace on `nums = [1,2,3]` (record on *entry*, indent = depth):
```
backtrack(0, [])           record []
 ├ i=0 +1 → backtrack(1,[1])      record [1]
 │   ├ i=1 +2 → backtrack(2,[1,2])    record [1,2]
 │   │   └ i=2 +3 → backtrack(3,[1,2,3]) record [1,2,3]   pop 3
 │   │   pop 2
 │   └ i=2 +3 → backtrack(3,[1,3])    record [1,3]    pop 3
 │   pop 1
 ├ i=1 +2 → backtrack(2,[2])      record [2]
 │   └ i=2 +3 → backtrack(3,[2,3])    record [2,3]    pop 3
 │   pop 2
 └ i=2 +3 → backtrack(3,[3])      record [3]      pop 3
```
Result: `[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]` — all 2³ = 8 subsets. Notice each `pop` exactly mirrors its `append`, and `start=i+1` guarantees we never revisit a number or produce a reordering.

## Gotchas
- **Recording a reference, not a copy.** `res.append(path)` appends the *same list object*; later `pop`s mutate it and every entry becomes garbage. Always `path[:]` (or `list(path)`).
- **Choose/un-choose not mirrored.** If you `path.append(x)` you must `path.pop()`; if you set `used[i]=True` you must reset it to `False`; if you flip a grid cell you must flip it back. Forget the undo and sibling branches inherit polluted state.
- **`i` vs `i+1`.** Combination Sum (39) reuses elements → recurse with `backtrack(i, ...)`. Subsets/standard combinations → `backtrack(i+1, ...)`. One character, totally different problem.
- **Word Search: restore the cell on *every* exit path.** Mark the cell before recursing the 4 neighbors, and unmark it before returning — including the failing return — or other start-cells will see it as permanently blocked.
- **Pruning placement.** In Combination Sum, check `remaining < 0` and bail (or break, if candidates are sorted) instead of recursing into hopeless branches. The search is exponential by nature — pruning is what keeps it tractable, not optional polish.

## Python idioms
- **`path[:]` / `list(path)`** to snapshot the current path when recording — the #1 backtracking bug is appending the live list.
- **`path.append` / `path.pop()`** (a stack) is the idiomatic choose/un-choose. O(1) both ways; avoid `path.pop(0)` (O(n)).
- **`used = [False] * n`** for permutations — a boolean array is faster than a `set` and trivially undoable.
- **Sort candidates first** (e.g. Combination Sum) so a single `if remaining - nums[i] < 0: break` prunes all larger candidates at once.
- **Mark-in-place for grids**: temporarily set `board[r][c] = '#'` (a sentinel) instead of a separate `visited` set — fewer allocations, and restore it on the way out.
- **Complexity is exponential and that's expected.** Subsets/Comb.Sum explore O(2ⁿ) nodes; Permutations O(n·n!); these are output-bound — you literally must emit that many answers. Don't try to "fix" it; just prune dead branches.

## Problem map
| LC | Problem | Df | How it fills the template |
|---|---|---|---|
| 17 | Letter Combinations of a Phone Number | M | choices = letters of digit `digits[idx]`; child = `backtrack(idx+1)`; complete when `idx==len(digits)`; record the joined string |
| 39 | Combination Sum | M | choices = candidates from `start`; **reuse allowed → recurse `backtrack(i)`** not `i+1`; prune when `remaining-cand<0` (break if sorted); record when `remaining==0` |
| 46 | Permutations | M | no `start`; choices = all `i` with `used[i]==False`; mark `used[i]=True`/append, then unmark/pop; complete when `len(path)==n` |
| 78 | Subsets | M | choices from `start`; child = `backtrack(i+1)`; **record at every node** (no completion test) |
| 79 | Word Search | M | choices = 4 grid neighbors in-bounds, unvisited, matching `word[k]`; mark cell `'#'` / recurse / restore; complete when `k==len(word)`; try every start cell |
| 131 | Palindrome Partitioning | M | choices = each split `end` where prefix `s[start:end]` is a palindrome; child = `backtrack(end)`; complete when `start==len(s)`; record the list of cuts |
