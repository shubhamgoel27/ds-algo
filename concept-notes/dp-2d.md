# Dynamic Programming — 2D

## The engine in one sentence
2D DP = "the answer for two prefixes `A[:i]` and `B[:j]` is built from the answers for *slightly shorter* prefixes" — you fill a grid where each cell looks at its **up, left, and diagonal** neighbors and the corner cell is your answer.

## The one question that unlocks it
Don't try to solve the whole thing. Stand on cell `dp[i][j]` and ask exactly one thing:
**"Looking only at the last character of each prefix — `A[i-1]` and `B[j-1]` — what's the one decision I make here, and which already-solved smaller cells does it reduce to?"**

The whole pattern is: *do they match?* If yes, you usually inherit the **diagonal** `dp[i-1][j-1]` (you've "consumed" one char from each). If no, you combine the **neighbors** — up (`dp[i-1][j]` = drop a char from A) and left (`dp[i][j-1]` = drop a char from B). You never re-derive a subproblem; you trust the cells already filled.

## The mental model
Every two-sequence DP is a grid. Row `i` = "I've considered the first `i` chars of A", column `j` = "first `j` chars of B". The three sources of truth for any cell:

```
            B[j-1]
              |
   dp[i-1][j-1]   dp[i-1][j]
        (diag)   (up: skip A[i-1])
              \    |
A[i-1] ——      \   |
   dp[i][j-1] —— dp[i][j]
   (left: skip B[j-1])

 match A[i-1]==B[j-1]  → use DIAGONAL (+0/+1)
 mismatch              → combine UP / LEFT  (min for cost, max for length)
```

The empty-prefix **row 0 and column 0 are your base cases** — "A vs empty string" and "empty vs B". Fill them first, then sweep row by row, left to right, so every neighbor a cell needs is already done. Answer sits in the bottom-right corner `dp[m][n]`.

```visual
type: grid-animation
title: LCS grid filling with up/left/diagonal dependency
shows: that each cell dp[i][j] is computed from its diagonal (on match, +1) or the max of up/left (on mismatch), filling row by row to the bottom-right corner
elements: a 5x4 grid for A="ABCBDAB", B="BDCAB" (or smaller); row 0 and col 0 shaded as base case zeros; for one highlighted cell draw three arrows — a green diagonal arrow labeled "+1 if match", a blue up arrow and a blue left arrow labeled "max() if mismatch"; mark the bottom-right cell as "answer"
```

## The universal template
```python
def two_seq_dp(A, B):
    m, n = len(A), len(B)
    # dp[i][j] = answer for A[:i] vs B[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # ← BASE CASES: fill row 0 and col 0 (empty-prefix answers).
    #    LCS: zeros. Edit Distance: dp[i][0]=i, dp[0][j]=j (i deletes / j inserts).
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:        # ← MATCH rule: usually the diagonal
                dp[i][j] = dp[i - 1][j - 1] + match_bonus   # +1 (LCS) or +0 (edit, free copy)
            else:                            # ← MISMATCH rule: combine neighbors
                dp[i][j] = combine(           # max(...) to optimize length,
                    dp[i - 1][j],            #   up   = drop/delete A[i-1]
                    dp[i][j - 1],            #   left = drop/insert B[j-1]
                    dp[i - 1][j - 1],        #   diag = replace (edit distance only)
                )                            # min(...)+cost for edit distance
    return dp[m][n]                          # ← answer in the corner
```
Three decisions: the **base row/col**, the **match rule** (diagonal), and the **mismatch combine** (max vs min, which neighbors).

## Variants / when to use
| Sub-pattern | Grid axes | Match rule | Mismatch / combine | Example |
|---|---|---|---|---|
| **Two-sequence (length)** | `A[:i]` × `B[:j]` | diag + 1 | `max(up, left)` | LCS (1143) |
| **Two-sequence (cost)** | `A[:i]` × `B[:j]` | diag + 0 | `1 + min(up, left, diag)` | Edit Distance (72) |
| **Pattern matching** | text × pattern | diag if char/`.` matches | `*` lets you drop pair or repeat | Regex (10) |
| **Counting knapsack** | items × amount | n/a (count, don't optimize) | `dp[a] += dp[a-coin]`, **coin loop outer** | Coin Change II (518) |
| **State-machine DP** | day × {hold, sold, rest} | n/a | transitions between fixed states | Stock w/ Cooldown (309) |

## Worked example
**LC1143 Longest Common Subsequence.** `dp[i][j]` = length of the LCS of `A[:i]` and `B[:j]`. Empty prefix ⇒ LCS 0, so the whole base row/col is zeros. On a match, the two matching chars extend the best LCS of the shorter prefixes → `dp[i-1][j-1] + 1`. On a mismatch, the last char of A or B can't both be in the LCS, so take the better of dropping one → `max(dp[i-1][j], dp[i][j-1])`.

```python
def longestCommonSubsequence(A: str, B: str) -> int:
    m, n = len(A), len(B)
    dp = [[0] * (n + 1) for _ in range(m + 1)]   # row/col 0 = base case (zeros)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1          # diagonal + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # up vs left
    return dp[m][n]
```

Trace `A = "AGCAT"`, `B = "GAC"` (answer = 2, e.g. "AC" or "GC"):
```
        ""  G   A   C        ← B
   ""   0   0   0   0
   A    0   0   1   1        A==A → diag(0)+1 = 1
   G    0   1   1   1        G==G → diag(0)+1 = 1
   C    0   1   1   2        C==C → diag(1)+1 = 2  ← "GC"/"AC"
   A    0   1   2   2        A==A → diag(1)+1 = 2
   T    0   1   2   2        T matches nothing → max(up,left) carries 2
   ↑A
```
Each cell did one thing: matched the diagonal +1, or copied the bigger neighbor. The corner `dp[5][3] = 2` is the LCS length — you never enumerated subsequences.

**Edit Distance (LC72) reuses the exact same grid** — only the base case and recurrence change: `dp[i][0]=i`, `dp[0][j]=j`; on match take `dp[i-1][j-1]` free; else `1 + min(dp[i-1][j] delete, dp[i][j-1] insert, dp[i-1][j-1] replace)`.

```visual
type: table-heatmap
title: Same grid, two recurrences (LCS vs Edit Distance)
shows: that LCS and Edit Distance share the up/left/diagonal grid skeleton but differ only in base row/col and the match/mismatch formula (max+1 to maximize length vs 1+min to minimize cost)
elements: two side-by-side filled grids for short strings; left grid LCS with diagonal+1 highlighted on matches; right grid Edit Distance with base row 0..n and col 0..m shaded, and a mismatch cell showing 1+min of its three neighbors; a caption "diagonal=copy/match, up=delete, left=insert"
```

## Gotchas
- **Off-by-one indexing.** Cell `dp[i][j]` compares `A[i-1]` and `B[j-1]` (the grid is 1-indexed over prefixes, the strings are 0-indexed). Mix these up and everything shifts.
- **Wrong base case.** LCS bases are zeros; Edit Distance bases are `i` and `j` (deleting/inserting into the empty string). Forgetting the non-zero edit-distance base gives garbage for one-empty-string cases.
- **Coin Change II loop order.** To *count combinations* (not permutations), the **coin loop must be outer** and the amount loop inner. Swap them and you count ordered sequences, over-counting (e.g. 1+2 and 2+1 as distinct).
- **Regex `*` consumes a pair.** In LC10, `*` and its preceding char are one unit. "Zero of it" = `dp[i][j-2]` (drop the `x*`); "one more of it" = the char before `*` matches `text[i-1]` ⇒ `dp[i-1][j]`. The empty-pattern base and the `dp[0][j]` row (pattern vs empty text, only `*` can survive) are where people break.
- **State-machine DP isn't a string grid.** Don't force Stock-with-Cooldown into a two-sequence grid. Its "two indices" are *day* × *state*; cells are `hold/sold/rest`, not character matches.

## Python idioms
- Allocate with `dp = [[init] * (n+1) for _ in range(m+1)]`. **Never** `[[init]*(n+1)]*(m+1)` — that aliases one row m times and writes corrupt everything.
- **Space optimization:** when `dp[i][j]` only reads row `i-1` and `i`, keep two 1D rows (`prev`, `cur`) → O(min(m,n)) space. LCS, Edit Distance, and Coin Change II all collapse this way.
- For **counting knapsack** (Coin Change II) the whole thing is genuinely 1D: `dp = [0]*(amount+1); dp[0]=1; for coin: for a in range(coin, amount+1): dp[a] += dp[a-coin]`.
- `float('inf')` as the "impossible" sentinel when minimizing; guard against adding to it.
- `min`/`max` over the three neighbors reads cleanest as `1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 1143 | Longest Common Subsequence | M | `dp[i][j]`=LCS length; base zeros; match ⇒ `diag+1`; mismatch ⇒ `max(up,left)` |
| 72 | Edit Distance | M | same grid; base `dp[i][0]=i, dp[0][j]=j`; match ⇒ `diag`; else `1+min(up=del, left=ins, diag=replace)` |
| 10 | Regular Expression Matching | H | text×pattern boolean grid; char/`.` ⇒ `diag`; `*` ⇒ drop pair `dp[i][j-2]` OR repeat `dp[i-1][j]` if prev matches |
| 518 | Coin Change II | M | counting knapsack, coins×amount; **coin loop outer**; `dp[a] += dp[a-coin]`; base `dp[0]=1` |
| 309 | Best Time to Buy/Sell w/ Cooldown | M | state-machine DP over day×{hold,sold,rest}; `hold=max(hold, rest-price)`, `sold=hold+price`, `rest=max(rest, sold)` |
