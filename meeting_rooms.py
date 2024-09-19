from heapq import heappush, heappop
from typing import List

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Determine the minimum number of meeting rooms required to schedule all meetings.

        Args:
            intervals (List[List[int]]): A list of meeting intervals, where each interval is [start_time, end_time].

        Returns:
            int: The minimum number of meeting rooms required.

        Time complexity: O(n log n), where n is the number of intervals.
        Space complexity: O(n) for the heap.
        """
        if not intervals:
            return 0

        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])

        # Initialize a min-heap to keep track of end times
        rooms = []
        heappush(rooms, intervals[0][1])

        for start, end in intervals[1:]:
            # If the earliest ending room is available, use it
            if start >= rooms[0]:
                heappop(rooms)
            # Add the current meeting's end time to the heap
            heappush(rooms, end)

        # The number of rooms in use is the size of the heap
        return len(rooms)

# Test cases
def test_min_meeting_rooms():
    solution = Solution()
    
    # Test case 1: No overlapping meetings
    assert solution.minMeetingRooms([[1, 2], [3, 4], [5, 6]]) == 1

    # Test case 2: Some overlapping meetings
    assert solution.minMeetingRooms([[0, 30], [5, 10], [15, 20]]) == 2

    # Test case 3: All meetings overlap
    assert solution.minMeetingRooms([[1, 5], [2, 6], [3, 7], [4, 8]]) == 4

    # Test case 4: Empty input
    assert solution.minMeetingRooms([]) == 0

    print("All test cases passed!")

# Run the test cases
test_min_meeting_rooms()

# Hints for solving this problem:
# 1. Sort the intervals by start time to process them in chronological order.
# 2. Use a min-heap to keep track of the earliest ending time of ongoing meetings.
# 3. For each new meeting, check if it can reuse a room (start time >= earliest end time).
# 4. The size of the heap at the end represents the minimum number of rooms needed.
# 5. Consider edge cases like empty input or non-overlapping meetings.
