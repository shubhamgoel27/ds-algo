# Design

## The engine in one sentence
"Implement a data structure where every operation is O(1)" almost never has a single-structure answer — you **pair two simple structures so each one covers the other's blind spot.**

## The one question that unlocks it
Don't hunt for the one magic container. Ask:
**"Which O(1) ops do I need, and which single structure gives each one — for free?"**
List the required ops. A hashmap gives you O(1) *lookup by key*. An array gives you O(1) *random access + append*. A doubly-linked list gives you O(1) *splice/reorder/evict at a known node*. No one of them gives all three. So you write down which structure earns each operation, then **glue them together with a shared key** — the hashmap points *into* the other structure so the slow op (find the thing) becomes O(1).

## The mental model
Every design problem is a **two-column ledger**: each operation on the left, the structure that makes it O(1) on the right. When two different structures own different rows, you keep *both* and let the hashmap bridge them.
```
 OPERATION            O(1) IF YOU HAVE...        so pair:
 ──────────────────   ───────────────────────    ──────────────────────────
 lookup by key        hashmap                     hashmap  ─┐
 reorder / evict      doubly-linked list   ◄──────────────  ├─ LRU (146)
 (LRU)                (splice at a node)          DLL      ─┘

 lookup by value      hashmap (val→index)         hashmap  ─┐
 random pick          dynamic array (arr[rand])   ◄─────────├─ RandomSet(380)
 insert / delete O(1) array append + swap-pop     array    ─┘
```
The hashmap is *always* one of the pair — it's the universal "make finding-it free" tool. The second structure is whatever owns the op the hashmap *can't* do: ordered eviction → DLL, indexed/random access → array.

```visual
type: before-after
title: Why pair a hashmap with a doubly-linked list (LRU)
shows: hashmap alone can't express recency order; DLL alone can't find a key fast; together each op is O(1)
elements: LEFT panel "hashmap only" {key→value boxes, label "O(1) get, but no order → eviction is O(n) scan"}. RIGHT panel "hashmap + DLL" {hashmap key→node arrows pointing into a horizontal DLL: head⇄A⇄B⇄C⇄tail; label "get: hash→node, then splice node to front O(1); evict: drop node before tail O(1), node.key tells hashmap which entry to delete"}
```

## The universal template
```python
class Design:
    def __init__(self):
        self.index = {}            # ← hashmap: key → (value | node | array-index)
        self.store = ???           # ← second structure: DLL or dynamic array
        # invariant: every live key is in BOTH; they never disagree

    def query(self, key):          # the O(1) lookup → hashmap earns this
        ...

    def mutate(self, key, ...):    # ← the op the hashmap can't do alone:
        #   • recency reorder?  → splice in the DLL
        #   • delete-anywhere?  → swap-with-last + pop in the array
        #   • capacity full?    → evict via the second structure, then
        node = self.index[key]     #     use node.key / stored value to
        del self.index[key]        #     keep the hashmap in sync
```
Two decisions only: **what the second structure is** (DLL vs array), and **how you keep the two in sync on delete** (node stores its own key / array stores value, dict stores index).

## Variants / when to use
| Pairing | Second structure earns | Use for |
|---|---|---|
| hashmap + doubly-linked list | O(1) recency reorder + evict-at-end | **LRU Cache (146)**, LFU |
| hashmap + dynamic array | O(1) random access + swap-pop delete | **Insert/Delete/GetRandom (380)** |
| hashmap of timestamps (just one map) | O(1) "have I seen this recently?" | **Logger Rate Limiter (359)** |

Rule of thumb: need **order/eviction** → DLL. Need **random / by-index** → array. Need only **recency-as-a-number** → a plain dict suffices, no second structure.

## Worked example
**LC380 — Insert Delete GetRandom O(1).** Required ops: `insert`, `remove`, `getRandom`, all O(1). `getRandom` *demands* an array (pick `arr[randint]`). But arrays delete in O(n)... unless you don't care about order. The trick: **to delete in O(1), swap the doomed element with the last element, then `pop()` the end** — popping the tail is O(1), and a dict maps each value to its current index so you know *where* to swap.

```python
import random
class RandomizedSet:
    def __init__(self):
        self.arr = []          # array: O(1) append + random access
        self.pos = {}          # hashmap: value → its index in arr

    def insert(self, val):
        if val in self.pos: return False
        self.pos[val] = len(self.arr)
        self.arr.append(val)
        return True

    def remove(self, val):
        if val not in self.pos: return False
        i = self.pos[val]
        last = self.arr[-1]
        self.arr[i] = last         # move last value into the hole
        self.pos[last] = i         # fix its index in the map
        self.arr.pop()             # O(1) tail pop
        del self.pos[val]
        return True

    def getRandom(self):
        return random.choice(self.arr)   # O(1) — arr stays gap-free
```
The whole point: deleting from the *middle* is forbidden (O(n) shift), so we relocate the last element into the gap and only ever pop the tail.

Trace — `insert(7), insert(3), insert(9), remove(3)`:
```
insert 7:  arr=[7]          pos={7:0}
insert 3:  arr=[7,3]        pos={7:0, 3:1}
insert 9:  arr=[7,3,9]      pos={7:0, 3:1, 9:2}

remove 3:  i = pos[3] = 1,  last = arr[-1] = 9
           arr[1] = 9   →   arr=[7,9,9]   (overwrite the hole)
           pos[9] = 1   →   pos={7:0, 3:1, 9:1}
           arr.pop()    →   arr=[7,9]     (drop stale tail)
           del pos[3]   →   pos={7:0, 9:1}
result:    arr=[7,9]   pos={7:0, 9:1}     ← gap-free, indices consistent
```
9 fell from index 2 into index 1, the dict followed, and the array stayed dense so `getRandom` is still uniform.

```visual
type: grid-animation
title: Swap-with-last O(1) delete (LC380)
shows: removing a middle element by overwriting it with the tail, then popping the tail, keeping the array contiguous
elements: array cells [7][3][9] with index labels 0,1,2 and a side dict {7:0,3:1,9:2}. Step1 highlight cell index1 (value3) as "doomed" and cell index2 (value9) as "last". Step2 arrow from 9→cell1 overwriting 3, dict updates 9:1. Step3 strike-through tail cell, dict drops 3. Final array [7][9] dict {7:0,9:1}
```

## Gotchas
- **LC380, the self-delete edge case**: if `val` *is* the last element, the swap is a harmless no-op — but make sure you `pop()` before/after consistently and that you don't delete from the dict and then re-add a stale index. The order in the code above is safe.
- **LC146, node must store its own key**: when you evict the LRU node off the DLL tail, you need to delete it from the hashmap too — but the dict is keyed by *key*, and you reached the node via the *list*. So each node carries `node.key`. Without it, eviction can't find the dict entry → O(n) reverse scan.
- **LC146, dummy head & tail**: use sentinel `head`/`tail` nodes so `_add`/`_remove` never special-case "first node" or "empty list" — no `if node.prev is None` branches. This is the single biggest source of LRU pointer bugs.
- **LC359, off-by-one on the window**: "rate limited to once per 10 seconds" means print iff `timestamp >= last_seen + 10` (allowed at exactly t+10, not t+9). Store the *next-allowed* time or the last-printed time consistently — don't mix them.

## Python idioms
- **`collections.OrderedDict`** *is* a hashmap + doubly-linked list in one. For LRU you can skip the from-scratch DLL: `od.move_to_end(key)` on access, `od.popitem(last=False)` to evict the oldest. Interviewers often want the hand-rolled version anyway — know both.
- **`functools.lru_cache` / `functools.cache`**: decorator-level LRU for memoizing pure functions; not for the class problem, but name-drop it.
- **`random.choice(list)`** / `random.randint` for LC380 — needs the underlying dense list; can't randomly sample a dict's keys in O(1).
- **DLL `_remove` / `_add_front` as atomic primitives**: write two tiny helpers that only re-wire 4 pointers each; every public method is then "remove then re-add," which makes the logic obvious and bug-free.
- `dict` membership (`val in d`) and `del d[k]` are O(1) average — the workhorse behind all three problems.

## The LRU node dance (LC146)
For completeness, the 146 pairing in code — `get`/`put` are both "unlink the node, relink at front; if over capacity, drop the tail's predecessor and erase its `node.key` from the dict":
```python
class Node:
    __slots__ = ('key','val','prev','next')
    def __init__(self, k=0, v=0):
        self.key, self.val, self.prev, self.next = k, v, None, None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                         # key → Node
        self.head, self.tail = Node(), Node() # dummy sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, n):                     # atomic: splice n out
        n.prev.next, n.next.prev = n.next, n.prev
    def _add_front(self, n):                  # atomic: insert after head
        n.next, n.prev = self.head.next, self.head
        self.head.next.prev = n
        self.head.next = n

    def get(self, key):
        if key not in self.map: return -1
        n = self.map[key]
        self._remove(n); self._add_front(n)   # mark most-recently-used
        return n.val

    def put(self, key, val):
        if key in self.map:
            self._remove(self.map[key])
        n = Node(key, val)
        self.map[key] = n
        self._add_front(n)
        if len(self.map) > self.cap:
            lru = self.tail.prev              # node just before tail = oldest
            self._remove(lru)
            del self.map[lru.key]             # ← node.key bridges DLL→dict
```

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 359 | Logger Rate Limiter | E | **hashmap only**: `msg → last-allowed timestamp`; print iff `ts >= map.get(msg, -inf)`, then set `map[msg]=ts+10`. No second structure — recency is just a number. |
| 146 | LRU Cache | M | **hashmap + doubly-linked list**: dict `key→node` for O(1) lookup; DLL for O(1) recency reorder + evict-at-tail; dummy head/tail; `node.key` lets eviction delete from the dict. |
| 380 | Insert Delete GetRandom | M | **hashmap + dynamic array**: array for O(1) append + `random.choice`; dict `value→index`; O(1) delete via swap-with-last-then-pop, dict follows the moved element. |
