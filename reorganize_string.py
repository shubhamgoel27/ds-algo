from collections import Counter
import heapq

def reorganize_string(str):
    heap = []
    counter = Counter(str)

    for key, value in counter.items():
        heapq.heappush(heap, (-value,key))
    prev_val, prev_char = None, None 
    out = ''
    while len(heap)>0:
        val, char = heapq.heappop(heap)
        out+=char 
        if prev_char and prev_val <0:
          heapq.heappush(heap, (prev_val, prev_char))
        prev_val, prev_char = val + 1, char 
    return out if len(out) == len(str) else ''

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