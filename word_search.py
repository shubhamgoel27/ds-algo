from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """Does `word` exist as a path of adjacent cells (no cell reused)? Backtracking.
        O(m * n * 4^L) time, O(L) space (L = len(word)).

        Grow `path` (immutable string, so each branch owns its copy -- no path-undo).
        Pre-check the next letter `word[len(path)]` before recursing, which also acts
        as the visited check (a '#' cell never equals a needed letter). Restore the
        cell to `path[-1]` (its own letter) on the way back -- no board copy needed.
        """
        m, n = len(board), len(board[0])

        def backtrack(start, path):
            path += board[start[0]][start[1]]
            if path == word:
                return True
            board[start[0]][start[1]] = "#"                       # mark visited
            for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
                nx, ny = start[0] + dx, start[1] + dy
                if 0 <= nx < m and 0 <= ny < n and board[nx][ny] == word[len(path)]:
                    if backtrack((nx, ny), path):
                        return True
            board[start[0]][start[1]] = path[-1]                  # restore this cell's letter
            return False

        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0] and backtrack((i, j), ''):
                    return True
        return False

    def exist_index(self, board: List[List[str]], word: str) -> bool:
        """Equivalent, tracking an index instead of a path string (O(1) per step).
        Guard-clause DFS: each cell validates itself on entry."""
        m, n = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[i]:
                return False
            board[r][c] = "#"
            found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            board[r][c] = word[i]
            return found

        return any(dfs(i, j, 0) for i in range(m) for j in range(n))


if __name__ == "__main__":
    sol = Solution()
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    for w, exp in [("ABCCED", True), ("SEE", True), ("ABCB", False), ("Z", False), ("ABCESEEEFS", False)]:
        for method in (sol.exist, sol.exist_index):
            assert method([r[:] for r in board], w) == exp, f"{method.__name__} {w}"
    print("All tests passed.")
