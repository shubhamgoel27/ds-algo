from collections import Counter


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """True if s2 contains a permutation (anagram) of s1 as a substring. O(n).

        Fixed-size sliding window of width len(s1). Keep ONE window counter alive
        and update it incrementally as the window slides (add the entering char,
        drop the leaving char), instead of rebuilding it each step (which would
        be O(len(s1) * len(s2))). The window matches when its counts == s1's.
        """
        if len(s1) > len(s2):
            return False

        need = Counter(s1)
        window = Counter(s2[:len(s1)])      # first window, built once
        if window == need:
            return True

        for right in range(len(s1), len(s2)):
            window[s2[right]] += 1                       # char entering on the right
            leaving = s2[right - len(s1)]                # char leaving on the left
            window[leaving] -= 1
            if window[leaving] == 0:
                del window[leaving]                      # drop zero counts, or Counter == breaks
            if window == need:
                return True
        return False


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        ("ab", "eidbaooo", True),
        ("ab", "eidboaoo", False),
        ("ab", "ba", True),            # match is the last window
        ("a", "a", True),              # single window
        ("abc", "bbbca", True),
        ("adc", "dcda", True),
        ("hello", "ooolleoooleh", False),
    ]
    for s1, s2, expected in test_cases:
        result = solution.checkInclusion(s1, s2)
        assert result == expected, f"checkInclusion({s1!r}, {s2!r}) = {result}, expected {expected}"
    print("All tests passed.")
