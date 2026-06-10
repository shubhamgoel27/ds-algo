# Advanced Graphs / Union-Find

Three different graph engines live under this banner. Don't blur them — each fires on a distinct shape of question. **Union-Find** answers "are these two nodes in the same blob, and if I add this edge do I close a loop?" **Dijkstra** answers "cheapest cost to every node from a source, non-negative weights." **Hierholzer** answers "can I walk every edge exactly once, and what's that walk?" Pick the engine by the *question*, not the graph.

## The engine in one sentence
- **Union-Find (DSU):** a forest of `parent[]` pointers where every node lazily flattens toward its set's root, so "same component?" and "merge components" are both near-O(1) — fires the instant a problem is about *connectivity* or *cycle detection on undirected edges*.
- **Dijkstra:** a greedy BFS weighted by cost — a min-heap always pops the closest *unsettled* node, freezes its distance, and relaxes its neighbors; fires for *single-source shortest path with non-negative weights*.
- **Hierholzer:** greedily walk edges until stuck, append nodes *post-order*, reverse — fires for *Eulerian path* (use every edge exactly once).

## The one question that unlocks it
For each engine there's one reframe:

- **Union-Find:** *"Two nodes are connected iff they share a root."* You never store the actual blob — you store a pointer up to a representative. An edge between two nodes that **already share a root** is redundant: it's the one that forms a cycle.
- **Dijkstra:** *"The closest unsettled node can never be improved later"* (because all remaining edges add non-negative cost). So the moment you pop it from the heap, its distance is final — settle it and move on.
- **Hierholzer:** *"A node gets appended to the route only once you can't leave it."* You recurse out along edges first, and only when a node is a dead-end do you prepend it. Reverse at the end.

## The mental model

### Union-Find: pointers up to a root
A set is a tree of parent-pointers. `find(x)` climbs to the root; two nodes are in the same set iff `find(a) == find(b)`. `union` hangs one root under the other.
```
before union(2,4):           after union(2,4) (4's root → 2's root):

   1        3                       1        3
   |        |                       |        |
   2        4                       2 ─────→ 4
   |        |                       |        |
   5        6                       5        6
 find(5)=1  find(6)=3            find(6)=1, find(5)=1  → same set
```
Path compression: after `find(5)`, node 5 (and everything on the path) is re-pointed *directly* at the root, so the next lookup is O(1). Union by rank: always hang the shorter tree under the taller one so depth barely grows. Together → **O(α(n)) ≈ O(1)** amortized per op.

```visual
type: tree
title: DSU forest merging two components
shows: union by rank attaches the smaller-rank root under the larger, and find flattens the path via path compression
elements: two parent-pointer trees rooted at 1 (children 2,5) and 3 (child 4,6); a union(5,6) operation; show root(3) re-pointed under root(1); then show a find(6) call flattening 6 and 4 to point directly at root 1 with dashed "compressed" arrows
```

### Dijkstra: a settled frontier expanding outward
Nodes are in one of three states: **settled** (final distance known), **frontier** (in the heap, tentative distance), **unseen**. Each pop settles the cheapest frontier node; relaxing pushes cheaper tentative distances for its neighbors.
```
heap = [(0,src)]                 dist: src=0, rest=∞
pop (0,src)  → settle src,  relax → push (w,nbr) for each edge
pop smallest → settle it,   relax → push improved (newdist,nbr)
... repeat until heap empty ...  stale entries (dist already smaller) are skipped
```

## The universal template

### Union-Find (DSU)
```python
parent = list(range(n + 1))      # ← node ids; use n+1 if 1-indexed
rank   = [0] * (n + 1)

def find(x):                     # path compression
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # halve the path
        x = parent[x]
    return x

def union(a, b):                 # returns False if already connected
    ra, rb = find(a), find(b)
    if ra == rb:
        return False             # ← a + b already in same set (cycle / redundant edge)
    if rank[ra] < rank[rb]:      # union by rank: small under big
        ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]:
        rank[ra] += 1
    return True
```
Two decisions: **the id space** (0- vs 1-indexed, or coordinate-compressed) and **what `union` returning False means** for your problem (redundant edge, cycle, duplicate group).

### Dijkstra
```python
import heapq

def dijkstra(graph, src, n):     # graph[u] = list of (v, weight)
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[src] = 0
    heap = [(0, src)]            # (distance, node)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:          # ← stale entry, already settled cheaper → skip
            continue
        for v, w in graph[u]:    # relax neighbors
            nd = d + w
            if nd < dist[v]:     # ← found a cheaper path to v
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist                  # ← reduce to your answer (max, a target node, ...)
```
Two decisions: **how you build `graph`** (directed vs undirected adjacency with weights) and **how you reduce `dist`** into the final answer.

```visual
type: flow
title: Dijkstra frontier on a 4-node weighted graph
shows: each heap pop settles the closest node and relaxation updates tentative distances; stale heap entries are discarded
elements: nodes 1,2,3,4 with directed weighted edges 1->2(1), 1->3(4), 2->3(1), 2->4(2), 3->4(3); a heap column and a dist row evolving over 4 pops; settled nodes colored, frontier nodes outlined, the stale (4,3) entry struck through when (3,3) settles 3 first
```

## Variants / when to use
| Engine | Graph kind | Question it answers | Key property |
|---|---|---|---|
| Union-Find | undirected, incremental edges | same component? cycle? redundant edge? | α(n) per op; can't easily *delete* edges |
| Dijkstra | weighted, **non-negative** | single-source shortest distances | greedy: pop = settled; O(E log V) |
| Hierholzer | directed/undirected, edges to use once | Eulerian path/circuit (use every edge) | walk-till-stuck, append post-order, reverse |

## Worked example
**LC684 Redundant Connection (M)** — a tree of `n` nodes plus *one* extra edge. Return that extra edge. The extra edge is precisely the one whose two endpoints are **already connected** when you process edges in order — adding it would create a cycle. That's `union` returning False.

```python
def findRedundantConnection(edges):
    n = len(edges)
    parent = list(range(n + 1))
    rank   = [0] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False                # both already connected → this edge closes the cycle
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        rank[ra] += (rank[ra] == rank[rb])
        return True

    for a, b in edges:
        if not union(a, b):
            return [a, b]               # first edge that fails to union is the answer
```

Trace on `edges = [[1,2],[1,3],[2,3]]`:
```
start  parent = [0,1,2,3]              (index 0 unused)

[1,2]  find(1)=1, find(2)=2  differ → union, parent[2]=1
       parent = [0,1,1,3]
              1
             / \
            2

[1,3]  find(1)=1, find(3)=3  differ → union, parent[3]=1
       parent = [0,1,1,1]
              1
             /|\
            2 3

[2,3]  find(2)=1, find(3)=1  SAME root → union returns False
       ⇒ adding edge (2,3) would close a cycle  →  return [2,3]   ✓
```
You never built the graph or searched for a cycle — DSU detected it the instant an edge tried to merge a set with itself.

## Gotchas
- **Dijkstra with negative weights is wrong.** The "pop = settled" guarantee breaks the moment an edge can *decrease* a settled node's distance. Use Bellman-Ford for negatives.
- **Forgetting the stale-entry skip** (`if d > dist[u]: continue`) doesn't give a wrong answer but lets each node be reprocessed — silently O(E²) blowups. Keep it.
- **Union-Find indexing.** If nodes are 1-indexed (as in 684/743), size `parent` as `n+1` or you'll index out of range / mix up node 0.
- **Hierholzer must append post-order, then reverse.** If you append a node *before* exhausting its outgoing edges, you can paint yourself into a dead-end and drop edges. The reverse at the end is not optional.
- **Lexical Eulerian path (332):** you must visit destinations in sorted order. Use a min-heap (or sort + pop from the end) per source so the *smallest* airport is taken first.

## Python idioms
- `heapq` is a **min-heap** of tuples — `(dist, node)` sorts by dist then node, exactly what Dijkstra wants. No max-heap; negate for max.
- `parent[x] = parent[parent[x]]` is iterative **path halving** — same asymptotics as full compression, no recursion, no stack-depth risk.
- `rank[ra] += (rank[ra] == rank[rb])` — bool is an int in Python; bumps rank only on a tie. Tidy.
- `collections.defaultdict(list)` for adjacency; for 332's lexical walk, `defaultdict(list)` of destinations then `heapq.heapify` each list, or sort and `pop()` from the tail (O(1)).
- Hierholzer is cleanest **iterative** with an explicit stack — avoids recursion limits on long itineraries; append to `route` when a node has no edges left, then `route[::-1]`.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 684 | Redundant Connection | M | **Union-Find.** Process edges; the first edge where `union` returns False (endpoints already share a root) is the redundant one → return it. |
| 743 | Network Delay Time | M | **Dijkstra** from source `k` over directed weighted graph; answer = `max(dist.values())`, or `-1` if any node stays `inf` (unreachable). |
| 332 | Reconstruct Itinerary | H | **Hierholzer** Eulerian path from `"JFK"`. Min-heap of destinations per airport for lexical order; walk till stuck, append airport post-order, reverse the route. |
