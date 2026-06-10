# Greedy

## The engine in one sentence
Greedy = make the locally-best choice at each step, never look back, and bet that local optimum stacks up to global optimum — it fires when you can *prove* the greedy choice never forecloses a better future.

## The one question that unlocks it
The code is always trivial — a single scan tracking one running variable. The whole game is the proof. So ask exactly one thing:

**"Why is the greedy choice *safe* — what's the argument that taking it now can't make the final answer worse?"**

If you can't answer that in one sentence, greedy is probably wrong (use DP). Greedy fails *silently*: it returns a confident, plausible, incorrect number. The discipline is the **exchange / contradiction argument** — show that any optimal solution can be morphed into your greedy one without getting worse. If you can do that, the greedy is justified. If you're hand-waving, stop.

## The mental model
Every greedy problem is a tension between two moves:

```
   COMMIT now (greedy)                 vs    RECONSIDER later (DP/search)
 take the best-looking option,               keep all options open,
 throw the rest away forever                 pay memory/time to compare paths

 SAFE only if: committing now never
 blocks a >= future                          always safe, but slower
```

The justification almost always takes one of two shapes:

- **"Prefix can only hurt"** — a running accumulator that, once it turns against you, is worth *less than nothing*, so you reset/drop it. (Kadane, Gas Station.)
- **"Furthest is dominant"** — the choice that maximizes reach/value weakly dominates every alternative, so greedily grabbing the max can't lose. (Jump Game, Maximum Swap.)

```visual
type: before-after
title: Why reset a negative running sum
shows: that carrying a negative prefix forward strictly lowers every later subarray sum, so dropping it (reset to 0) is always safe
elements: a number line of cumulative running-sum; left segment dips below zero shaded red labeled "prefix < 0: drag"; a vertical "RESET to 0" bar; right segment climbs labeled "start fresh, never worse"; caption "any window that includes the red drag is beaten by the same window without it"
```

ASCII of the same idea (Kadane):
```
nums:   -2   1  -3   4  -1   2   1  -5   4
cur :   -2 → reset? cur<0 so drop it before next
        when cur dips below 0, it can ONLY subtract from
        whatever comes next → throw it away, restart at 0
```

## The universal template
```python
def greedy(nums):
    best = SOMETHING            # ← global answer so far (often nums[0] or 0/-inf)
    run  = INIT                 # ← the running accumulator / reach / tank
    for i, x in enumerate(nums):
        run = combine(run, x)   # ← extend the running state with x
        if run is BAD:          # ← the SAFE-to-drop condition (run can only hurt)
            run = RESET         #   reset, or move the start pointer past i
        best = better(best, run)  # ← record best seen (or just keep scanning)
    return best
```
Three decisions, all driven by the proof: **what's the running state**, **when is it safe to drop/reset it**, and **what do we record**. You should be able to say *why* the drop is safe before you write the line.

## Variants / when to use
| Sub-pattern | Running state | Greedy choice + the one-line why |
|---|---|---|
| Running-sum reset (**Kadane**) | best subarray ending here | drop prefix when `cur<0` — a negative prefix only lowers every later sum |
| Furthest-reach scan | max index reachable | extend reach to `max(reach, i+nums[i])` — a farther reach dominates any nearer one |
| Level expansion (BFS-greedy) | current jump's frontier | when you exhaust a level, take +1 jump — fewest jumps = fewest frontiers crossed |
| Feasibility + restart | running tank | if total≥0 a start exists; it's just past the lowest dip — anything before can't fuel past the dip |
| Leftmost-gain swap | best digit to the right | swap leftmost digit with the largest *later* digit — fixing a higher place value beats any lower one |

## Worked example
**LC53 Maximum Subarray (Kadane's).** Greedy choice: at each element, either extend the current run or start a new one *here* — and you start new exactly when the carried sum is negative.

**Why it's safe:** if the running sum just before index `i` is negative, any subarray that includes that prefix is strictly smaller than the same subarray without it. So a negative prefix can *only hurt* — drop it (reset to 0), losing nothing.

```python
def maxSubArray(nums):
    best = nums[0]
    cur  = 0
    for x in nums:
        if cur < 0:        # prefix can only hurt → drop it
            cur = 0
        cur += x
        best = max(best, cur)
    return best
```
`O(n)` time, `O(1)` space.

Trace on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`:
```
x     cur(before reset→add)        best
-2    cur=0→ -2                     -2
 1    cur<0→0, +1 = 1                1
-3    1 + (-3) = -2                  1
 4    cur<0→0, +4 = 4                4      ← reset paid off
-1    4 + (-1) = 3                   4
 2    3 + 2 = 5                      5
 1    5 + 1 = 6                      6      ← answer: [4,-1,2,1]
-5    6 + (-5) = 1                   6
 4    1 + 4 = 5                      6
```
Best subarray sum = **6**. Notice we never enumerated subarrays — each step just chose "extend or restart," and the restart was provably free.

```visual
type: bar-steps
title: Kadane running sum with resets
shows: cur rising and being clamped to 0 whenever it goes negative, with best tracking the running peak
elements: nine bars for [-2,1,-3,4,-1,2,1,-5,4] showing cur values [-2,1,-2,4,3,5,6,1,5]; red dashed line at 0; bars dropping below 0 marked "RESET next"; a horizontal "best" line stepping up to 6 at index 6
```

## Furthest-reach, visualized
**LC55 Jump Game** — can you reach the end? Track the furthest index reachable so far; if you ever stand at an index beyond `reach`, you're stuck.

```python
def canJump(nums):
    reach = 0
    for i, n in enumerate(nums):
        if i > reach:          # can't even get here
            return False
        reach = max(reach, i + n)
    return True
```
**Why safe:** you don't care *which* path got you here — only the maximum reach, since a farther reach makes every nearer reach redundant.

```visual
type: pointer-walk
title: Furthest-reach scan (Jump Game)
shows: reach expanding to the max of (current reach, i+nums[i]) as i walks left to right, and failure when i overtakes reach
elements: array indices 0..n-1 as cells with nums values; a moving "i" caret; a horizontal "reach" bracket that only grows; highlight the step where reach jumps; an X if i passes the bracket's right edge
```

**LC45 Jump Game II** — *fewest* jumps. Same reach idea, but expand in BFS-like levels: a jump count increments only when you've consumed the current reachable window.
```python
def jump(nums):
    jumps = end = farthest = 0
    for i in range(len(nums) - 1):     # no jump needed at last index
        farthest = max(farthest, i + nums[i])
        if i == end:                   # exhausted current level → must jump
            jumps += 1
            end = farthest
    return jumps
```
**Why safe:** within one jump's window every index is equally "1 jump away"; you only pay another jump when forced, and you always extend to the farthest the window allows — fewest windows crossed = fewest jumps.

## Gotchas
- **Kadane init:** start `best = nums[0]`, not `0`. An all-negative array like `[-3,-1,-2]` must return `-1`, not `0`. Initializing `best=0` silently returns the empty-subarray answer.
- **Gas Station (LC134) — two checks, don't conflate them.** Feasibility is global: if `sum(gas) < sum(cost)`, return `-1`. The *start* is local: scan once tracking `tank`; whenever `tank` dips below 0, no station up to here can be the start, so set `start = i+1` and reset `tank = 0`. Why safe: if you ran dry reaching `i`, every earlier start also runs dry by `i` (it had even less fuel arriving), so skip them all. With total gas ≥ total cost, the single surviving start is guaranteed valid.
  ```python
  def canCompleteCircuit(gas, cost):
      if sum(gas) < sum(cost): return -1
      start = tank = 0
      for i in range(len(gas)):
          tank += gas[i] - cost[i]
          if tank < 0:           # can't reach i+1 from current start
              start, tank = i + 1, 0
      return start
  ```
- **Maximum Swap (LC670) — swap with the *last* occurrence of the largest later digit.** Greedily, scan from the leftmost digit; find the largest digit to its right, and if it beats the current digit, swap. Use the *rightmost* copy of that max digit so the big digit lands as far left as possible. Why safe: improving a higher place value dominates any improvement at a lower place — and one swap is all you get.
  ```python
  def maximumSwap(num):
      d = list(str(num))
      last = {int(c): i for i, c in enumerate(d)}   # rightmost index of each digit
      for i, c in enumerate(d):
          for big in range(9, int(c), -1):          # want a bigger digit later
              if last.get(big, -1) > i:
                  d[i], d[last[big]] = d[last[big]], d[i]
                  return int("".join(d))
      return num
  ```
- **Greedy ≠ always right.** If you can't state the exchange argument, you're guessing. Many "looks greedy" problems (coin change with arbitrary denominations, knapsack) need DP. The proof is the gate.

## Python idioms
- `cur = max(cur, 0)` or an explicit `if cur < 0: cur = 0` to clamp a running accumulator — the heart of reset-style greedy.
- `farthest = max(farthest, i + nums[i])` — the furthest-reach one-liner; reuse it for both Jump Game variants.
- Build a "last index of each value" dict in one pass: `{v: i for i, v in enumerate(xs)}` (later writes win → rightmost). Perfect for Maximum Swap.
- Digit problems: `list(str(num))` to mutate in place, `int("".join(d))` to rebuild — avoids fragile `//`/`%` arithmetic.
- `range(len(nums) - 1)` when the last element needs no processing (Jump Game II) — a classic off-by-one guard.
- Greedy is almost always `O(n)` time, `O(1)` extra space (Maximum Swap's dict is `O(1)` — at most 10 keys). If you reach for a heap or DP table, double-check greedy actually applies.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 53 | Maximum Subarray | M | Kadane; running state = best sum ending here; drop prefix when `cur<0` (negative prefix only hurts); record `max` |
| 55 | Jump Game | M | furthest-reach scan; state = max reachable index; fail if `i>reach`; farther reach dominates |
| 45 | Jump Game II | M | reach + BFS levels; bump `jumps` only when `i==end`; extend `end=farthest`; fewest windows = fewest jumps |
| 134 | Gas Station | M | feasibility (`sum(gas)≥sum(cost)`) + restart `start=i+1` whenever running tank `<0`; pre-dip starts all fail |
| 670 | Maximum Swap | M | leftmost-gain swap; swap left digit with rightmost copy of largest later digit; higher place value dominates |
