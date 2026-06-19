#!/usr/bin/env python3
"""Revision tracker — active recall + spaced repetition over the merged LC catalog.

Source of truth: review.json (this dir). Human view: REVIEW.md (auto-generated).

Subcommands:
  build   (re)create review.json by merging frontier-lab-prep/lc-problems.json
          with the locally-solved ds-algo files. Preserves existing SR state.
  due [N] list problems due today (most overdue / weakest first). N optional.
  log KEY RATING [NOTE...]   record a review of KEY (LC id or filename) at
          RATING 1-5, append NOTE to its history, reschedule next due date.
  gen     regenerate REVIEW.md and SESSIONS.md from review.json.
  journal print the full attempt history, newest first.
  stats   coverage + confidence summary.
"""
import json, sys, os
from datetime import date, timedelta, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "review.json")
CATALOG = os.path.join(HERE, "..", "frontier-lab-prep", "lc-problems.json")
VIEW = os.path.join(HERE, "REVIEW.md")
JOURNAL = os.path.join(HERE, "SESSIONS.md")

# rating -> days until next review
INTERVAL = {1: 1, 2: 3, 3: 7, 4: 21, 5: 56}

# --- overlap: ds-algo file <-> catalog LC id (problem already solved locally) ---
# New solutions written during review sessions get appended here so the tracker
# marks them as having a local answer key (survives `build`).
OVERLAP = {
    20: "valid_parentheses.py",  # solved 2026-06-07 session
    33: "search_rotated_array.py",  # solved 2026-06-07 session (with help)
    206: "reverse_linked_list.py",  # solved 2026-06-07 session
    102: "level_order_traversal.py",  # solved 2026-06-07 session (one hint)
    167: "two_sum_sorted.py",  # solved 2026-06-11 session (two pointers, clean)
    11: "container_with_water.py",  # solved 2026-06-11 session (greedy two pointers)
    424: "longest_repeating_char_replacement.py",  # solved 2026-06-14 session (window, richer state)
    567: "permutation_in_string.py",  # solved 2026-06-15 session (fixed-size window)
    704: "binary_search.py",  # solved 2026-06-12 session (vanilla template, clean)
    153: "find_min_rotated.py",  # solved 2026-06-13 session (boundary/keep-mid convention)
    875: "koko_bananas.py",  # solved 2026-06-14 session (binary search on the answer)
    215: "kth_largest.py",  # solved 2026-06-15 session (bounded heap)
    79: "word_search.py",  # solved 2026-06-18 session (grid backtracking, given)
    78: "subsets.py",  # solved 2026-06-16 session (backtracking intro)
    46: "permutations.py",  # solved 2026-06-16 session (backtracking, used set)
    226: "invert_binary_tree.py",  # solved 2026-06-09 session (DFS warm-up)
    98: "validate_bst.py",  # solved 2026-06-09 session (bounds-down, clean)
    146: "lru_cache.py", 560: "subarray_sum_k.py", 543: "diameter_of_tree.py",
    155: "min_stack.py", 199: "right_view_of_tree.py", 207: "course_scheduler.py",
    695: "max_area_of_island.py", 973: "k_closest_to_origin.py",
    138: "copy_ll_with_random_node.py", 133: "clone.graph.py",
    238: "product_of_all_except_self.py", 347: "k_most_frequent.py",
    200: "no_of_islands.py", 56: "merged_intervals.py", 994: "rotten_oranges.py",
    295: "median_of_stream.py", 3: "longest_substring_without_repeating.py",
    252: "meeting_rooms.py", 236: "lca_of_binary_tree.py", 19: "delete_nth_from_last.py",
}

# --- extras: solved locally but NOT in the catalog (mostly company-specific) ---
# (id, title, difficulty, topic, file). LC ids are best-effort; urls built from slug.
EXTRAS = [
    (224, "Basic Calculator", "H", "Stack", "basic_calculator.py", "basic-calculator"),
    (628, "Maximum Product of Three Numbers", "E", "Arrays & Hashing", "max_product_of_three.py", "maximum-product-of-three-numbers"),
    (26, "Remove Duplicates from Sorted Array", "E", "Two Pointers", "remove_duplicates_from_sorted_array.py", "remove-duplicates-from-sorted-array"),
    (767, "Reorganize String", "M", "Heap / PQ", "reorganize_string.py", "reorganize-string"),
    (88, "Merge Sorted Array", "E", "Two Pointers", "merge_sorted_arrays.py", "merge-sorted-array"),
    (1091, "Shortest Path in Binary Matrix", "M", "Graphs", "shortest_path_in_binary_grid.py", "shortest-path-in-binary-matrix"),
    (893, "Groups of Special-Equivalent Strings", "E", "Arrays & Hashing", "special_equivalent_strings.py", "groups-of-special-equivalent-strings"),
    (1249, "Minimum Remove to Make Valid Parentheses", "M", "Stack", "min_remove_valid_parenthesis.py", "minimum-remove-to-make-valid-parentheses"),
    (987, "Vertical Order Traversal of a Binary Tree", "H", "Trees", "binary_tree_vertical_traversal.py", "vertical-order-traversal-of-a-binary-tree"),
    (31, "Next Permutation", "M", "Two Pointers", "next_permutation.py", "next-permutation"),
    (1011, "Capacity To Ship Packages Within D Days", "M", "Binary Search", "capacity_to_ship_packages.py", "capacity-to-ship-packages-within-d-days"),
    (670, "Maximum Swap", "M", "Greedy", "swap_digits_for_max_number.py", "maximum-swap"),
    (1650, "Lowest Common Ancestor of a Binary Tree III", "M", "Trees", "lca_with_parent.py", "lowest-common-ancestor-of-a-binary-tree-iii"),
    (329, "Longest Increasing Path in a Matrix", "H", "Graphs", "longest_increasing_path.py", "longest-increasing-path-in-a-matrix"),
    (528, "Random Pick with Weight", "M", "Binary Search", "random_pick_with_weight.py", "random-pick-with-weight"),
    (876, "Middle of the Linked List", "E", "Linked List", "middle_of_ll.py", "middle-of-the-linked-list"),
    (791, "Custom Sort String", "M", "Arrays & Hashing", "custom_sort_string.py", "custom-sort-string"),
    (162, "Find Peak Element", "M", "Binary Search", "peak_in_array.py", "find-peak-element"),
    (359, "Logger Rate Limiter", "E", "Design", "logger_rate_limiter.py", "logger-rate-limiter"),
    (426, "Convert BST to Sorted Doubly Linked List", "M", "Trees", "bst_to_sorted_dll.py", "convert-binary-search-tree-to-sorted-doubly-linked-list"),
    (283, "Move Zeroes", "E", "Two Pointers", "move_zeros.py", "move-zeroes"),
    (1698, "Number of Distinct Substrings in a String", "M", "Tries", "count_distinct_substring.py", "number-of-distinct-substrings-in-a-string"),
    (270, "Closest Binary Search Tree Value", "E", "Trees", "return_closest_in_bst.py", "closest-binary-search-tree-value"),
    (408, "Valid Word Abbreviation", "E", "Two Pointers", "valid_word_abbr.py", "valid-word-abbreviation"),
    (938, "Range Sum of BST", "E", "Trees", "range_sum_of_bst.py", "range-sum-of-bst"),
    (708, "Insert into a Sorted Circular Linked List", "M", "Linked List", "insert_into_circular_node.py", "insert-into-a-sorted-circular-linked-list"),
    (986, "Interval List Intersections", "M", "Intervals", "interval_intersection.py", "interval-list-intersections"),
    (438, "Find All Anagrams in a String", "M", "Sliding Window", "find_anagrams_in_string.py", "find-all-anagrams-in-a-string"),
    (71, "Simplify Path", "M", "Stack", "simplify_path.py", "simplify-path"),
    (249, "Group Shifted Strings", "M", "Arrays & Hashing", "group_shifted_sequences.py", "group-shifted-strings"),
    (2134, "Minimum Number of Swaps to Group All 1's Together II", "M", "Sliding Window", "min_swaps_to_group_ones.py", "minimum-number-of-swaps-to-group-all-1s-together-ii"),
    (1004, "Max Consecutive Ones III", "M", "Sliding Window", "max_consecutive_ones.py", "max-consecutive-ones-iii"),
]

# topic display order for the view
TOPIC_ORDER = [
    "Arrays & Hashing", "Two Pointers", "Sliding Window", "Stack", "Binary Search",
    "Linked List", "Trees", "Tries", "Heap / PQ", "Backtracking", "Graphs",
    "Adv. Graphs / UF", "DP · 1D", "DP · 2D", "Greedy", "Intervals", "Bit / Math", "Design",
]
DIFF_ORDER = {"E": 0, "M": 1, "H": 2}


def load():
    with open(DATA) as f:
        return json.load(f)


def save(probs):
    with open(DATA, "w") as f:
        json.dump(probs, f, indent=2)


def today():
    return date.today()


def now_ts():
    """Full local timestamp (minute precision) for the attempt history."""
    return datetime.now().isoformat(timespec="minutes")


def when(h):
    """Best available time for a history entry: full ts if present, else date."""
    return h.get("ts") or h.get("date") or ""


def parse_due(p):
    """Return a date for sorting; 'now'/unreviewed sorts as very overdue."""
    d = p["sr"]["due"]
    return date(1970, 1, 1) if d == "now" else date.fromisoformat(d)


def is_due(p, ref=None):
    ref = ref or today()
    return parse_due(p) <= ref


def build():
    with open(CATALOG) as f:
        catalog = json.load(f)
    prev = {p["id"]: p for p in load()} if os.path.exists(DATA) else {}

    fresh = {"conf": None, "last_reviewed": None, "due": "now", "reps": 0}

    def carry(cid):
        p = prev.get(cid, {})
        return p.get("sr", dict(fresh)), p.get("history", [])

    probs = []
    for c in catalog:
        f = OVERLAP.get(c["id"])
        sr, hist = carry(c["id"])
        probs.append({
            "id": c["id"], "title": c["title"], "difficulty": c["difficulty"],
            "topic": c["topic"], "companies": c.get("companies", []),
            "sources": c.get("sources", []), "url": c["url"],
            "file": f, "in_catalog": True, "sr": sr, "history": hist,
        })
    for (cid, title, diff, topic, file, slug) in EXTRAS:
        sr, hist = carry(cid)
        probs.append({
            "id": cid, "title": title, "difficulty": diff, "topic": topic,
            "companies": [], "sources": ["ds-algo"],
            "url": f"https://leetcode.com/problems/{slug}/",
            "file": file, "in_catalog": False, "sr": sr, "history": hist,
        })
    probs.sort(key=lambda p: (TOPIC_ORDER.index(p["topic"]) if p["topic"] in TOPIC_ORDER else 99,
                              DIFF_ORDER.get(p["difficulty"], 9), p["id"]))
    save(probs)
    solved = sum(1 for p in probs if p["file"])
    print(f"built review.json: {len(probs)} problems "
          f"({solved} with local answer key, {len(probs) - solved} new)")


def freq(p):
    """Ask-frequency proxy = # of companies tagging it (catalog signal)."""
    return len(p.get("companies", []))


def due(argv):
    n = int(argv[0]) if argv else None
    probs = [p for p in load() if is_due(p)]
    # overdue first, then highest company-frequency, then lowest confidence
    probs.sort(key=lambda p: (parse_due(p), -freq(p), p["sr"]["conf"] or 0))
    if n:
        probs = probs[:n]
    for p in probs:
        key = p["file"] or f"LC{p['id']}"
        flag = "✓key" if p["file"] else "new"
        co = ",".join(p.get("companies", [])) or "-"
        print(f"LC{p['id']:<5} {p['difficulty']} {p['title']:<46} {p['topic']:<18} "
              f"f{freq(p)} [{co:<8}] [{flag}]  {key}")
    print(f"\n{len(probs)} shown.")


def find(probs, key):
    if key.upper().startswith("LC"):
        key = key[2:]
    for p in probs:
        if str(p["id"]) == key or p["file"] == key or (p["file"] and p["file"].rstrip(".py") == key):
            return p
    return None


def log(argv):
    if len(argv) < 2:
        sys.exit('usage: review.py log KEY RATING [NOTE...]')
    key, rating = argv[0], int(argv[1])
    note = " ".join(argv[2:])
    if rating not in INTERVAL:
        sys.exit("rating must be 1-5")
    probs = load()
    p = find(probs, key)
    if not p:
        sys.exit(f"not found: {key}")
    nxt = today() + timedelta(days=INTERVAL[rating])
    p["sr"] = {"conf": rating, "last_reviewed": today().isoformat(),
               "due": nxt.isoformat(), "reps": p["sr"]["reps"] + 1}
    p.setdefault("history", []).append(
        {"date": today().isoformat(), "ts": now_ts(), "conf": rating, "note": note})
    save(probs)
    print(f"logged LC{p['id']} {p['title']}: conf {rating}, "
          f"rep {p['sr']['reps']}, next due {p['sr']['due']}")
    gen()


def journal():
    probs = load()
    entries = []
    for p in probs:
        for h in p.get("history", []):
            entries.append((when(h), p, h))
    entries.sort(key=lambda e: e[0], reverse=True)
    for w, p, h in entries:
        print(f"{w:16}  LC{p['id']:<5} conf {h['conf']}  {p['title']}")
        if h.get("note"):
            print(f"                    ↳ {h['note']}")


def stats():
    probs = load()
    total = len(probs)
    reviewed = [p for p in probs if p["sr"]["reps"] > 0]
    due_n = sum(1 for p in probs if is_due(p))
    print(f"Total: {total} | reviewed: {len(reviewed)} | due now: {due_n} "
          f"| with answer key: {sum(1 for p in probs if p['file'])}")
    print("\nBy topic (reviewed/total, mean conf):")
    for t in TOPIC_ORDER:
        tp = [p for p in probs if p["topic"] == t]
        if not tp:
            continue
        rv = [p for p in tp if p["sr"]["conf"]]
        mc = f"{sum(p['sr']['conf'] for p in rv)/len(rv):.1f}" if rv else " - "
        print(f"  {t:<18} {len(rv):>2}/{len(tp):<2}  conf {mc}")


def gen():
    probs = load()
    t = today()
    lines = []
    lines.append("# Revision Tracker — Active Recall + Spaced Repetition\n")
    lines.append("> Auto-generated from `review.json` by `review.py gen`. Don't hand-edit — "
                 "log reviews with `python3 review.py log <key> <1-5>`.\n")
    solved = sum(1 for p in probs if p["file"])
    due_n = sum(1 for p in probs if is_due(p, t))
    rev_n = sum(1 for p in probs if p["sr"]["reps"] > 0)
    lines.append(f"**{len(probs)} problems** — {solved} with a local answer key (active recall vs your "
                 f"saved solution), {len(probs)-solved} new (learn from scratch). "
                 f"**{rev_n} reviewed, {due_n} due today ({t.isoformat()}).**\n")
    lines.append("**Mode:** active recall — you get the statement only, re-solve, then we diff & you rate 1–5.  ")
    lines.append("**Priority:** spaced repetition — overdue/weak surface first.\n")
    lines.append("Say: `review N` · `quiz me on <topic>` · `what's due?` · `random`.\n")
    lines.append("| Rating | 1 blank | 2 partial | 3 effort | 4 clean | 5 instant |")
    lines.append("|---|---|---|---|---|---|")
    lines.append("| Next due | +1d | +3d | +1wk | +3wk | +8wk |\n")
    lines.append("`key` = answer-key file ✓ or `new`. Conf = last rating. Due `now` = never/overdue.\n")
    lines.append("---\n")
    for topic in TOPIC_ORDER:
        tp = [p for p in probs if p["topic"] == topic]
        if not tp:
            continue
        tp.sort(key=lambda p: (DIFF_ORDER.get(p["difficulty"], 9), p["id"]))
        nkey = sum(1 for p in tp if p["file"])
        lines.append(f"## {topic}  ({nkey}/{len(tp)} solved)")
        lines.append("| LC | Problem | Df | Key | Conf | Last | Due | Reps |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for p in tp:
            sr = p["sr"]
            key = "✓" if p["file"] else "new"
            link = f"[{p['title']}]({p['url']})"
            lines.append(f"| {p['id']} | {link} | {p['difficulty']} | {key} | "
                         f"{sr['conf'] or '—'} | {sr['last_reviewed'] or '—'} | {sr['due']} | {sr['reps']} |")
        lines.append("")
    with open(VIEW, "w") as f:
        f.write("\n".join(lines))
    gen_journal(probs, t)
    print(f"wrote {VIEW} and {JOURNAL}")


def gen_journal(probs, t):
    """Readable per-attempt journal — what tripped you, for targeted revision."""
    entries = []
    for p in probs:
        for h in p.get("history", []):
            entries.append((when(h), p, h))
    entries.sort(key=lambda e: e[0], reverse=True)
    out = ["# Session Journal — what tripped me, per attempt\n",
           "> Auto-generated from `review.json` history by `review.py gen`. "
           "Newest first (timestamped). Read this at the start of a session to target weak spots.\n",
           f"Total attempts logged: **{len(entries)}**.\n", "---\n"]
    for w, p, h in entries:
        key = p["file"] or f"LC{p['id']}"
        stamp = w.replace("T", " ") if "T" in w else w
        out.append(f"### {stamp} · LC{p['id']} {p['title']} · conf {h['conf']}/5  ({p['topic']}, {p['difficulty']})")
        out.append(f"`{key}`  ")
        out.append(f"{h['note'] or '_(no note)_'}\n")
    with open(JOURNAL, "w") as f:
        f.write("\n".join(out))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "due"
    argv = sys.argv[2:]
    {"build": lambda: build(), "due": lambda: due(argv), "log": lambda: log(argv),
     "gen": lambda: gen(), "journal": lambda: journal(),
     "stats": lambda: stats()}.get(cmd, lambda: sys.exit(__doc__))()


if __name__ == "__main__":
    main()
