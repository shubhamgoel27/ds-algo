from collections import Counter
import heapq

def reorganize_string(s: str) -> str:
    """
    Reorganize the characters in the input string so that no two adjacent characters are the same.

    Description:
    This function uses a max-heap to greedily select the most frequent character
    that is different from the previously used character. It constructs the
    reorganized string character by character, always choosing the most frequent
    remaining character that is not the same as the last one used.

    Args:
    s (str): The input string to be reorganized.

    Returns:
    str: The reorganized string if possible, or an empty string if not possible.

    Hints:
    - Time complexity: O(n log k), where n is the length of the string and k is the number of unique characters.
    - Space complexity: O(k), where k is the number of unique characters.
    - The max-heap is simulated using a min-heap with negated frequencies.
    """
    heap = []
    counter = Counter(s)

    for char, freq in counter.items():
        heapq.heappush(heap, (-freq, char))
    
    prev_freq, prev_char = 0, ''
    result = []

    while heap:
        freq, char = heapq.heappop(heap)
        result.append(char)
        
        if prev_freq < 0:
            heapq.heappush(heap, (prev_freq, prev_char))
        
        prev_freq, prev_char = freq + 1, char

    return ''.join(result) if len(result) == len(s) else ''

def run_tests():
    test_cases = [
        {"input": "aabbcc", "expected": True},
        {"input": "aaab", "expected": False},
        {"input": "a", "expected": True},
        {"input": "abab", "expected": True},
        {"input": "aaaa", "expected": False},
        {"input": "aaabbccdde", "expected": True},
        {"input": "aaabbbcccddddeeeee", "expected": True},
        {"input": "", "expected": True},
        {"input": "aaabbb", "expected": True},
        {"input": "aabbccddeeffgg", "expected": True},
    ]

    for i, case in enumerate(test_cases):
        result = reorganize_string(case["input"])
        # Check if the result matches the expected outcome
        # For valid reorganizations, we check the length and character adjacency
        if case["expected"]:
            is_valid = len(result) == len(case["input"]) and all(result[i] != result[i+1] for i in range(len(result) - 1))
            if is_valid:
                print(f"Test case {i+1}: Passed")
            else:
                print(f"Test case {i+1}: Failed (expected valid reorganization, got '{result}')")
        else:
            if result == "":
                print(f"Test case {i+1}: Passed")
            else:
                print(f"Test case {i+1}: Failed (expected '', got '{result}')")

# Run the test cases
run_tests()