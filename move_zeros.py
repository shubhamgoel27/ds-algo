def move_zeros_to_left(A):
    if len(A) <= 1:
        return A
    
    n = len(A)
    i = n - 2
    j = n - 1
    
    while i >= 0 and j >= 0:
        if A[j] == 0:
            if A[i] != 0:
                A[i], A[j] = A[j], A[i]
            else:
                j += 1
        
        j -= 1
        i -= 1
    return A

# Test cases
test_cases = [
    ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ([0, 1, 0, 2, 0, 3, 0, 4, 0, 5], [0, 0, 0, 0, 0, 1, 2, 3, 4, 5]),
    ([1, 2, 3, 0, 0, 0], [0, 0, 0, 1, 2, 3]),
    ([0, 0, 0, 1, 2, 3], [0, 0, 0, 1, 2, 3]),
    ([0], [0]),
    ([1], [1])
]

# Testing function
for idx, (input_list, expected_output) in enumerate(test_cases):
    result = move_zeros_to_left(input_list.copy())
    assert result == expected_output, f"Test case {idx + 1} failed: expected {expected_output}, got {result}"

print("All test cases passed!")

