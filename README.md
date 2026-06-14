# ds-algo — a memory that fights back

This is not a folder of LeetCode solutions. It is a **spaced-repetition training system** that re-serves problems cold, makes me re-derive them from scratch, grades the attempt, and schedules the next showing based on how badly it went. Solutions are just the answer key. The point is the forgetting curve, and beating it.

> Most algo repos are a graveyard: solve it once, paste it, never look again. This one drags problems back out of the grave on a schedule and asks, "OK, do it again. No looking."

---

## How it works

**Active recall + spaced repetition.** Every session: I get the problem statement only, re-solve it from memory, the solution gets fuzz-tested against a reference, I rate myself 1 to 5, and the tracker reschedules. A clean solve disappears for 8 weeks. A blank comes back tomorrow.

```
rating  1 blank   2 partial   3 effort   4 clean   5 instant
next    +1 day    +3 days     +1 week    +3 weeks  +8 weeks
```

## The machine

| File | What it is |
|---|---|
| `review.py` | the engine. `build` / `due` / `log` / `gen` / `journal` / `stats`. Schedules by confidence, prioritizes by ask-frequency at target companies. |
| `review.json` | source of truth: 140 problems, per-problem SR state + full timestamped attempt history. |
| `REVIEW.md` | the tracker board (what is due, by topic). |
| `SESSIONS.md` | the journal of **what tripped me**, per attempt. The most useful file here. |
| `CHEATSHEET.md` | concise pre-interview notes, one block per pattern. |
| `concept-bible.html` | a tabbed reference of all 18 patterns in the "here's the unlock" voice, with rendered figures. Open it. |
| `SESSION_WORKFLOW.md` | the per-problem ritual so no step gets skipped. |
| `*.py` | the answer keys. Each runs its own tests (`python3 file.py`). |

## How to play

Talk to the coach, not the files:
- `what's due?` — today's re-reviews + the queue
- `review N` — the N most overdue / weakest, one at a time
- `quiz me on <pattern>` — drill a topic (graphs, sliding window, binary search...)
- `random` — interview mode, no pattern hint

---

## Current standings *(snapshot, 2026-06-14)*

**21 / 140 reviewed · 63 answer keys · 9 fives · 1 one.**

Patterns ranked by confidence (the leaderboard):

```
5.0  ██████████  Two Pointers · Stack · Linked List · Intervals
4.2  ████████░░  Trees
3.8  ███████░░░  Binary Search
3.5  ███████░░░  Graphs
3.0  ██████░░░░  Design
1.5  ███░░░░░░░  Sliding Window   <- the boss to beat
```

## The Nemesis

One bug has shown up in the journal **20 times** across rotated-array search, BST validation, sliding windows, and binary-search-on-the-answer:

> **strict vs inclusive** (`<` where it should be `<=`).

The standing rule, earned the hard way: **when the problem says "within / at most / no more than / at least," the comparison is inclusive.** "Within `h` hours" is `<= h`. If this repo has a final exam, it is that one character.

---

## House rules

- **Hints, not solutions.** Stuck means a nudge, not the answer. The answer is the last resort.
- **Rate the floor.** When in doubt, rate lower. Costs a little review time, buys certainty it actually stuck.
- **Evidence over vibes.** Every solve is fuzz-tested against an independent reference before it counts.
- **The clear version beats the clever one-liner.** Readability is graded.

Built as a daily coaching loop. The forgetting curve is undefeated, but the gap is closing.
