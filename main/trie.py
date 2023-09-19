
print("reading trie file")
import pickle

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.count = -1

class Trie:
    def __init__(self):
        self.root = TrieNode()
        # return self.root

    def insert(self, word_pair):
        word = word_pair[0]
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.count = word_pair[1]

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def autocomplete(self, prefix):
        results = []
        node = self.root

        # Traverse to the last node of the prefix
        for char in prefix: 
            if char not in node.children:
                return results
            node = node.children[char]

        # Perform a depth-first search to find all words with the given prefix
        self._find_words_with_prefix(node, prefix, results)
        return results

    def _find_words_with_prefix(self, node, current_prefix, results):
        if node.is_end_of_word:
            results.append([current_prefix, node.count])
        for char, child_node in node.children.items():
            self._find_words_with_prefix(child_node, current_prefix + char, results)

# # Example usage:
# trie = Trie()
# words = ["apple", "app", "banana", "bat", "ball"]
# for word in words:
#     trie.insert(word)

# print(trie.search("apple"))  # True
# print(trie.search("app"))    # True
# print(trie.search("ban"))    # False

# print(trie.autocomplete("ba"))  # ['banana', 'ball', 'bat']



