# Sliding Window

## The engine in one sentence
A sliding window is two pointers `[left, right]` over a sequence where you only ever push `right` forward (grow) and push `left` forward (shrink) — never backward — so a brute-force O(n²) scan of all subarrays collapses to O(n) by reusing the window's running state.

## The one question that unlocks it
Brute force asks "for every start, scan every end." That's the trap. Instead ask:
**"As I extend `right` by one element, what invariant just broke — and can I restore it by only moving `left` forward?"**
If the answer is yes, you have a sliding window. The whole pattern is: the window carries a piece of running state (a count, a hashmap, a sum), and `left` only ever advances. Because both pointers march in one direction, each element is added once and removed at most once → O(n).

## The mental model
Every window problem is one of three shapes. The shape decides **when you shrink** and **when you record the answer**:
```
LONGEST-VALID            SHORTEST-VALID           FIXED-SIZE
grow right always        grow right always        grow right to size k
shrink WHILE invalid     shrink WHILE valid       slide: add right, drop left
record at EVERY step     record WHEN valid        record when len == k
(answer = max width)     (answer = min width)     (compare to target counts)
```
The pivot is the `while` condition. Longest: you tolerate validity and only kick in `left` when the window goes *bad*, recording width every iteration. Shortest: the moment the window is *good*, you greedily shrink to find the tightest good window. Fixed: width never changes — you just check a match each slide.

```
LONGEST (LC3: no repeats)            window over "abcabcbb"
 a  b  c  a  b  c  b  b
[a]                                  right=0  ok,   width 1
[a  b]                               right=1  ok,   width 2
[a  b  c]                            right=2  ok,   width 3  ← best
[a  b  c  a]                         right=3  'a' dup! invalid
    [b  c  a]                        shrink left past old 'a', ok again
```

```visual
type: grid-animation
title: Longest-valid window sliding over "abcabcbb"
shows: right always advances; when a duplicate enters, left jumps forward to restore the no-repeat invariant; the max width seen is the answer
elements: a row of 8 cells labeled a,b,c,a,b,c,b,b; a highlighted [left..right] band that grows rightward each frame; at right=3 the duplicate 'a' turns red and left snaps to index 1 so the band becomes [b,c,a]; a running "best=3" badge above the grid
```

## The universal template
```python
def sliding_window(s):
    from collections import defaultdict
    state = defaultdict(int)          # ← window's running state (counts/sum/distinct)
    left = 0
    best = 0                          # ← max width, min width, or a result accumulator

    for right in range(len(s)):
        state[s[right]] += 1          # ← STEP 1: add s[right] to window

        while invalid(state):         # ← STEP 2: invariant check (the heart)
            state[s[left]] -= 1       #            undo left's contribution
            left += 1                 #            shrink — left only moves forward

        best = max(best, right - left + 1)   # ← STEP 3: record (placement = the shape)
    return best
```
Three decisions: **what state** the window carries, **what `invalid()` means**, and **where you record** the answer (inside the `while` for shortest-valid, after it for longest-valid). For fixed-size, replace the `while` with an `if right >= k: drop s[right-k]` and compare counts.

## Variants / when to use
| Variant | Shrink rule | Record answer | State carried | Example |
|---|---|---|---|---|
| Longest-valid | `while` window is **invalid** | every step, `max(width)` | hashmap / counter | LC3, LC424, LC1004 |
| Shortest-valid | `while` window is **valid** | inside shrink, `min(width)` | need-counter + `have` | LC76 |
| Fixed-size (count match) | none — slide, drop `left` when `len > k` | when `len == k` and counts match | freq array / counter | LC438, LC567 |
| Fixed-size (max in window) | drop indices outside `[i-k+1]` | every full window | **monotonic deque** | LC239 |
| Best-prefix (degenerate) | never shrink | track running min/max | a scalar | LC121 |
| Circular fixed-size | window over `arr+arr` | every step | count of one value | LC2134 |

## Worked example
**LC424 Longest Repeating Character Replacement** — pick the longest window where, after replacing at most `k` chars, all chars are equal. This is a *longest-valid* window. A window is valid when `(window_width − count_of_most_frequent_char) ≤ k`; that difference is the number of replacements needed. Grow `right` always; when replacements exceed `k`, shrink `left` once.
```python
def characterReplacement(s, k):
    from collections import defaultdict
    count = defaultdict(int)
    left = 0
    max_freq = 0
    best = 0
    for right in range(len(s)):
        count[s[right]] += 1
        max_freq = max(max_freq, count[s[right]])   # most-frequent char in window
        # replacements needed = width - max_freq
        if (right - left + 1) - max_freq > k:        # invalid → shrink ONE step
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```
(Subtle: `max_freq` is never decreased on shrink. That's fine — the window only grows when a more frequent char appears, so a stale `max_freq` never inflates the answer.)

Trace on `s = "AABABBA"`, `k = 1`:
```
 idx:  0 1 2 3 4 5 6
 char: A A B A B B A
right=0 [A]          maxf=1 need=1-1=0 ≤1 ok  width=1 best=1
right=1 [A A]        maxf=2 need=2-2=0 ≤1 ok  width=2 best=2
right=2 [A A B]      maxf=2 need=3-2=1 ≤1 ok  width=3 best=3
right=3 [A A B A]    maxf=3 need=4-3=1 ≤1 ok  width=4 best=4  ← best
right=4 [A A B A B]  maxf=3 need=5-3=2 >1 → shrink: drop A, left=1
        [A B A B]    width=4 best=4
right=5 [A B A B B]  maxf=3 need=5-3=2 >1 → shrink: drop A, left=2
        [B A B B]    width=4 best=4
right=6 [B A B B A]  maxf=3 need=5-3=2 >1 → shrink: drop B, left=3
        [A B B A]    width=4 best=4
```
Answer `4`: replace one char in `AABA` (or `ABBA`) to get four equal chars. Each element entered and left the window once → O(n).

## The monotonic-deque variant (LC239)
Window max is **not** the count template — you can't "undo" a max by decrementing. Instead keep a **deque of indices** whose values are strictly decreasing front→back. The front is always the current window's max.
```python
def maxSlidingWindow(nums, k):
    from collections import deque
    dq = deque()          # holds INDICES, values decreasing front→back
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:   # pop smaller-or-equal from the back
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                # front index fell out of window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])       # front = max of this window
    return out
```
Why O(n): every index is appended once and popped at most once. The deque stays a clean "staircase" of candidates that could still become a future max. Smaller values to the left of a bigger newcomer are useless forever, so you discard them. This same deque idea generalizes to any "running max/min over a sliding window."

## Gotchas
- **Recording in the wrong place.** Longest-valid records *after* the `while` (window is valid there). Shortest-valid (LC76) records *inside* the shrink loop, right when the window first becomes valid, before you shrink past it.
- **`while` vs `if` on the shrink.** Longest-valid shrinks until valid again → `while`. But LC424's window can shrink at most one step per grow (width only drops by 1), so an `if` works there; using `while` is also correct, just unnecessary. Shortest-valid *must* use `while` to fully tighten.
- **Fixed-size off-by-one.** The first full window of size `k` completes at `right == k-1`. Drop the element leaving the window (`s[right-k]`) *before* comparing counts, or your frequency map drifts.
- **`have`/`need` bookkeeping (LC76).** Track a single `have` counter of how many *distinct required chars* are fully satisfied, not a full map comparison each step — comparing maps every iteration silently makes it O(n·Σ).
- **Window max by deletion.** Trying to maintain window max with a hashmap/counter and "remove on shrink" is wrong — you can't cheaply find the new max. Use the deque.

## Python idioms
- `from collections import deque` — O(1) `append`, `appendleft`, `pop`, `popleft`. **Never `list.pop(0)`** for the front: it's O(n) and silently turns the window into O(n²).
- `collections.Counter(t)` to build the "need" map for LC76/LC438/LC567; `Counter` equality (`==`) compares all counts in one expression for fixed-size matches.
- `defaultdict(int)` for frequency state so `count[c] += 1` never KeyErrors.
- A fixed 26-length list (`[0]*26`, index `ord(c)-ord('a')`) beats a `Counter` for anagram problems — array equality is a tight C-level compare and avoids hashing.
- For circular arrays (LC2134), index with `arr[i % n]` and run `right` over `[0, 2n)` to simulate wrap-around without copying the array.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 121 | Best Time to Buy and Sell Stock | E | Degenerate window: `left`=cheapest day so far, `right`=today; never shrink, track `max(price[right]-min_so_far)`. |
| 3 | Longest Substring Without Repeating Characters | M | Longest-valid; state = char→count; invalid when any count > 1; record width every step. |
| 424 | Longest Repeating Character Replacement | M | Longest-valid; state = char counts + `max_freq`; invalid when `width - max_freq > k`; record width. |
| 438 | Find All Anagrams in a String | M | Fixed-size `k=len(p)`; slide a freq array; emit `left` index whenever window counts == `p` counts. |
| 567 | Permutation in String | M | Fixed-size `k=len(s1)`; same as 438 but return `True` on first count match instead of collecting. |
| 1004 | Max Consecutive Ones III | M | Longest-valid; state = count of 0s in window; invalid when `zeros > k`; record width. |
| 2134 | Min Swaps to Group All 1's Together II | M | Circular fixed-size `k=total ones`; over `arr+arr` count 1s per window; answer = `k - max_ones_in_any_window`. |
| 76 | Minimum Window Substring | H | Shortest-valid; need-counter + `have`; valid when `have == len(need)`; shrink while valid, record `min` width inside. |
| 239 | Sliding Window Maximum | H | Fixed-size max; **monotonic deque** of indices, values decreasing; front = window max; not the count template. |
