# Per-Problem Workflow (do EVERY step, in order, no skipping)

This is the checklist for each problem in a revision session. The mode is **active
recall + spaced repetition**: serve the statement only, the user re-solves, then:

1. **Give hints, not solutions.** If stuck, nudge toward the bug/insight. Only hand over
   full code after several hints, or if they ask. Run their code against a battery +
   fuzz to show failures (evidence over assertion).
2. **TEST.** Run a named battery + a randomized fuzz vs an independent reference. For
   answer-key problems, diff against the saved `.py`. Report pass/fail with the output.
3. **TIPS (concept).** 2-4 crisp fundamentals: the invariant, the mental model, why it
   works, the family of problems it unlocks.
4. **PYTHON TOOLKIT.** Language/stdlib specifics for this pattern: the idioms, the
   gotchas (e.g. `[[]]*n` aliasing), complexity traps (`list.pop(0)` is O(n)), the
   stdlib shortcut (`deque`, `heapq`, `bisect`, `enumerate`, `defaultdict`, ...).
5. **HISTORY + VOCAB.** A short origin/history note (who invented it, when, the
   real-world problem it came from, where it runs today). PLUS one "word of the
   problem": a fun/useful vocab word with a one-line definition and a daily-life
   flex sentence. Pick a word that relates to the problem (e.g. parsimonious for a
   memory-frugal bounded heap). User is building vocab. (History added 2026-06-11,
   vocab added 2026-06-15, both per user request.)
6. **LOG with a note.** `python3 review.py log <key> <1-5> "<what tripped them>"`.
   Honest ratings (drives the spaced-rep schedule). Updates REVIEW.md + SESSIONS.md.
7. **SAVE clean file** (if newly solved or a cleaner rewrite): repo-style `.py` with
   tests; add `<lcid>: "<file>.py"` to OVERLAP in review.py.
8. **CHEATSHEET.** Add/update the concise entry in CHEATSHEET.md.
9. **COMMIT + PUSH.** Scope `git add` to session files only; direct to `main` (repo
   convention). No em dashes anywhere (commit messages included).

## Standing coaching notes
- Teach **return-value recursion** (user's stated goal): "define what the call returns,
  trust it, combine."
- Sliding window: **element updates state; state drives the decision.** No `else` branch
  on the current element.
- Boundary precision (`<` vs `<=`) is a recurring weak spot (rotated search, BST, windows).
- Reward readability judgment; the clear version beats the clever one-liner in interviews.
