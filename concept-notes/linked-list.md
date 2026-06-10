# Linked List

## The engine in one sentence
A linked list is just a chain of `node.next` pointers, and every problem is one of three moves on that chain — guard the head with a **dummy node**, walk it with **two pointers**, or rewire it with **prev/curr/next reversal** — where the only rule is *save `next` before you overwrite it*.

## The one question that unlocks it
Don't think about "the list." Think about **the one pointer you're about to clobber**. The instant you write `curr.next = something`, you've destroyed your only link to the rest of the chain — unless you stashed it first. So before any rewire, ask:
**"What does `curr.next` point to right now, and will I still need it after I overwrite it?"**
If yes, save it: `nxt = curr.next`. That single habit kills 90% of linked-list bugs.

## The mental model
Three primitives compose into every problem. Burn these into memory:
```
DUMMY HEAD            FAST / SLOW             REVERSE (3-pointer)
dummy → n1 → n2       slow→  fast→→           prev  curr  next
  ↑ return .next      gap or 2x speed         ←n1   n2 → n3
 head never special   finds mid / cycle /     flip curr.next=prev
 deletions trivial    n-th-from-end           then all shift right
```
- **Dummy head**: a fake node before `head` so the "first node" is never a special case. You build/delete by pointing at `dummy.next`, and return `dummy.next` at the end.
- **Fast/slow**: two pointers at different speeds (2x) or a fixed **gap**. Floyd's: if fast laps slow, there's a cycle. Equal-speed-with-gap finds the n-th-from-end.
- **Reverse**: three pointers march down the list flipping each `next` backward. This is the only one that mutates structure, and it's where saving `next` is non-negotiable.

```visual
type: pointer-walk
title: Fast/slow pointers finding the middle
shows: that fast moves 2 steps per slow's 1 step, so when fast hits the end, slow sits at the middle
elements: a 5-node list 1→2→3→4→5→null; three frames; frame1 slow@1 fast@1; frame2 slow@2 fast@3; frame3 slow@3 fast@5(null next); arrow labels "slow +1" "fast +2"; highlight node 3 as the returned middle
```

## The universal template
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

# ---- PRIMITIVE 1: dummy head (build or delete without head special-cases) ----
def with_dummy(head):
    dummy = ListNode(0, head)          # ← fake node in front of head
    tail = dummy                       # ← cursor you append to / advance
    while ...:                         # ← per-problem walk condition
        tail.next = chosen_node        # ← wire next link
        tail = tail.next
    return dummy.next                  # ← real head, head-edge-case-free

# ---- PRIMITIVE 2: fast / slow ----
def fast_slow(head):
    slow = fast = head
    while fast and fast.next:          # ← guard BOTH for 2x speed
        slow = slow.next               #   +1
        fast = fast.next.next          #   +2
    return slow                        # ← slow = middle (or use for cycle)

# ---- PRIMITIVE 3: in-place reversal ----
def reverse(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next                # ← SAVE next before clobbering it
        curr.next = prev               # ← flip the pointer backward
        prev, curr = curr, nxt         # ← shift both right
    return prev                        # ← new head (old tail)
```
The decisions per problem: **which primitive(s)**, the **walk condition**, and **what you wire** at each step.

## Variants / when to use
| Primitive | Signal in the problem | Use for |
|---|---|---|
| Dummy head | building a new list, or deleting nodes (incl. the head) | Merge Two Sorted, Add Two Numbers, Remove Nth, Merge K |
| Fast/slow (2x) | "middle", "is there a cycle", split list in half | Middle of List, Linked List Cycle, Reorder (find mid) |
| Fast/slow (gap of n) | "n-th from the end" in one pass | Remove Nth From End |
| Reverse | "reverse", or "rearrange" needing a backward half | Reverse List, Reorder (reverse 2nd half) |
| Find-mid + reverse + merge | reorder/fold a list onto itself | Reorder List |
| Heap / divide-conquer | merge *many* sorted lists | Merge K Sorted Lists |
| Hashmap old→new (or interleave) | nodes have a second pointer to copy | Copy List with Random Pointer |

## Worked example
**LC143 Reorder List** — the cleanest proof that everything composes. Turn `1→2→3→4→5` into `1→5→2→4→3`. That's three primitives back to back: **find middle** (fast/slow), **reverse the second half**, then **merge** the two halves alternately.

```python
def reorderList(head):
    if not head or not head.next:
        return
    # 1) find middle (slow lands on mid; second half starts at slow)
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    # 2) reverse the second half (everything after slow)
    prev, curr = None, slow.next
    slow.next = None                   # cut the list into two halves
    while curr:
        nxt = curr.next                # SAVE before clobber
        curr.next = prev
        prev, curr = curr, nxt
    # 3) merge first half (head) with reversed second half (prev), alternating
    first, second = head, prev
    while second:
        n1, n2 = first.next, second.next   # SAVE both before rewiring
        first.next = second
        second.next = n1
        first, second = n1, n2
```

Trace on `1→2→3→4→5`. After step 1, `slow` is at `3`. Step 2 reverses `4→5` into `5→4`, and step 3 zips them:
```
half A:  1 → 2 → 3 → null
half B:  5 → 4 → null         (was 4→5, reversed)

merge, alternating, saving n1/n2 each time:
  first=1 second=5 : 1→5→(2…)     n1=2 n2=4
  first=2 second=4 : 2→4→(3…)     n1=3 n2=null
  second=null → stop

result:  1 → 5 → 2 → 4 → 3
```
You never juggled the whole list — each primitive did its one job and handed off.

```visual
type: before-after
title: Reorder List = find-mid + reverse + merge
shows: the three-stage pipeline transforming 1→2→3→4→5 into 1→5→2→4→3
elements: row1 "1→2→3→4→5" with slow pointer under node 3; row2 split into "1→2→3" and reversed "5→4"; row3 interleaved result "1→5→2→4→3" with alternating arrows colored by source half
```

## Gotchas
- **Overwriting `next` before saving it.** `curr.next = prev` orphans the rest of the list. Always `nxt = curr.next` first — in reversal *and* in the merge step (save both `n1` and `n2`).
- **`while fast and fast.next` vs `while fast.next and fast.next.next`.** The first lands `slow` on the *second* middle of an even list (use for Middle of List, returning the second mid). The second stops `slow` on the *first* middle / left-of-center — what you want before splitting in Reorder. Pick deliberately.
- **Forgetting to cut the list.** In Reorder you must `slow.next = None`, else the reversed half still points back and you build a cycle.
- **Remove Nth off-by-one.** Advance `fast` by `n+1` (not `n`) from a dummy so `slow` stops on the node *before* the target, letting you do `slow.next = slow.next.next`.
- **Cycle detection needs `fast and fast.next`.** If you only check `fast`, you deref `None.next` at the end of an acyclic list.

## Python idioms
- **`heapq`** for Merge K: push `(node.val, i, node)` — include a tiebreaker index `i` because `ListNode` isn't comparable, so equal vals would otherwise crash the heap. `heappush`/`heappop` are `O(log k)`.
- **No manual comparators needed** for divide-and-conquer Merge K: just pairwise-merge lists, `O(N log k)` total, `O(1)` extra space (vs heap's `O(k)`).
- **`dummy = ListNode()`** is the universal scaffold; `return dummy.next` discards the fake head for free.
- **Carry arithmetic** (Add Two Numbers): `carry, digit = divmod(a + b + carry, 10)` keeps the loop tight; loop while `l1 or l2 or carry`.
- **Hashmap for Copy Random**: `dict` mapping `old_node → new_node`, `defaultdict`-free; first pass clones nodes, second pass wires `next`/`random` via the map. The `O(1)`-space alternative interleaves clones between originals.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 21 | Merge Two Sorted Lists | E | **Dummy head**; walk both, wire `tail.next` to the smaller, advance; attach leftover. |
| 141 | Linked List Cycle | E | **Fast/slow**; if `fast` ever meets `slow`, cycle exists; `fast` hitting `None` ⇒ none. |
| 206 | Reverse Linked List | E | **Reversal**; the bare prev/curr/next loop, `return prev`. The primitive itself. |
| 876 | Middle of the Linked List | E | **Fast/slow** at 2x; `while fast and fast.next`; `slow` = (second) middle. |
| 2 | Add Two Numbers | M | **Dummy head**; `divmod(a+b+carry,10)`; loop while `l1 or l2 or carry`. |
| 19 | Remove Nth From End | M | **Fast/slow gap**; advance `fast` `n+1` from dummy, move both till `fast` ends; `slow.next = slow.next.next`. |
| 138 | Copy List with Random Pointer | M | **Hashmap old→new** (or interleave clones); two passes to wire `next` and `random`. |
| 143 | Reorder List | M | **Compose all three**: find mid (fast/slow) → reverse 2nd half → merge alternately. |
| 708 | Insert into Sorted Circular List | M | Walk `prev/curr` around the ring; insert where `prev.val ≤ x ≤ curr.val`, or at the min/max wrap point; handle empty + uniform-value rings. |
| 23 | Merge K Sorted Lists | H | **Heap** of `(val, i, node)`, `O(N log k)`; or **divide-and-conquer** pairwise merge with the dummy-head merge of LC21. |
