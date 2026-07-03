"""
Task Scheduler (LeetCode 621) + the bank/agents generalization
==============================================================

Pattern: "ready set + waiting set." When choosing an item benches it for a
while and it returns later, one heap is not enough. Split into:
  - a READY set ordered by PRIORITY   (what to pick now)   -> heap
  - a WAITING set ordered by WAKE-TIME (what returns, when) -> deque or heap

leastInterval: equal cooldowns -> tasks wake in insertion order -> WAITING is a
plain FIFO deque. bank_service_time: unequal durations -> WAITING must be a heap
keyed by finish-time. Same skeleton, the waiting side just upgrades.
"""
from collections import Counter, deque
import heapq
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """Min intervals to run all tasks with cooldown n between same task.
        Heap simulation: each tick, run the most-frequent READY task; benched
        tasks wait in a FIFO queue until their cooldown expires.

        Time  O(T) ticks, each O(log K) heap work (K distinct tasks <= 26).
        Space O(K).
        """
        heap = [-c for c in Counter(tasks).values()]   # max-heap via negation
        heapq.heapify(heap)
        q = deque()                                    # (neg_count, ready_time)
        sec = 0
        while heap or q:                               # stop only when BOTH empty
            sec += 1
            if q and q[0][1] == sec:                   # front task finished cooling
                heapq.heappush(heap, q.popleft()[0])
            if heap:
                cnt = heapq.heappop(heap) + 1          # negative -> +1 "uses one unit"
                if cnt != 0:                           # work left -> send to cooldown
                    q.append((cnt, sec + n + 1))
            # else: heap empty but q not -> this tick is an idle
        return sec

    def leastInterval_formula(self, tasks: List[str], n: int) -> int:
        """O(T) greedy math: the most frequent task forces (m-1) gaps of (n+1);
        ties widen the tail by k; enough filler tasks erase idles -> len(tasks)."""
        c = Counter(tasks)
        m = max(c.values())
        k = sum(1 for v in c.values() if v == m)
        return max((m - 1) * (n + 1) + k, len(tasks))


def bank_service_time(num_customers: int, service_times: List[int],
                      num_agents: int) -> int:
    """The reported Pinterest question. Customers served FIFO; a waiting customer
    takes the lowest-id agent that is free. Return when the last one finishes.
    WAITING set is a heap (agents finish at different times) keyed by free-time."""
    if num_agents <= 0 or num_customers <= 0:
        return 0
    free = list(range(num_agents))                     # min-heap of idle agent ids
    heapq.heapify(free)
    busy = []                                          # (free_time, agent_id)
    now = finish = 0
    for i in range(num_customers):
        if not free:                                   # fast-forward to next free agent
            now = busy[0][0]
            while busy and busy[0][0] == now:
                heapq.heappush(free, heapq.heappop(busy)[1])
        aid = heapq.heappop(free)                      # lowest-numbered free agent
        done = now + service_times[i]
        finish = max(finish, done)
        heapq.heappush(busy, (done, aid))
    return finish


def run_tests():
    s = Solution()
    for method in (s.leastInterval, s.leastInterval_formula):
        assert method(["A","A","A","B","B","B"], 2) == 8
        assert method(["A","A","A","B","B","B"], 0) == 6
        assert method(["A","A","A","A","B","C","D"], 2) == 10
        assert method(["A"], 2) == 1
        assert method(["A","B","C"], 2) == 3
        assert method(["A","A","A","A","A","A","B","C","D","E","F","G"], 2) == 16

    assert bank_service_time(0, [], 3) == 0
    assert bank_service_time(3, [4, 1, 2], 1) == 7
    assert bank_service_time(3, [4, 1, 2], 2) == 4
    assert bank_service_time(2, [5, 3], 5) == 5
    assert bank_service_time(3, [2, 2, 2], 2) == 4
    print("All test cases passed!")


run_tests()

# Hints:
# 1. Two containers: max-heap of ready counts, deque of resting (count, ready_time).
# 2. Loop while heap OR queue (stop only when BOTH empty) -- classic and/or flip.
# 3. Each tick: wake the front of the queue if ready, then run the heap top.
# 4. Negated counts -> "use one" is += 1; requeue with ready_time = sec + n + 1.
# 5. Bank/agents = same skeleton but the waiting set is a HEAP (unequal durations).
