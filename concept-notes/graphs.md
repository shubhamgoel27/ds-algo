# Graphs

## The engine in one sentence
A graph traversal is just "explore everything reachable from a start, but **mark each node visited so you never re-enter it**" — BFS when you need shortest hops on equal-cost edges, DFS when you just need reachability/connectivity.

## The one question that unlocks it
You already know tree traversal. A graph is the same code with **one extra line**. So ask:

**"What stops me from looping forever?"**

A tree can't cycle, so tree-DFS needs no bookkeeping. A graph *can* cycle (and can re-reach the same node by multiple paths), so the **visited set is non-negotiable** — it's the *only* structural difference between tree-DFS and graph-DFS. Mark a node the moment you commit to it, and a cyclic graph becomes a finite, acyclic walk.

## The mental model
Two axes decide everything. First: **BFS vs DFS**. Second: **is the graph explicit (nodes/edges) or implicit (a grid / a string-transform / a dependency list)?**

```
                  visited = the firewall against cycles

   DFS (stack / recursion)            BFS (queue)
   ───────────────────────            ──────────────────────
   go DEEP first                      go WIDE in rings
   "is it connected? / area?"         "fewest steps? / nearest?"
   flood fill, path-exists,           shortest path on UNWEIGHTED
   cycle detect, topo post-order      graph, multi-source spread

   Grid as implicit graph:  cell (r,c) ── edges ──> 4 neighbors
        (r-1,c) (r+1,c) (r,c-1) (r,c+1)    (sometimes 8-dir diagonals)
```

The deepest unlock: **BFS pops nodes in non-decreasing distance from the source.** The first time you reach a node via BFS, you reached it in the *fewest edges*. That single fact is why BFS = shortest path on unweighted graphs, and why **multi-source BFS** (seed the queue with *all* starts at once) computes "distance to the nearest source" for free — every node's first visit comes from whichever source is closest.

```visual
type: grid-animation
title: Multi-source BFS frontier expanding (Rotting Oranges)
shows: that seeding the queue with ALL rotten cells at once makes the frontier expand as one synchronized ring, so each fresh orange is reached by its NEAREST rotten source in minimum minutes
elements: a 3x3 grid; minute 0 = two cells marked R (rotten sources) at (0,0) and (0,2), the rest F (fresh); minute 1 = their 4-neighbor cells flip R simultaneously; minute 2 = next ring flips; color cells by the minute they turned, showing two wavefronts meeting in the middle; a side counter "minutes elapsed = max ring reached"
```

## The universal template

**DFS (recursion) — connectivity / flood fill / cycle work:**
```python
def dfs(node):
    visited.add(node)                 # ← mark ON ENTRY (the firewall)
    for nxt in neighbors(node):        # ← neighbors() defines the graph
        if nxt not in visited:         #   (grid: 4 dirs; explicit: adj[node])
            dfs(nxt)
```

**BFS — shortest hops / multi-source spread:**
```python
from collections import deque

def bfs(starts):
    q = deque(starts)                  # ← seed ONE source, or ALL sources
    visited = set(starts)              #   mark sources immediately, not on pop
    dist = 0
    while q:
        for _ in range(len(q)):        # ← drain one whole LEVEL = one step
            node = q.popleft()
            # process node at distance `dist`
            for nxt in neighbors(node):
                if nxt not in visited:
                    visited.add(nxt)   # ← mark ON ENQUEUE (avoids dup pushes)
                    q.append(nxt)
        dist += 1                      # ← one ring done, distance grows by 1
```

**Topological sort (Kahn / BFS with in-degrees) — ordering + cycle detection:**
```python
def topo(n, edges):                    # edge u→v means "u before v"
    adj = defaultdict(list); indeg = [0]*n
    for u, v in edges:
        adj[u].append(v); indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)   # ← no-prereq nodes
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1              # ← "u is done, drop one prereq from v"
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []   # ← short ⇒ CYCLE exists
```
Four blanks total: **`neighbors()`**, **when to mark visited**, **whether to drain by level**, and (topo) **the edge direction**.

## Variants / when to use
| Variant | Engine | Fires when | Catalog |
|---|---|---|---|
| Flood fill / area | DFS or BFS + visited | count/size connected components | 200, 695 |
| Shortest path, unweighted | **BFS, level by level** | "fewest steps/moves/transforms" | 1091, 127 |
| Multi-source BFS | BFS seeded with all sources | "time to fill all" / "dist to nearest" | 994, 417 |
| Reverse-flow trick | DFS/BFS from the *targets* inward | "cells that can reach BOTH borders" | 417 |
| Topological sort | Kahn BFS or DFS post-order | order with prereqs + detect cycle | 207, 210, 269 |
| DAG longest path | DFS + memo | longest chain, no cycles | 329 |
| Graph copy | DFS/BFS + `old→new` map | clone with shared structure | 133 |

## Worked example
**LC994 Rotting Oranges** — multi-source BFS. Every rotten orange rots its 4-neighbors each minute; return minutes until none are fresh, or `-1` if some can't be reached. "All sources spread simultaneously" ⇒ seed the queue with **every** rotten cell at minute 0.

```python
def orangesRotting(grid):
    R, C = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2: q.append((r, c))   # ← ALL sources up front
            elif grid[r][c] == 1: fresh += 1
    minutes = 0
    while q and fresh:                              # stop early if none left
        for _ in range(len(q)):                     # drain one minute's ring
            r, c = q.popleft()
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r+dr, c+dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2                # mark visited = "now rotten"
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1            # leftover fresh ⇒ unreachable
```

Trace on `grid = [[2,1,1],[1,1,0],[0,1,1]]` (2=rotten, 1=fresh, 0=empty). One source at (0,0), `fresh=6`:

```
start (min 0)      after min 1        after min 2        after min 3
2 1 1              2 2 1              2 2 2              2 2 2
1 1 0     ──▶      2 1 0     ──▶      2 2 0     ──▶      2 2 0
0 1 1              0 1 1              0 1 1              0 2 1   ... → 0 2 2

queue drains by LEVEL:
 q=[(0,0)]                 fresh=6
 min1: pop (0,0) → rot (0,1),(1,0)         q=[(0,1),(1,0)]  fresh=4
 min2: pop both → rot (0,2),(1,1)          q=[(0,2),(1,1)]  fresh=2
 min3: pop both → rot (2,1)                q=[(2,1)]        fresh=1
 min4: pop (2,1) → rot (2,2)               q=[(2,2)]        fresh=0  → return 4
```
Each orange flips the instant the wavefront reaches it — its first (and only) visit is via the shortest path from the nearest source. The `for _ in range(len(q))` is what slices the queue into discrete minutes.

## Gotchas
- **`list.pop(0)` is O(n).** Use `collections.deque` and `popleft()` for the queue, or BFS silently becomes O(V²).
- **Mark visited on ENQUEUE, not on dequeue.** If you wait until you pop, the same node gets pushed multiple times before its first pop, blowing up the queue and breaking distance correctness.
- **Drain by level or carry distance per node** — don't do both, and don't forget one. Either `for _ in range(len(q))` per step, or store `(node, dist)` tuples. Mixing them double-counts.
- **Multi-source ≠ run single-source N times.** Seed *all* sources into one queue first; then a single BFS sweep gives nearest-source distance. (994, and 417 where you BFS inward from each ocean's border cells.)
- **417 reverses the flow.** Water flows high→low, but you start DFS *from the ocean borders going to equal-or-higher* cells — far cheaper than testing every cell's path to both oceans. Intersect the two reachable sets.
- **Topo "short order" = cycle.** If Kahn's result has fewer than `n` nodes, a cycle starved them of in-degree 0. That's the cycle-detection answer for 207, and an invalid-ordering signal for 269.
- **`grid` mutation as visited** (994/200) is fine and saves a set — but only if you're allowed to mutate the input.

## Python idioms
- `from collections import deque` → O(1) `append` / `popleft`. The BFS workhorse.
- `defaultdict(list)` for adjacency lists; `defaultdict(int)` won't help in-degrees directly — build a `[0]*n` array or a dict.
- Direction vectors: `for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))` (8-dir for 1091: add the four diagonals).
- Bounds-check inline: `0 <= nr < R and 0 <= nc < C`.
- Clone-style map: `clone = {}` mapping `old_node -> new_node` doubles as the visited set (133).
- DFS+memo on a DAG: `@functools.lru_cache(None)` or a `memo` dict turns exponential path-search into O(V+E) (329).
- Recursion depth caps ~1000 — a 200×200 grid flood fill (200/695) can overflow; prefer an explicit stack or BFS for huge grids.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 133 | Clone Graph | M | DFS/BFS + `old→new` dict as visited; copy node, then recurse neighbors |
| 200 | Number of Islands | M | flood fill; `neighbors`=4-dir; each unvisited land cell launches one DFS, count launches |
| 695 | Max Area of Island | M | flood fill returning size; DFS returns `1 + sum(children)`, track global max |
| 1091 | Shortest Path in Binary Matrix | M | BFS, **8-dir**; shortest hops on unweighted grid; level count = path length |
| 994 | Rotting Oranges | M | **multi-source BFS**; seed all rotten cells; level = minutes; leftover fresh ⇒ -1 |
| 417 | Pacific Atlantic Water Flow | M | **multi-source, reverse flow**; DFS inward from each ocean's border to ≥ cells; intersect sets |
| 127 | Word Ladder | H | BFS on implicit graph; `neighbors`=words 1 letter apart; level = transform count |
| 207 | Course Schedule | M | topo sort; can finish ⇔ `len(order)==n` (no cycle) |
| 210 | Course Schedule II | M | topo sort; **return the order** (or `[]` if cycle) |
| 269 | Alien Dictionary | H | build edges from adjacent-word first diff, then topo sort; cycle ⇒ invalid |
| 329 | Longest Increasing Path in Matrix | H | **DFS + memo** on implicit DAG (edges to strictly-greater neighbors); answer = max memo |
