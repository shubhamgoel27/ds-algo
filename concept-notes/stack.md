# Stack

## The engine in one sentence
A stack is your memory for *the most recent thing still waiting to be resolved* — it fires whenever the answer to "what do I match/cancel/compare against?" is always the **last** unfinished item, not the first.

## The one question that unlocks it
Don't ask "how do I scan this." Ask:
**"When I hit element X, which earlier element does it pair with — and is it always the most recent one still open?"**
If yes, that earlier element is sitting on top of a stack, waiting. A closing `)` matches the *last* `(`. A warmer day resolves the *most recent* colder day. An operator consumes the *last two* operands. Last-In-First-Out isn't a data-structure trivia fact — it's the literal shape of "nesting" and "most recent pending."

One deep cut that justifies the whole pattern: **balanced parentheses is not a regular language.** A finite-state machine (regex, a fixed set of `if`s) physically cannot count arbitrary nesting depth — you need unbounded memory of "how many opens am I inside?" That memory is a stack. A stack + state machine = a *pushdown automaton*, the minimum machine that can parse nesting. When you smell nesting, you smell a stack.

## The mental model
Every stack problem is one of three jobs. Burn this trichotomy in:
```
 MATCH / NEST            MONOTONIC               EVALUATE
 push openers,           keep stack sorted,      push operands,
 pop+check on closer     pop while new elem      pop & apply on
                         breaks the order        operator/close
 "()[]{}", "a/../b"      "next greater day"      "3 4 + ", "1+(2-3)"
 stack holds: what's     stack holds: indices    stack holds: partial
 still OPEN               still WAITING for       results not yet
                         their answer            collapsed
```
The unifying invariant: **the stack always holds exactly the items that are still pending, ordered most-recent-on-top.** You push when something becomes pending; you pop when something resolves it.

```visual
type: state-machine
title: The three jobs of a stack
shows: that all stack problems push a "pending" item and pop when an incoming element resolves it, branching by what "resolve" means
elements: a central STACK column (LIFO, top highlighted); three labeled inflows — MATCH (closer pops matching opener), MONOTONIC (bigger element pops all smaller waiting indices), EVALUATE (operator pops 2 operands → pushes result); each shows one push arrow in and one pop arrow out of the top cell
```

## The universal template
```python
def stack_solve(seq):
    stack = []                       # ← holds PENDING items (openers / indices / operands)
    for i, x in enumerate(seq):
        while stack and resolves(stack[-1], x):   # ← MONOTONIC/EVAL: incoming x settles the top
            top = stack.pop()
            record(top, x)           # ← e.g. answer[top] = i - top, or apply operator
        if is_pending(x):            # ← MATCH/MONOTONIC: this x now waits
            stack.append(x)          #   (push index for monotonic, char for matching)
    return finalize(stack)           # ← leftovers = never-resolved (unmatched / no greater elem)
```
The four blanks: **what you push** (char vs index vs value), **`resolves`** (the pop condition), **`record`** (what a pop produces), and **how you read the leftovers**. Matching uses the `if/pop-once` form; monotonic and eval use the `while/pop-many` form.

## Variants / when to use
| Sub-pattern | Stack holds | Pop trigger | Tells you | Problems |
|---|---|---|---|---|
| Match / nest | open symbols (or their type) | a closer arrives | is it balanced / valid | LC20, LC1249, LC71 |
| Monotonic (incr/decr) | **indices** waiting for an answer | new elem breaks the order | next greater/smaller + distance | LC739 |
| Evaluate (postfix) | operands | operator arrives | fold expression | LC150 |
| Evaluate (infix + parens) | running result + sign | `(` push context, `)` collapse | nested arithmetic | LC224 |
| Augmented stack | value **+** side-info (e.g. min) | normal pop | O(1) extra query | LC155 |
| Generate via implicit stack | the path so far (recursion) | backtrack | enumerate valid nestings | LC22 |

## Worked example
**LC739 Daily Temperatures** — for each day, how many days until a warmer one. The decreasing **monotonic stack** does it in O(n): keep a stack of *indices* whose answer is still unknown, in strictly decreasing temperature order. When today is warmer than the top, today *is* that day's answer — pop and record the gap.

Why it's O(n) not O(n²): every index is pushed once and popped at most once. The inner `while` is amortized O(1).

```python
def dailyTemperatures(T):
    ans = [0] * len(T)
    stack = []                       # indices, temps strictly decreasing top→down
    for i, t in enumerate(T):
        while stack and T[stack[-1]] < t:   # today resolves all colder waiting days
            j = stack.pop()
            ans[j] = i - j           # distance to next warmer day
        stack.append(i)              # i now waits for ITS warmer day
    return ans                       # never-popped indices keep ans=0
```
Trace on `T = [73, 74, 75, 71, 69, 72, 76, 73]` (showing stack as indices, with temps):
```
i=0 t=73  stack empty        push 0          stack=[0]            (73)
i=1 t=74  74>73 → pop 0, ans[0]=1-0=1        stack=[1]            (74)
i=2 t=75  75>74 → pop 1, ans[1]=2-1=1        stack=[2]            (75)
i=3 t=71  71<75 → no pop      push 3          stack=[2,3]         (75,71)
i=4 t=69  69<71 → no pop      push 4          stack=[2,3,4]       (75,71,69)
i=5 t=72  72>69 → pop 4 ans[4]=5-4=1
          72>71 → pop 3 ans[3]=5-3=2
          72<75 → stop         push 5         stack=[2,5]         (75,72)
i=6 t=76  76>72 → pop 5 ans[5]=6-5=1
          76>75 → pop 2 ans[2]=6-2=4
                              push 6          stack=[6]           (76)
i=7 t=73  73<76 → no pop      push 7          stack=[6,7]         (76,73)
end       leftovers 6,7 keep ans=0
```
Result: `[1, 1, 4, 2, 1, 1, 0, 0]`. Each colder day sat on the stack exactly until the first warmer day walked past and knocked it off.

```visual
type: bar-steps
title: Daily Temperatures monotonic stack
shows: the decreasing stack of indices shrinking when a warmer day arrives and pops every colder pending day in one sweep
elements: temperature bars [73,74,75,71,69,72,76,73]; a stack region holding pending indices with their bar heights strictly decreasing top→down; at i=5 (72) highlight popping indices 4 then 3 and writing ans=1,2; at i=6 (76) highlight popping 5 then 2 writing ans=1,4
```

## Gotchas
- **Push indices, not values, for monotonic stacks.** You almost always need the *position* to compute a distance (`i - j`) or to index back into the array. Storing the value alone throws that away.
- **`list.pop(0)` is O(n)** — that's a queue op, not a stack op. A stack only ever touches `stack[-1]` and `stack.append`/`stack.pop()`, all O(1). If you reach for `pop(0)`, you've confused stack with queue.
- **Empty-stack peek crashes.** Always guard `while stack and ...` / `if stack`. A lone closer `)` with nothing to pop means *invalid* (LC20) — handle it, don't index `stack[-1]` blind.
- **Leftovers are the answer, not garbage.** Unpopped openers in LC20 = unbalanced. Unpopped indices in LC739 = no warmer day (ans stays 0). Don't forget to read what's still on the stack at the end.
- **Calculator sign handling (LC224):** the sign belongs to the *number after* it; on `(`, push the running `result` and current `sign` so the inside computes fresh, then on `)` fold back as `result*saved_sign + saved_result`.

## Python idioms
- A plain `list` *is* the stack: `append` to push, `pop()` to pop, `stack[-1]` to peek, `if stack:` for non-empty. No need for `collections.deque` unless you also pop from the front.
- For matching, a dict of pairs reads cleanly: `pairs = {')':'(', ']':'[', '}':'{'}`; on a closer, check `stack and stack[-1] == pairs[c]`.
- **Min Stack (LC155):** store tuples `(val, min_so_far)` — `stack.append((x, min(x, stack[-1][1] if stack else x)))`. Then `getMin` is `stack[-1][1]`, O(1), no rescans.
- **RPN (LC150):** `int(...)` is fine for `+ - *`, but division truncates toward zero, so use `int(a / b)` not `a // b` (floor division gives wrong sign on negatives).
- **String building from a stack:** for LC71 Simplify Path, `'/' + '/'.join(stack)` after splitting on `/` and skipping `''`, `.`, and popping on `..`.
- For LC22 the "stack" is the recursion call stack / an explicit path list you append-and-pop during backtracking — same LIFO shape, no literal `stack` object.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 20 | Valid Parentheses | E | match; push openers, on closer pop+compare via pairs dict; valid iff stack empty at end |
| 1249 | Minimum Remove to Make Valid | M | match; push `(` indices, pop on `)`; unmatched `(` left on stack + stray `)` → delete those indices |
| 71 | Simplify Path | M | match/nest; split on `/`; push real names, `..` pops, `.`/`''` skipped; join leftovers |
| 739 | Daily Temperatures | M | monotonic decreasing; stack of indices, pop while `T[top] < t`, record `i - j` |
| 150 | Evaluate RPN | M | evaluate; push operands, on operator pop 2, apply (`int(a/b)` for div), push result |
| 224 | Basic Calculator | H | evaluate infix; track `result, sign`; `(` pushes `(result, sign)`, `)` folds back |
| 155 | Min Stack | M | augmented; each entry carries `min_so_far` alongside value → O(1) `getMin` |
| 22 | Generate Parentheses | M | implicit stack (backtracking); push `(` if opens<n, `)` if closes<opens; record when len==2n |
