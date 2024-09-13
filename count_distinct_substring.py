class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
        self.node_count = 0  # To count distinct nodes (distinct substrings)

    def insert(self, s:int) -> None:
        node = self.root
        for char in s:
            if char not in node.children:
                node.children[char] = TrieNode()
                self.node_count += 1  # Every new node represents a distinct substring
            node = node.children[char]
        node.is_end_of_word = True
class Solution:

    def countDistinct(self, s):
        trie = Trie()
        
        # Insert all suffixes into the trie
        for i in range(len(s)):
            suffix = s[i:]
            trie.insert(suffix)
        
        # The number of distinct substrings is the number of nodes in the trie
        return trie.node_count