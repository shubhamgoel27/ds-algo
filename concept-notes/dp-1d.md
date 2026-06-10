# Dynamic Programming — 1D

## The engine in one sentence
1D DP = "define one number `dp[i]` that fully answers the subproblem ending at index `i`, then express it using only *earlier* `dp` values" — so the whole array fills in one pass instead of an exponential recursion tree re-solving the same prefixes.

## The one question that unlocks it
Stop trying to compute the final answer directly. Ask the one question that turns any DP into a fill-in-the-blank:
**"If I already knew the answer for every smaller subproblem, how would I build the answer for `i`?"**
That single sentence is the *recurrence*. Once you can write `dp[i] = f(dp[i-1], dp[i-2], ...)`, you're done thinking — the rest is bookkeeping (base cases + loop order). The recursion and the table are the *same equation*; one fills it lazily top-down, the other eagerly bottom-up.

## The mental model
Every 1D DP is four decisions. Burn this checklist into memory — it's the whole pattern:
```
1. STATE      dp[i] = "<answer for the subproblem ending at / using up to i>"   ← one English sentence
2. RECURRENCE dp[i] = f( dp[i-1], dp[i-2], ... )                                ← how i leans on the past
3. BASE       dp[0] (and maybe dp[1]) = known seed values                       ← the smallest subproblems
4. ORDER      iterate i so every dependency is computed before you need it      ← usually left → right
```
The dichotomy that confuses people: **top-down memo vs bottom-up table are NOT two algorithms.** Same recurrence, opposite fill direction:
```
   TOP-DOWN (memo)                      BOTTOM-UP (table)
 recurse from the answer DOWN         start at the base, build UP
 dp[i] computed lazily, on demand     dp[i] computed eagerly, in order
 cache dict / @lru_cache              explicit array, for-loop
 recursion stack = O(n) space         can often shrink to O(1) rolling vars
```

```visual
type: grid-animation
title: House Robber dp array filling left-to-right
shows: how each dp[i] is computed from dp[i-1] and dp[i-2] in one pass, choosing skip-vs-rob
shows the recurrence dp[i]=max(dp[i-1], dp[i-2]+nums[i]) lighting up two prior cells to set the current cell
elements: nums row [2,7,9,3,1]; dp row below filling cell by cell to [2,7,11,11,12]; for cell dp[2]=11 highlight dp[1]=7 (skip arrow) and dp[0]+nums[2]=2+9=11 (rob arrow), max picks 11; a running "best so far" pointer landing on dp[4]=12
```

## The universal template
```python
def solve(nums):
    n = len(nums)
    dp = [0] * n                      # ← STATE: dp[i] = answer for subproblem ending at i
    dp[0] = base_value(nums[0])       # ← BASE: smallest subproblem(s), set directly
    for i in range(1, n):             # ← ORDER: left→right so dp[i-1], dp[i-2] already exist
        dp[i] = combine(dp[i-1],      # ← RECURRENCE: build dp[i] from earlier states only
                        dp[i-2],
                        nums[i])
    return dp[-1]                     # ← or max(dp), or dp computed at the target index
```
The exact same equation, written top-down:
```python
from functools import lru_cache
def solve(nums):
    @lru_cache(None)
    def dp(i):                        # ← STATE: answer for subproblem ending at i
        if i < 0: return 0            # ← BASE expressed as a recursion floor
        return combine(dp(i-1), dp(i-2), nums[i])   # ← SAME RECURRENCE
    return dp(len(nums) - 1)
```
Four blanks, every time: **state**, **recurrence**, **base**, **order**. Fill them and the code writes itself.

## Variants / when to use
| Shape | dp[i] means | Recurrence flavor | Catalog problem |
|---|---|---|---|
| Linear pick/skip | best using items 0..i | `max(dp[i-1], dp[i-2]+v)` | LC198 House Robber |
| Circular pick/skip | same, but ends wrap | run linear twice, drop first or last | LC213 House Robber II |
| Count ways | # ways to reach i | `dp[i] = dp[i-1] + dp[i-2]` (sum, not max) | LC70 Climbing Stairs, LC91 Decode Ways |
| Track two extremes | best+worst ending at i | keep `maxp` AND `minp` (sign flips) | LC152 Max Product Subarray |
| Best-over-all-j (O(n²)) | best ending at i | `1 + max(dp[j])` over valid `j<i` | LC300 LIS (n²) / Word Break |
| Unbounded knapsack | min coins / reachability for amount t | `min(dp[t-c]+1)` over coins `c` | LC322 Coin Change |
| Subset-sum / 0-1 | can we hit target sum? | `dp[t] |= dp[t-num]`, iterate t **downward** | LC416 Partition Equal Subset |
| Interval / 2D-on-1D-axis | palindrome over (i,j) | expand-around-center or `dp[i][j]` | LC5 Longest Palindromic Substring |

## Worked example
**LC322 Coin Change** — `coins=[1,2,5]`, `amount=11`. Classic unbounded knapsack.

- **State:** `dp[t]` = fewest coins to make amount `t`.
- **Recurrence:** `dp[t] = 1 + min(dp[t-c])` over every coin `c ≤ t`.
- **Base:** `dp[0] = 0` (zero coins make amount 0). Everything else starts at `∞` (unreachable).
- **Order:** `t` from `1 → amount`, so every `dp[t-c]` is already final.

```python
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for t in range(1, amount + 1):
        for c in coins:
            if c <= t:
                dp[t] = min(dp[t], dp[t - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```
Trace filling `dp[0..11]` with `coins=[1,2,5]` (each cell = min coins; `∞` means unreachable yet):
```
t      :  0   1   2   3   4   5   6   7   8   9  10  11
dp[t]  :  0   1   1   2   2   1   2   2   3   3   2   3
                                  ↑                   ↑
   dp[5]=1: best of dp[4]+1=3, dp[3]+1=3, dp[0]+1=1 → use the 5-coin
   dp[11]=3: best of dp[10]+1=3, dp[9]+1=4, dp[6]+1=3 → 5+5+1
```
Each `dp[t]` looked back exactly `len(coins)` cells and took the cheapest predecessor. Answer = `dp[11] = 3` (5+5+1).

```visual
type: bar-steps
title: Coin Change dp table built amount 0 → 11
shows: each amount t pulling from dp[t-1], dp[t-2], dp[t-5] and taking the minimum predecessor + 1
elements: an array of 12 bars indexed 0..11 with heights [0,1,1,2,2,1,2,2,3,3,2,3]; when filling t=5 draw three back-arrows to t=4,t=3,t=0 and highlight the t=0 path (+1 coin) as the winner; mark dp[0]=0 as the base seed in a distinct color
```

## Gotchas
- **Max Product Subarray needs TWO running values.** A negative flips sign, so today's *minimum* can become tomorrow's *maximum*. Track both `cur_max` and `cur_min`, and **swap them when `nums[i] < 0`** (or recompute both as max/min of `{n, n*cur_max, n*cur_min}`). One running max alone is the #1 wrong answer here.
- **House Robber II = run the linear DP twice.** The houses form a circle, so house `0` and house `n-1` are adjacent. You can't rob both → answer is `max(rob(nums[0:-1]), rob(nums[1:]))`. Edge case: a single house, return `nums[0]` directly (both slices would be empty).
- **0-1 vs unbounded loop direction (LC416 vs LC322).** Coin Change reuses each coin unlimited times → iterate amount **forward** (`dp[t-c]` may already include `c`). Partition Equal Subset Sum uses each number **once** → iterate the target sum **downward** so a number isn't counted twice. Flip the loop and you silently solve the wrong problem.
- **Count vs optimize.** Climbing Stairs / Decode Ways *sum* predecessors (`dp[i]=dp[i-1]+dp[i-2]`); Robber/Coin Change take a *max/min*. Using `max` where you need a count (or vice-versa) is a classic mis-frame.
- **Decode Ways zeros.** A leading `'0'` is invalid; `"06"` is NOT a valid two-digit decode. Only add the one-digit path when `s[i] != '0'`, and the two-digit path when `10 ≤ int(s[i-1:i+1]) ≤ 26`.
- **`float('inf')` overflow in min-recurrences.** Doing `dp[t-c] + 1` on an `inf` cell stays `inf` in Python (safe), but guard the final read: return `-1` if the target is still `inf`.

## Python idioms
- `@lru_cache(None)` (or `functools.cache`) turns any recursion into top-down DP for free — just make args hashable. Watch Python's ~1000-deep recursion limit on long inputs (Word Break, LIS).
- **Rolling variables** collapse O(n) space to O(1) when `dp[i]` only needs the last one or two cells: `prev2, prev1 = prev1, max(prev1, prev2 + x)` (House Robber, Climbing Stairs).
- `bisect.bisect_left` powers the **O(n log n) LIS**: maintain a `tails` array of smallest tail per length; for each `x`, replace the first tail `≥ x` (patience sorting). `len(tails)` is the LIS length. The plain O(n²) DP (`dp[i]=1+max(dp[j] for j<i if nums[j]<nums[i])`) is fine for small `n`.
- Boolean DP as a set or bitmask: Partition Equal Subset can be a `set` of reachable sums, or a Python int used as a bitset (`bits |= bits << num`), exploiting big-int shifts.
- `dp = [0]*(n)` for counts/sums, `[float('inf')]*(n)` for minimization, `[False]*(n)` for reachability — pick the identity that the recurrence's combine operator leaves unchanged.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 70 | Climbing Stairs | E | `dp[i]=dp[i-1]+dp[i-2]`; base `dp[0]=dp[1]=1`; it's Fibonacci, O(1) rolling vars |
| 198 | House Robber | M | `dp[i]=max(dp[i-1], dp[i-2]+nums[i])`; base `dp[0]=nums[0]`; pick-vs-skip |
| 213 | House Robber II | M | run LC198 twice on `nums[:-1]` and `nums[1:]`, take max; circle breaks adjacency |
| 91 | Decode Ways | M | `dp[i]=` (one-digit ok ? `dp[i-1]` : 0) `+` (two-digit 10..26 ? `dp[i-2]` : 0); count, not max |
| 139 | Word Break | M | `dp[i]=any(dp[j] and s[j:i] in words)` over `j<i`; boolean, O(n²) |
| 152 | Max Product Subarray | M | track `cur_max` AND `cur_min` ending at i; swap on negatives; answer = global max |
| 300 | Longest Increasing Subsequence | M | O(n²): `dp[i]=1+max(dp[j] for j<i if nums[j]<nums[i])`; O(n log n): `bisect` on tails |
| 322 | Coin Change | M | unbounded knapsack: `dp[t]=1+min(dp[t-c])`; base `dp[0]=0`; iterate amount forward |
| 416 | Partition Equal Subset Sum | M | subset-sum to `total/2`: `dp[t]|=dp[t-num]`; iterate t **downward** (0-1, each num once) |
| 5 | Longest Palindromic Substring | M | expand-around-center (O(n²) time, O(1) space) or `dp[i][j]=s[i]==s[j] and dp[i+1][j-1]` |
