# Concept Explainer Spec — follow this EXACTLY

You are writing ONE concept explainer for a LeetCode interview-prep "concept bible."
Match the voice and structure of the gold-standard example at the bottom. The reader is a
strong engineer relearning patterns for frontier-lab / big-tech interviews — assume intelligence,
kill hand-waving, give the *mental model* not a textbook.

## Voice rules
- Second person, direct, energetic. "Here's the unlock." "Burn this into memory."
- Lead with the *reframe* that makes the pattern obvious, not the definition.
- Every claim concrete. NO fabricated LC numbers or complexities — only use the problems you're given.
  If unsure of a fact, omit it. Accuracy > completeness.
- Python only. Real, runnable-looking code. Tight.
- Concise but complete. Aim ~250–450 lines of markdown.

## Required sections (use these exact `##` headers, adapt the prose)
1. `## The engine in one sentence` — 1–2 sentences naming the core idea + when it fires.
2. `## The one question that unlocks it` — the single reframe that makes the pattern click.
3. `## The mental model` — the central dichotomy/invariant (like "info DOWN vs UP" for DFS).
   MUST include an ASCII diagram. ALSO include a fenced ` ```visual ` block (see VISUAL SPECS).
4. `## The universal template` — a Python skeleton with `# ← fill-in` comments marking the
   2–4 decisions that vary per problem. This is the heart — make it copy-pasteable scaffolding.
5. `## Variants / when to use` — a markdown table of sub-patterns and when each applies.
6. `## Worked example` — pick ONE representative problem from your list. Show the approach,
   the code, AND a traced execution (ASCII, like the maxDepth trace in the example).
7. `## Gotchas` — 2–4 traps that actually bite (off-by-ones, wrong data structure, edge cases).
8. `## Python idioms` — stdlib + language specifics for this pattern (deque, heapq, bisect,
   defaultdict, complexity gotchas like list.pop(0) being O(n), etc.).
9. `## Problem map` — a markdown table: every problem you're given, mapped to how it fills the
   template (the "blanks"). Columns: `LC | Problem | Df | How it instantiates the pattern`.

## VISUAL SPECS — how to request diagrams
Where a picture beats prose, emit a fenced block:
```visual
type: <flow | state-machine | grid-animation | before-after | tree | pointer-walk | table-heatmap | bar-steps>
title: <short title>
shows: <one precise sentence on what the diagram must convey>
elements: <the nodes/cells/arrows/labels to draw, concretely enough to render as SVG/HTML>
```
Use 1–3 visual blocks total — only where they genuinely aid understanding (a two-pointer walk,
a DP table filling, a recursion tree, a sliding window expanding/contracting). Keep the ASCII
version too as a fallback.

## Output
Write the finished markdown to the file path you are given. Start with a top-level
`# <Concept Name>` line. Do not include this spec. End with one line of confirmation as your reply.

---
---

# GOLD-STANDARD EXAMPLE (this is the quality + voice bar) — concept: Tree DFS / Recursion

# Tree DFS / Recursion

## The engine in one sentence
Recursion on a tree = "assume the call already works on my children; I only decide what to do at THIS node." The base case bottoms it out.

## The one question that unlocks it
Don't trace the whole tree in your head — that's what makes it feel impossible. Ask exactly one thing:
**"Assuming the recursive call already works perfectly on my children, what do I do at this node?"**
You write the function *as if it's already finished*, call `dfs(node.left)`, and TRUST the answer.

## The mental model
Every tree-DFS problem asks: which way does information move?
```
   DOWN ↓ (parameters)            UP ↑ (return values)
 parent hands context to child   child reports a fact to parent
 "valid bounds are (lo,hi)"      "my subtree height is 3"
 TOP-DOWN / pre-order            BOTTOM-UP / post-order
```
- Need DOWN? Pass it as a **parameter**. - Need UP? **Return** it. - Need both? Do both.

```visual
type: flow
title: Two directions of information flow
shows: that top-down passes state via params while bottom-up returns values, and post-order combines children
elements: a small 3-node tree; downward red arrows labeled "params (bounds/path)"; upward blue arrows labeled "return (height/validity)"; node body labeled "combine(node,left,right)"
```

## The universal template
```python
def dfs(node, state_from_parent):     # ← param = info flowing DOWN
    if node is None:                  # ← base case: the empty-subtree answer
        return identity_value         #   (0 for height, True for valid, ...)
    left  = dfs(node.left,  ...)      # ← TRUST: correct answer for left subtree
    right = dfs(node.right, ...)      # ← TRUST: correct answer for right subtree
    # combine node + left + right → this node's answer
    return value_for_parent           # ← info flowing UP
```
Two decisions only: the **base-case value** and the **combine step**.

## Variants / when to use
| Order | Work happens | You have | Use for |
|---|---|---|---|
| Pre (node→L→R) | before recursing | parent context | passing bounds/paths down |
| In (L→node→R) | between | — | **BST → sorted order** (kth smallest, validate) |
| Post (L→R→node) | after recursing | both children's results | height, diameter, sums, validity |

## Worked example
**Max Depth** — info flows UP, so post-order, return-value. Empty subtree = depth 0.
```python
def maxDepth(node):
    if node is None: return 0
    return 1 + max(maxDepth(node.left), maxDepth(node.right))
```
Trace on `[3,9,20,null,null,15,7]`:
```
maxDepth(15)→1   maxDepth(7)→1
maxDepth(20)→1+max(1,1)=2
maxDepth(9) →1
maxDepth(3) →1+max(1,2)=3   ← bubbles to root
```
You never traced the whole tree — each node did `1+max(children)` and trusted the rest.

## Gotchas
- Forgetting the `None` base case → crash on leaf children.
- "Return one thing but track another": Diameter/Max-Path-Sum *return* a downward height while
  side-tracking a global best for the through-node case. The #1 tricky tree idiom.
- In-order on a BST is sorted — using the wrong order loses that.

## Python idioms
- `nonlocal best` to update an outer accumulator from the recursion.
- Recursion depth: Python caps ~1000; deep/skewed trees may need an explicit stack.
- Tuple returns to pass multiple facts up: `return height, is_balanced`.

## Problem map
| LC | Problem | Df | How it fills the template |
|---|---|---|---|
| 104 | Maximum Depth | E | post; base 0; combine `1+max(L,R)` |
| 543 | Diameter | E | post; return height, side-track best `L+R` |
| 98 | Validate BST | M | pre; pass `(lo,hi)` down; check `lo<val<hi` |
| 230 | Kth Smallest in BST | M | in-order; stop at k-th |
| 236 | LCA | M | post; both sides non-null ⇒ this node |
| 124 | Max Path Sum | H | post; return best downward path, track best-through-node |
