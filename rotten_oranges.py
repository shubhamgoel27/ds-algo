from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """Minutes until no fresh orange remains, or -1 if impossible. O(m*n).

        Multi-source BFS: seed the queue with every rotten orange so the rot
        spreads from all of them at once, one ring per minute. The level
        snapshot (len(q)) drains exactly one minute's worth of cells per pass.
        """
        m, n = len(grid), len(grid[0])

        # one pass: collect all sources, count fresh
        q = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j))
                elif grid[i][j] == 1:
                    fresh += 1

        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
        minutes = 0
        # one pass = one minute; the `fresh > 0` guard stops the counter the
        # instant the last orange rots, so minutes is never over-counted.
        while q and fresh > 0:
            minutes += 1
            for _ in range(len(q)):
                i, j = q.popleft()
                for di, dj in DIRS:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                        grid[ni][nj] = 2          # rot it, mark on enqueue
                        fresh -= 1
                        q.append((ni, nj))

        return minutes if fresh == 0 else -1


def test_oranges_rotting():
    sol = Solution()

    assert sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1   # unreachable
    assert sol.orangesRotting([[0, 2]]) == 0                              # no fresh
    assert sol.orangesRotting([[]]) == 0                                  # empty row
    assert sol.orangesRotting([[0]]) == 0                                 # only empty
    assert sol.orangesRotting([[1]]) == -1                                # lone fresh, no source

    print("All test cases passed!")


if __name__ == "__main__":
    test_oranges_rotting()
