# Intervals

## The engine in one sentence
Interval problems collapse the moment you **sort first** — then a single left-to-right sweep, holding only the *last kept interval* (or a *running count of what's open*), answers almost everything. The fire condition is any prompt about overlapping ranges: merge, insert, count rooms, remove the fewest, intersect.

## The one question that unlocks it
Before writing any code, ask the one question that decides everything:
**"Do I sort by START or by END?"**
That single choice is the whole problem. Sort by **start** when you sweep and *merge/extend* (Merge, Insert). Sort by **end** when you greedily *keep as many as possible* (Non-overlapping). And for "how many overlap at once," don't think intervals at all — think **events** on a number line. Pick the wrong key and the greedy stops being correct; pick the right one and the loop is five lines.

## The mental model
Two intervals `a` and `b` (with `a` starting first) overlap iff `a.end >= b.start`. Touching counts: `[1,2]` and `[2,3]` share the point `2`, so `<=` (not `<`) means overlap.
```
sort-by-start sweep              vs        event sweep (counting)
─────────────────────                      ──────────────────────
keep ONE running interval                  walk a sorted list of +1 / -1
[1,3] [2,6] [8,10]                         starts ↑   ends ↓
 └──┬──┘   └─┘                             time → +1 +1 -1 ...  track running max
 last.end >= cur.start? extend : flush     max concurrent = answer
```
The dichotomy: do you need the **shape** of the merged ranges (keep the last interval) or just **how many are simultaneously alive** (keep a counter)? Shape ⇒ sweep last-kept. Count ⇒ events or a min-heap of end times.

```visual
type: pointer-walk
title: Sort-by-start sweep merging intervals
shows: that after sorting by start, you compare each interval only against the last merged one, extending its end on overlap
elements: a horizontal timeline 0..10; bars [1,3],[2,6],[8,10]; a "last" bracket starting at [1,3]; arrow to [2,6] with label "2<=3 → overlap, end=max(3,6)=6"; merged bar [1,6]; arrow to [8,10] with label "8>6 → flush, start new"; output [[1,6],[8,10]]
```

## The universal template

**Template A — sort by start, sweep keeping the last interval** (merge / insert):
```python
def sweep(intervals):
    intervals.sort(key=lambda x: x[0])        # ← SORT KEY: by start
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:           # ← OVERLAP TEST: touching counts (<=)
            out[-1][1] = max(out[-1][1], e)   # ← MERGE: extend last.end
        else:
            out.append([s, e])                # ← else start a fresh interval
    return out
```

**Template B — count max concurrent** (rooms / max overlap). Two equivalent views:
```python
# View 1: min-heap of end times — pop rooms that freed up before this start
import heapq
def min_rooms(intervals):
    intervals.sort(key=lambda x: x[0])        # ← sort by start
    heap = []                                 # heap of end times of busy rooms
    for s, e in intervals:
        if heap and heap[0] <= s:             # ← earliest-ending room is free? reuse it
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)                          # ← peak heap size = max concurrent

# View 2: chronological events — +1 at each start, -1 at each end
def min_rooms_events(intervals):
    starts = sorted(s for s, e in intervals)
    ends   = sorted(e for s, e in intervals)
    i = j = cur = best = 0
    while i < len(starts):
        if starts[i] < ends[j]:               # ← a start before next end → +1, new room
            cur += 1; i += 1
            best = max(best, cur)
        else:                                  # ← an end ≤ this start → -1, room frees
            cur -= 1; j += 1
    return best
```

**Template C — greedy by end time** (keep the most non-overlapping):
```python
def max_nonoverlap(intervals):
    intervals.sort(key=lambda x: x[1])        # ← SORT KEY: by END
    kept, last_end = 0, float('-inf')
    for s, e in intervals:
        if s >= last_end:                     # ← no overlap with last kept → take it
            kept += 1; last_end = e           #   greedily lock in earliest end
    return kept
```

## Variants / when to use
| Sub-pattern | Sort key | State you hold | Use for |
|---|---|---|---|
| Sweep last-kept | **start** | last merged interval | merge ranges, insert, "any overlap?" |
| Min-heap end times | **start** | heap of active end times | max concurrent / min rooms |
| Event counting | starts & ends separately | running `+1/-1` counter | max concurrent (no heap) |
| Greedy earliest-end | **end** | last kept end | max non-overlapping / min removals |
| Two-pointer intersect | already sorted | two indices | intersection of two interval lists |

## Worked example
**LC253 Meeting Rooms II** — minimum rooms = maximum number of meetings overlapping at any instant. This is a *count*, not a shape, so use events.

Input `[[0,30],[5,10],[15,20]]`. Split and sort:
```
starts = [0, 5, 15]
ends   = [10, 20, 30]
```
Walk both pointers, always advancing whichever event comes first; a start is `+1` (need a room), an end is `-1` (room frees). Ties: an end at the same time frees a room *before* the next start, so `start < end` is the branch test.
```
ASCII timeline (each '#' = a meeting alive):
 0    5   10   15   20        30
[0,30] ##########################   (room A, never frees in window)
   [5,10]  #####                    (room B)
            [15,20] #####           (room B reused!)

step | event      | cur | best
-----|------------|-----|-----
 -   | start 0    |  1  |  1
 -   | start 5    |  2  |  2   ← two alive (0..30 and 5..10)
 -   | end 10     |  1  |  2
 -   | start 15   |  2  |  2   ← reuses the freed room, peak stays 2
 -   | end 20     |  1  |  2
 -   | end 30     |  0  |  2
```
Peak concurrency = **2 rooms**. The heap view gives the same answer: at start 15 the earliest end (10) ≤ 15, so pop and reuse — heap never exceeds size 2.

```visual
type: bar-steps
title: Max concurrent meetings via running event count
shows: how the +1/-1 sweep over sorted start/end events tracks a running count whose peak is the room count
elements: three interval bars [0,30],[5,10],[15,20] on a 0..30 axis; below them a step line rising +1 at t=0, +1 at t=5 (peak=2), -1 at t=10, +1 at t=15 (back to 2), -1 at t=20, -1 at t=30; annotation "peak = 2 = min rooms"
```

## Gotchas
- **Touching endpoints.** For merge/overlap, `[1,2]` and `[2,3]` overlap → use `s <= last.end`. But for *meeting rooms* (LC252/253), back-to-back meetings `[1,2],[2,3]` do **not** conflict — an ending meeting frees the room exactly when the next starts. That flips the tie-break: in event counting, advance the **end** when `start == end` (use `starts[i] < ends[j]`).
- **Wrong sort key kills the greedy.** Non-overlapping (LC435) needs sort by **end** — keeping the earliest-finishing interval leaves the most room. Sort by start there and the greedy is simply wrong.
- **Min removals = total − max kept.** LC435 asks for removals, but the clean greedy counts what you *keep*; subtract from `len`. Same problem, inverted framing.
- **Don't reuse the same room twice in one step.** In the heap view, pop *at most one* freed room per incoming meeting (an `if`, not a `while`) — otherwise you under-count rooms.

## Python idioms
- `intervals.sort(key=lambda x: x[0])` for start, `key=lambda x: x[1])` for end. This O(n log n) sort dominates the runtime; the sweep itself is O(n).
- `heapq` is a **min-heap**, exactly right for "earliest end time": `heap[0]` peeks the soonest-freeing room, `heappop`/`heappush` are O(log n).
- For event counting, sorting `starts` and `ends` into two arrays and merging with two pointers avoids building a combined event list — same result, less allocation.
- Mutating `out[-1][1] = ...` requires list intervals (not tuples). If inputs are tuples, append `[s, e]` lists into `out`.
- `bisect` shines in **Insert Interval (LC57)** to locate where the new interval lands, though a clean three-phase linear pass (before / overlapping-merge / after) is the more common interview answer.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 252 | Meeting Rooms | E | sort by start; sweep checking `cur.start < prev.end` for ANY overlap → return False; touching is allowed |
| 56 | Merge Intervals | M | Template A; sort by start, merge when `s <= last.end`, extend `last.end = max(...)` |
| 57 | Insert Interval | M | input pre-sorted; three phases — copy intervals before, merge all overlapping with the new one (`max`/`min` the bounds), copy after |
| 253 | Meeting Rooms II | M | Template B; min-heap of end times OR `+1/-1` event sweep; answer = peak concurrency |
| 435 | Non-overlapping Intervals | M | Template C; sort by **end**, greedily keep earliest-ending; removals = `len − kept` |
| 986 | Interval List Intersections | M | two-pointer over both sorted lists; overlap `= [max(a.s,b.s), min(a.e,b.e)]`, valid iff `lo <= hi`; advance the list whose end is smaller |
