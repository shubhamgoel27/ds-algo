from typing import List


class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        """
        Can a single person attend ALL meetings (i.e. no two overlap)?

        Sort by start; then any conflict must show up as an adjacent pair where
        the later meeting starts before the earlier one ends. So one linear scan
        comparing each start to the previous end suffices.

        Half-open [s, e): a meeting ending at t does not conflict with one
        starting at t, so the test is strict (`<`).
        Empty / single input trivially returns True (loop never runs).

        Time  O(n log n) — the sort dominates.
        Space O(1) beyond the sort.
        """
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:   # starts before prev ends -> conflict
                return False
        return True


def test_can_attend_meetings():
    s = Solution()
    assert s.canAttendMeetings([[0, 30], [5, 10], [15, 20]]) is False
    assert s.canAttendMeetings([[7, 10], [2, 4]]) is True      # unsorted, disjoint
    assert s.canAttendMeetings([[1, 5], [5, 8]]) is True       # touch at 5, half-open
    assert s.canAttendMeetings([[1, 10], [2, 3]]) is False     # nested overlap
    assert s.canAttendMeetings([[5, 8]]) is True               # single
    assert s.canAttendMeetings([]) is True                     # empty
    print("All test cases passed!")


test_can_attend_meetings()

# Hints:
# 1. Sort by start so conflicts become adjacent.
# 2. Compare each meeting's start to the PREVIOUS meeting's end.
# 3. Half-open intervals -> touching is fine -> strict `<`.
# 4. Min rooms variant (return a count instead of bool) = Meeting Rooms II (253).
