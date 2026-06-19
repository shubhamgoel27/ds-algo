from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """Does `word` exist as a path of adjacent cells (no cell reused)? Backtracking.
        O(m * n * 4^L) time, O(L) recursion (L = len(word)).

        State = an index `i` into the word: dfs(r, c, i) asks "can I match word[i:]
        from here?". Mark a cell '#' while it is on the current path, then restore it
        to word[i] (we only got past the guard if board[r][c] == word[i]) -- so no
        board copy is needed.
        """
        m, n = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[i]:
                return False
            board[r][c] = "#"                       # mark visited (shared mutable state)
            found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            board[r][c] = word[i]                   # un-mark: restore the original char
            return found

        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False

    def exist_pathstring(self, board: List[List[str]], word: str) -> bool:
        """Alternative: grow an immutable path string (copy-passed, so no path-undo).
        Only the BOARD (visited cells) is shared mutable state and needs mark/un-mark.
        """
        m, n = len(board), len(board[0])

        def backtrack(r, c, path):
            path = path + board[r][c]               # immutable: each branch gets its own
            if path == word:
                return True
            if not word.startswith(path):           # prune: path must stay a prefix
                return False
            ch = board[r][c]
            board[r][c] = "#"
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != "#":
                    if backtrack(nr, nc, path):
                        board[r][c] = ch
                        return True
            board[r][c] = ch
            return False

        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0] and backtrack(i, j, ""):
                    return True
        return False


if __name__ == "__main__":
    solution = Solution()
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    for w, exp in [("ABCCED", True), ("SEE", True), ("ABCB", False), ("Z", False), ("ABCESEEEFS", False)]:
        for method in (solution.exist, solution.exist_pathstring):
            assert method([r[:] for r in board], w) == exp, f"{method.__name__} {w}"
    print("All tests passed.")
