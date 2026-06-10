# Trees (BFS + DFS)

## The engine in one sentence
A binary tree has two engines: **BFS** (a queue, level by level) when you care about *depth/levels*, and **DFS recursion** (trust the children, combine at the node) when you care about *subtree aggregates*.

## The one question that unlocks it
For DFS, don't trace the whole tree in your head — that's what makes it feel impossible. Ask exactly one thing:
**"Assuming the recursive call already works perfectly on my children, what do I do at THIS node?"**
You write the function *as if it's already finished*, call `dfs(node.left)`, and TRUST the answer. The base case bottoms it out.

For BFS, the only question is: **"how do I know where one level ends?"** — snapshot the queue length before draining it.

## The mental model
DFS asks which way information moves:
```
   DOWN ↓ (parameters)             UP ↑ (return values)
 parent hands context to child    child reports a fact to parent
 "valid bounds are (lo, hi)"      "my subtree height is 3"
 TOP-DOWN / pre-order             BOTTOM-UP / post-order
```
- Need DOWN? Pass it as a **parameter**.  - Need UP? **Return** it.  - Need both? Do both.

BFS keeps a frontier in a queue; each "round" of the while-loop is exactly one level:
```
queue: [3]          → level [3]
queue: [9,20]       → level [9,20]
queue: [15,7]       → level [15,7]
```

```visual
type: flow
title: DFS — two directions of information flow
shows: top-down passes state via params; bottom-up returns values; post-order combines children at the node
elements: a 3-node tree (root + two children); downward RED arrows labeled "params: bounds / path-sum"; upward BLUE arrows labeled "return: height / validity"; the root body labeled "combine(node, left, right)"
```

```visual
type: tree
title: BFS level snapshot
shows: that freezing len(queue) at the start of each while-iteration captures exactly one level
elements: tree [3 / 9,20 / 15,7]; three horizontal bands; each band annotated "n = len(queue) frozen here" with the node count for that level
```

## The universal template
DFS — the shape of nearly every tree problem:
```python
def dfs(node, state_from_parent):     # ← param = info flowing DOWN
    if node is None:                  # ← base case: the empty-subtree answer
        return identity_value         #   (0 for height, True for valid, None for LCA)
    left  = dfs(node.left,  ...)      # ← TRUST: correct answer for left subtree
    right = dfs(node.right, ...)      # ← TRUST: correct answer for right subtree
    # combine node + left + right → this node's answer
    return value_for_parent           # ← info flowing UP
```
BFS — level-by-level:
```python
from collections import deque
def bfs(root):
    if not root: return []
    q, out = deque([root]), []
    while q:
        n = len(q)                    # ← FREEZE: # nodes on this level
        level = []
        for _ in range(n):
            node = q.popleft()
            level.append(node.val)
            for c in (node.left, node.right):
                if c: q.append(c)
        out.append(level)
    return out
```
DFS decisions: the **base-case value** + the **combine step**. BFS decision: what you collect per level.

## Variants / when to use
| Traversal | Work happens | You have | Use for |
|---|---|---|---|
| Pre (node→L→R) | before recursing | parent's context | passing bounds/paths DOWN |
| In (L→node→R) | between | — | **BST → sorted order** (kth smallest, validate) |
| Post (L→R→node) | after recursing | both children's results | height, diameter, sums, validity |
| BFS (level) | per frontier round | the whole level | level grouping, shortest depth, right-side view |

## Worked example
**Max Depth (LC104)** — info flows UP ⇒ post-order, return-value. Empty subtree = depth 0.
```python
def maxDepth(node):
    if node is None: return 0
    return 1 + max(maxDepth(node.left), maxDepth(node.right))
```
Trace on `[3,9,20,null,null,15,7]`:
```
maxDepth(15) → 1        maxDepth(7) → 1
maxDepth(20) → 1+max(1,1) = 2
maxDepth(9)  → 1
maxDepth(3)  → 1+max(1,2) = 3      ← bubbles up to the root
```
You never traced the whole tree — each node did `1 + max(children)` and trusted the rest. That's the entire skill.

## Gotchas
- **Missing the `None` base case** → crash dereferencing a leaf's child.
- **"Return one thing but track another"**: Diameter (543) and Max Path Sum (124) *return* a single downward height/path to the parent while *side-tracking* a `nonlocal best` for the "path THROUGH this node" case. This is the #1 tricky tree idiom — see it once, you own it.
- **Wrong traversal order on a BST**: in-order is sorted; using pre/post loses that free ordering.
- **BFS: reading `len(q)` mid-loop** after you've enqueued children — freeze it first.
- **Deep skewed trees**: Python recursion caps ~1000 frames; a 10⁵-node degenerate tree needs an explicit stack.

## Python idioms
- `nonlocal best` to update an outer accumulator from inside the recursion (Diameter, Max Path Sum).
- **Tuple returns** carry multiple facts up: `return height, is_balanced`.
- `collections.deque` for BFS — `popleft()` is O(1); a list's `pop(0)` is O(n) and silently makes BFS O(n²).
- In-order generator: `yield from inorder(node.left); yield node.val; yield from inorder(node.right)` — clean for "kth smallest, stop early."

## Problem map
| LC | Problem | Df | How it fills the template |
|---|---|---|---|
| 100 | Same Tree | E | post; compare both nodes + both subtrees |
| 104 | Maximum Depth | E | post; base 0; combine `1+max(L,R)` |
| 226 | Invert Binary Tree | E | post/pre; swap `node.left, node.right` |
| 270 | Closest BST Value | E | top-down walk using BST property; track closest |
| 543 | Diameter | E | post; return height, side-track best `L+R` |
| 938 | Range Sum of BST | E | pre; prune subtrees outside `[lo,hi]` (BST) |
| 98 | Validate BST | M | pre; pass `(lo,hi)` DOWN; check `lo<val<hi` |
| 102 | Level Order Traversal | M | **BFS**; freeze `len(q)` per level |
| 105 | Construct from Pre+In | M | pre defines root; inorder splits L/R subtrees |
| 199 | Right Side View | M | **BFS**; take the last node of each level |
| 230 | Kth Smallest in BST | M | **in-order**; stop at the k-th |
| 236 | LCA of Binary Tree | M | post; both sides non-null ⇒ this node is the LCA |
| 426 | BST → Sorted DLL | M | **in-order**; stitch prev↔curr as you visit |
| 1650 | LCA III (parent ptrs) | M | two-pointer on parent chains (like list intersection) |
| 124 | Max Path Sum | H | post; return best downward arm, track best-through-node |
| 297 | Serialize / Deserialize | H | pre-order with null markers; rebuild from a queue |
| 987 | Vertical Order Traversal | H | **BFS** + column index; bucket by column, sort ties |
