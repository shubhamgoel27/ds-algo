from typing import List
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """Group anagrams together. O(n * k) time (n words, k = max length).

        Canonical-signature pattern: anagrams share an identical signature, so
        bucket words by that signature in a dict. Signature = a 26-length letter
        count tuple (hashable, O(k)); the sorted string also works but is O(k log k).
        """
        groups = defaultdict(list)
        for word in strs:
            sig = [0] * 26
            for ch in word:
                sig[ord(ch) - ord('a')] += 1
            groups[tuple(sig)].append(word)        # tuple is hashable -> dict key
        return list(groups.values())


if __name__ == "__main__":
    solution = Solution()

    def norm(groups):
        return sorted(sorted(g) for g in groups)

    assert norm(solution.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == \
        norm([["eat", "tea", "ate"], ["tan", "nat"], ["bat"]])
    assert norm(solution.groupAnagrams([""])) == [[""]]
    assert norm(solution.groupAnagrams(["a"])) == [["a"]]
    print("All tests passed.")
