from heapq import heappush, heappop
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Minimum number of rooms so no two overlapping meetings share a room.
        Equivalent to the peak number of meetings overlapping at any instant.

        Process meetings in start order; keep a min-heap of the END times of
        currently-busy rooms. For each meeting, if the earliest-freeing room is
        already done (rooms[0] <= start), reuse it (pop); always occupy a room
        (push this end). The heap size never shrinks, so its final size is the
        peak concurrency.

        Constraint 1 <= len(intervals) <= 1e4 guarantees non-empty, so no guard.

        Time  O(n log n) — sort + n heap ops of O(log n).
        Space O(n) — the heap.
        """
        intervals.sort(key=lambda x: x[0])
        rooms = [intervals[0][1]]              # min-heap of end times
        for start, end in intervals[1:]:
            if rooms[0] <= start:              # earliest-freeing room is free -> reuse
                heappop(rooms)
            heappush(rooms, end)
        return len(rooms)                      # size is non-decreasing -> peak concurrency

    def minMeetingRooms_sweep(self, intervals: List[List[int]]) -> int:
        """Alternate engine: split into +1 (start) / -1 (end) events, sort, and
        track the running max. Generalizes to 'concurrency at each timestamp'.
        On ties, process ends (-1) before starts (+1) so [a,b) and [b,c) share."""
        events = []
        for start, end in intervals:
            events.append((start, 1))
            events.append((end, -1))
        events.sort(key=lambda x: (x[0], x[1]))
        cur = peak = 0
        for _, delta in events:
            cur += delta
            peak = max(peak, cur)
        return peak


def test_min_meeting_rooms():
    s = Solution()
    for method in (s.minMeetingRooms, s.minMeetingRooms_sweep):
        assert method([[1, 2], [3, 4], [5, 6]]) == 1        # disjoint
        assert method([[0, 30], [5, 10], [15, 20]]) == 2    # one spans both
        assert method([[1, 5], [2, 6], [3, 7], [4, 8]]) == 4  # all overlap
        assert method([[1, 5], [5, 8]]) == 1                 # touch at 5, share
        assert method([[7, 10], [2, 4]]) == 1                # unsorted, disjoint
        assert method([[5, 8]]) == 1                         # single
    print("All test cases passed!")


test_min_meeting_rooms()

# Hints:
# 1. Sort by start so you process meetings chronologically.
# 2. Min-heap holds END times of busy rooms; rooms[0] is the soonest to free.
# 3. Reuse a room only when rooms[0] <= start; otherwise you need a new one.
# 4. Pop at most one per meeting (you place one meeting -> free at most one room).
# 5. Heap size never decreases, so len(rooms) at the end is the peak concurrency.
