from collections import defaultdict


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """Longest substring that becomes uniform after <= k replacements. O(n).

        Sliding window. A window is valid iff the replacements needed to make it
        one letter, which is (window_length - max frequency in window), is <= k.
        Compute that directly each step rather than maintaining a fragile counter.
        max(d.values()) is O(26) since there are only 26 letters, so still O(n).
        """
        d = defaultdict(int)
        longest = 0
        left = 0
        for right in range(len(s)):
            d[s[right]] += 1                                    # expand
            while (right - left + 1) - max(d.values()) > k:    # shrink while invalid
                d[s[left]] -= 1
                left += 1
            longest = max(longest, right - left + 1)           # record (window now valid)
        return longest

    def characterReplacement_optimized(self, s: str, k: int) -> int:
        """Strictly O(n): keep a running max_freq that is never decreased.

        This looks wrong (max_freq can go stale after shrinking) but is correct:
        we only want the LONGEST window, and a stale-high max_freq only loosens
        the shrink test, so the window never drops below the best valid size and
        `longest` can never exceed a genuinely-valid window. Drops the per-step
        max() call. Worth knowing for the "make it strictly O(n)" follow-up.
        """
        d = defaultdict(int)
        longest = 0
        left = 0
        max_freq = 0
        for right in range(len(s)):
            d[s[right]] += 1
            max_freq = max(max_freq, d[s[right]])
            while (right - left + 1) - max_freq > k:
                d[s[left]] -= 1
                left += 1
            longest = max(longest, right - left + 1)
        return longest


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ("ABAB", 2, 4),
        ("AABABBA", 1, 4),
        ("AAAA", 0, 4),
        ("ABCDE", 1, 2),
        ("AAAB", 0, 3),
        ("", 0, 0),
    ]
    for s, k, expected in test_cases:
        assert solution.characterReplacement(s, k) == expected, f"clear: {s!r}, {k}"
        assert solution.characterReplacement_optimized(s, k) == expected, f"optimized: {s!r}, {k}"
    print("All tests passed.")
