class Solution:
    def maximumSwap(self, num: int) -> int:
        num_digits = list(map(int, str(num)))
        last = {digit: i for i, digit in enumerate(num_digits)}

        for i, digit in enumerate(num_digits):
            ##checking which max number is available later on starting from 9 to the digit
            ##if it's available, then make the swap and return 
            for d in range(9, digit, -1):
                if last.get(d, -1) > i:
                    num_digits[i], num_digits[last[d]] = num_digits[last[d]], num_digits[i]
                    return int(''.join(map(str, num_digits)))

        return num