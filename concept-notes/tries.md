# Tries (Prefix Trees)

## The engine in one sentence
A trie is a tree where **each edge is one character and shared prefixes share a path**, so every node represents *the prefix you spelled to reach it* — it fires whenever a problem asks "does anything start with…", "match with a wildcard", or "search many words at once."

## The one question that unlocks it
Stop thinking of words as strings in a set. Ask:
**"What if every prefix were a *place* I could stand, and walking one character moved me to exactly one neighbor?"**
A hashset can only answer "is this exact word present?" A trie answers "is this a *prefix* of anything?" for free — because reaching a node *is* the proof that the prefix exists. That single property (the node = a live prefix) is the whole pattern. Prefix queries and "explore all continuations" become a walk down the tree.

## The mental model
The node holds almost nothing: a dict of children and a boolean. The *path to the node* carries all the meaning.
```
           (root)              ← empty prefix ""
          /   |   \
        c     a    ...
        |     |
        a     n
        |     |•              • = is_end  →  "an" is a complete word
        t•                    "cat" is a complete word
        |
        s•                   "cats" is a complete word; "ca","cat" are prefixes (no •)
```
The two facts every trie problem leans on:
- **DOWN the path** = consuming characters one at a time. Missing child ⇒ dead end ⇒ prune.
- **is_end at a node** = "a word *ends here*." A node can be a prefix of many words yet not a word itself (`ca`, `cat` above have no `•`).

```visual
type: tree
title: A trie growing as you insert "cat", "cats", "an"
shows: that shared prefixes reuse the same path and is_end marks word boundaries, distinct from mere prefixes
elements: root node labeled ""; insert "cat" → chain c-a-t with t marked end(•); insert "cats" → reuse c-a-t, add s child marked end(•); insert "an" → new branch a-n with n marked end(•); color end-nodes green, non-end internal nodes grey; annotate "ca","cat" as prefixes-only
```

## The universal template
```python
class TrieNode:
    def __init__(self):
        self.children = {}        # ← dict[char, TrieNode]: one edge per character
        self.is_end = False       # ← True iff a word ends exactly here

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):                 # O(L)
        node = self.root
        for ch in word:
            if ch not in node.children:     # ← carve the path if missing
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True                  # ← stamp the word boundary

    def _walk(self, word):                  # shared helper: walk, return end node or None
        node = self.root
        for ch in word:
            if ch not in node.children:
                return None                 # ← dead end ⇒ prefix doesn't exist
            node = node.children[ch]
        return node

    def search(self, word):                 # full word present?
        node = self._walk(word)
        return node is not None and node.is_end   # ← MUST also be a word end

    def startsWith(self, prefix):           # any word with this prefix?
        return self._walk(prefix) is not None     # ← reaching the node is enough
```
Three decisions vary per problem: **what a "match" means at the final node** (`is_end` vs just "exists"), **whether the search can branch** (wildcards / a board), and **what you record as you build** (e.g. counting nodes).

## Variants / when to use
| Variant | Search shape | Final-node test | Use for |
|---|---|---|---|
| Exact word | single path | node exists **and** `is_end` | LC208 `search` |
| Prefix only | single path | node exists (ignore `is_end`) | LC208 `startsWith` |
| Wildcard `.` | **DFS, branch into all children on `.`** | `is_end` at end | LC211 |
| Count distinct substrings | insert every suffix's prefixes; **count new nodes** | — | LC1698 |
| Trie + board DFS | DFS the grid, **prune when path ∉ trie** | collect words at `is_end` | LC212 |

## Worked example
**LC212 — Word Search II.** Given a board and a word list, return all words found on the board (adjacent cells, no reuse). The naive approach runs a DFS per word: `O(words × board)`. The unlock: **put all words in one trie, then walk the board once**, and at each cell only continue if the current letter is a child in the trie. The trie *prunes the search* — paths that can't spell any word's prefix die instantly.

```python
def findWords(board, words):
    root = {}                                  # plain-dict trie: node = dict of children
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node['$'] = w                          # '$' sentinel stores the full word at its end

    R, C, res = len(board), len(board[0]), []

    def dfs(r, c, node):
        ch = board[r][c]
        nxt = node.get(ch)
        if nxt is None:                        # ← PRUNE: this letter extends no word
            return
        word = nxt.pop('$', None)              # found a complete word? collect once
        if word:
            res.append(word)
        board[r][c] = '#'                      # mark visited (no reuse)
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] != '#':
                dfs(nr, nc, nxt)
        board[r][c] = ch                       # restore (backtrack)
        if not nxt:                            # leaf emptied ⇒ snip dead branch (speedup)
            node.pop(ch)

    for r in range(R):
        for c in range(C):
            dfs(r, c, root)
    return res
```
Trace finding `["oath","pea","eat","rain"]` — start the DFS at cell `(0,0)='o'`:
```
trie prefixes that survive: o→a→t→h($), e→a→t($), p→e→a($), r→a→i→n($)

cell(0,0)='o'  → root['o'] exists      ✓ descend
  neighbor 'a' → node['a'] exists      ✓ descend     (spelling "oa")
    neighbor 't' → node['t'] exists    ✓ descend     (spelling "oat")
      neighbor 'h' → node['h']['$']="oath"  → COLLECT "oath"
cell(0,1)='a'  → root['a'] is None     ✗ PRUNE immediately (no word starts 'a')
```
You walked the board **once**. Every wrong turn was killed by a single `node.get(ch) is None` check — that's the trie doing the pruning the hashset never could.

## Gotchas
- **`search` needs `is_end`, `startsWith` does not.** If you reach the node for `"cat"` but it was only inserted as part of `"cats"`, `is_end` is False — `search("cat")` must return False, `startsWith("cat")` True. Conflating them is the classic LC208 bug.
- **LC211 wildcard: only `.` branches; a normal char is still a single step.** Don't DFS into all children for every letter — you'd explode the search and return wrong matches. Branch into *all* children **only** when the current pattern char is `.`.
- **LC212 backtracking: restore the cell AND consider snipping the trie.** Forgetting `board[r][c] = ch` corrupts the grid; forgetting to dedupe lets the same word collect twice (the `pop('$')` handles this — once popped it can't fire again).
- **LC1698: count NEW nodes, not insertions.** A distinct substring ⇔ a distinct path ⇔ a node that didn't exist before. If you count every character processed you over-count; only increment when you actually *create* a child.

## Python idioms
- `node.children[ch] = node.children.get(ch) or TrieNode()` — or, with a plain dict, `node = node.setdefault(ch, {})` for a one-liner descend-or-create.
- A **plain `dict` is often a faster trie than a class** (LC212): children are the dict itself, and a sentinel key like `'$'` marks word ends — fewer attribute lookups in hot DFS loops.
- Wildcard DFS: when `ch == '.'`, iterate `for nxt in node.children.values(): if dfs(...): return True` — `.values()` gives you "branch into everything."
- `defaultdict`-style descent and **snipping empty branches** (`node.pop(ch)` once a subtree is exhausted) shrinks LC212's search space as words are found.
- Insertion/search are **O(L)** in word length — independent of how many words the trie holds. That's the property a hashset of strings can't match for *prefix* queries.

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 208 | Implement Trie (Prefix Tree) | M | The base template verbatim: `children` dict + `is_end`. `insert`/`search`/`startsWith` all O(L); `search` tests `is_end`, `startsWith` doesn't. |
| 211 | Add and Search Words Data Structure | M | Same trie; `search` becomes **DFS** — on a literal char take one child, on `.` recurse into **all** children; succeed only at an `is_end` node when the pattern is consumed. |
| 1698 | Number of Distinct Substrings in a String | M | Insert every substring (each suffix's prefixes) into a trie; **each newly created node = one new distinct substring** → answer is the node count. |
| 212 | Word Search II | H | Build one trie of all words, then **DFS the board pruning when `board[r][c]` isn't a child of the current trie node**; collect at `is_end`/`'$'`. Turns O(words × board) into a single board walk. |
