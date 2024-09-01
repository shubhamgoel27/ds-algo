from typing import List

class Solution:
    def simplifyPath(self, path: str) -> str:
        """
        Simplify a Unix-style file path.

        This function takes a string path and returns the simplified canonical path.
        
        Args:
            path (str): The path to simplify.

        Returns:
            str: The simplified canonical path.

        Examples:
            "/home/" -> "/home"
            "/../" -> "/"
            "/home//foo/" -> "/home/foo"
        """
        parts = path.split("/")
        final = []
        if len(parts)==1:
            return path
        for part in parts:
            if part == '.' or part == "":
                continue 
            if part == "..":
                if len(final)>0:
                    final.pop()
            else:
                final.append(part)
        final =  "/" + "/".join(final)
        return final

# Test cases
def test_simplifyPath():
    solution = Solution()
    
    assert solution.simplifyPath("/home/") == "/home"
    assert solution.simplifyPath("/../") == "/"
    assert solution.simplifyPath("/home//foo/") == "/home/foo"
    assert solution.simplifyPath("/a/./b/../../c/") == "/c"
    assert solution.simplifyPath("/a/../../b/../c//.//") == "/c"
    assert solution.simplifyPath("/a//b////c/d//././/..") == "/a/b/c"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_simplifyPath()