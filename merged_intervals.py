class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals)<=1:
            return intervals
        intervals.sort(key=lambda x: x[0])
        merged_intervals = [intervals[0]]

        for i in range(1, len(intervals)):
            curr_start, curr_end = intervals[i]
            prev_start, prev_end = merged_intervals[-1]
            if prev_end >= curr_start:
                merged_intervals[-1] = [prev_start, max(prev_end, curr_end)]
            else:
                merged_intervals.append([curr_start, curr_end])

        return merged_intervals
