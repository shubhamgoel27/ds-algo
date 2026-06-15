# ds-algo

In 2024 I solved about fifty of these for interviews. By 2026 I had forgotten nearly all of it, which is the normal and slightly humbling fate of anything you cram and never revisit.

This is the second attempt, built so it sticks. It is a spaced-repetition system that re-serves problems cold on a schedule, plus a coaching loop (run with Claude) that will not hand over the answer and fuzz-tests every solution before it counts. The `.py` files are just the answer keys. The actual work is the forgetting curve losing.

## How a session actually goes

```
coach   LC153, find the minimum in a rotated sorted array. Statement only. Go.
me      <writes a binary search>
coach   8000 random rotations vs min(): all pass. But you picked nums[high] as
        the anchor from my hint, not from first principles. Here is why it is the
        only anchor that keeps the predicate monotonic...
me      rate it a 4, I leaned on the hint
coach   logged. next due July 4.
```

No solutions until I have genuinely tried. Stuck gets a hint, not the answer. Every solve is fuzz-tested against an independent brute force before it is allowed to count. Then I rate it 1 to 5 and the scheduler decides when I see it again: a clean solve disappears for eight weeks, a blank comes back tomorrow.

## The pieces

| file | what it is |
|---|---|
| `review.py` | the scheduler. `due` / `log` / `journal` / `stats`. Orders by confidence and by how often each problem actually shows up at the companies I care about. |
| `review.json` | every problem, its schedule, and a timestamped log of every attempt and what went wrong. |
| `REVIEW.md` · `SESSIONS.md` | the board (what is due) and the journal (what tripped me last time). |
| `CHEATSHEET.md` · `concept-bible.html` | pre-interview notes, and a tabbed reference for all 18 patterns. Open the bible. |
| `*.py` | the answer keys. Each runs its own tests. |

## The scoreboard *(2026-06-14, eight days in)*

23 problems back in memory, 25 attempts, 64 answer keys on file. Confidence by pattern (1 to 5):

```
Two Pointers · Stack · Linked List · Intervals   5.0
Trees                                            4.2
Binary Search                                    3.8
Graphs                                           3.5
Sliding Window                                   3.0   (was 1.5 two days ago)
Design                                           3.0
```

## The one stat I actually care about

Max Consecutive Ones III, a sliding-window problem: **rated 1 on June 11** (needed the whole solution handed to me). Re-served cold three days later, **rated 4** (wrote it from scratch, fixed my own bug). That jump, from "no idea" to "got it, mostly alone," is the entire reason this repo exists. Search in Rotated Sorted Array did the same thing, 2 to 3.

## Things I reliably get wrong

One bug has now shown up across rotated-array search, BST validation, two sliding-window problems, and binary-search-on-the-answer: **using `<` where it should be `<=`.** Same mistake, five disguises. The rule I keep re-learning: if the problem says *within / at most / at least*, the comparison is inclusive. "Within `h` hours" is `<= h`. Also a recurring fencepost or two (counting `n` days as `n-1`).

## The rules I run on

- Hints before answers. The answer is the last resort.
- Rate the floor. When unsure, rate lower; it just means I see it again sooner.
- Fuzz everything. A solution that has not beaten a brute-force reference does not count.
- Clear beats clever. The readable version wins, especially in an interview.

Eight days, 23 patterns relearned, one off-by-one I still cannot shake.
