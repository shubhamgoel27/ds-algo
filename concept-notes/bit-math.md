# Bit Manipulation & Math

## The engine in one sentence
These are the problems where brute force *works* but the right algebraic identity collapses it to one pass or to O(log n) — XOR cancels pairs, `n & (n-1)` strips a bit, and squaring halves an exponent. The trick isn't cleverness, it's knowing the identity.

## The one question that unlocks it
Don't reach for a hash set or a counter. Ask:
**"Is there an operation that makes the duplicates / paired structure *destroy itself*?"**
If every element appears twice except one, XOR them all — the pairs annihilate (`x^x=0`) and the loner survives. If you need to count or skip bits, ask what `n & (n-1)` or `n >> 1` does to the binary. The whole pattern is: *pick the operator whose own algebra does the bookkeeping for you.*

## The mental model
Three identities. Burn them in.

```
XOR                       BIT-STRIP                  HALVING
x ^ x = 0   (self-cancel) n & (n-1) clears lowest    x^n = (x^2)^(n/2)
x ^ 0 = x   (identity)    set bit of n               square the base,
commutative + associative                            halve the exponent
  ⇒ order doesn't matter  count of strips = popcount  ⇒ O(log n) not O(n)
  ⇒ pairs vanish anywhere
```

XOR is the star: because it's commutative and associative, you can fling all the numbers into one accumulator in *any* order and every matched pair zeroes out. Whatever's left unpaired is your answer. Bit-strip and halving are the "log n" levers — each step throws away half the work.

```visual
type: before-after
title: XOR pairs cancel, the single survives
shows: that XOR-ing a whole array where every value is doubled except one leaves exactly the unpaired value, regardless of order
elements: array [4,1,2,1,2]; show running accumulator left-to-right: 0^4=4, 4^1=5, 5^2=7, 7^1=6, 6^2=4; annotate that the two 1s and two 2s cancel pairwise (x^x=0) leaving 4; a second row reordering the array to [1,1,2,2,4] showing the same result 4 to prove order-independence
```

## The universal template
Each identity is a tiny skeleton. Pick the one the problem's structure asks for.

```python
# (1) XOR fold — "everything pairs up except the answer"
ans = 0                       # ← identity element (x^0 = x)
for x in nums:
    ans ^= x                  # ← pairs self-cancel; loner remains
return ans

# (2) Brian Kernighan — count set bits / strip lowest bit
count = 0
while n:
    n &= n - 1                # ← clears the LOWEST set bit each loop
    count += 1                # ← loops exactly popcount(n) times
return count

# (3) Fast exponentiation — square-and-multiply
def power(x, n):
    if n < 0:                 # ← handle negative exponent
        x, n = 1 / x, -n
    result = 1
    while n:
        if n & 1:             # ← bit set? fold current square into result
            result *= x
        x *= x                # ← square the base
        n >>= 1               # ← halve the exponent (drop the bit)
    return result
```

Decisions that vary: the **identity element** (XOR: 0), what you **fold in** at each step, and the **stopping condition** (n hits 0).

## Variants / when to use
| Identity | Operation | Fires when | LC |
|---|---|---|---|
| XOR self-cancel | `ans ^= x` over all elements | every element paired except one | 136 |
| XOR index⊕value | `ans ^= i ^ nums[i]` | one value missing from a known range | 268 |
| Gauss sum | `n*(n+1)//2 - sum(nums)` | missing number, prefer arithmetic | 268 |
| Brian Kernighan | `n &= n-1` until zero | count set bits / detect power-of-two | 191 |
| Bit DP | `bits[i] = bits[i>>1] + (i&1)` | popcount for *all* i in 0..n | 338 |
| Square & multiply | square base, `n >>= 1` | exponentiation in O(log n) | 50 |

## Worked example
**LC136 Single Number** — every number appears twice except one. XOR the whole array; pairs annihilate, the single survives.

```python
def singleNumber(nums):
    ans = 0
    for x in nums:
        ans ^= x          # x^x=0 kills pairs, x^0=x keeps the loner
    return ans
```

Trace on `[4,1,2,1,2]`, bit-level (4 bits). XOR is bitwise: a column ends `1` iff an odd number of `1`s appear in it.

```
        bits
  4  =  0 1 0 0
  1  =  0 0 0 1
  2  =  0 0 1 0
  1  =  0 0 0 1
  2  =  0 0 1 0
        -------  per-column XOR (parity of 1s in column)
 col3:  0,0,0,0,0 → 0
 col2:  1,0,0,0,0 → 1   (only the 4 contributes)
 col1:  0,0,1,0,1 → 0   (two 1s → even → cancel)
 col0:  0,1,0,1,0 → 0   (two 1s → even → cancel)
        -------
 ans =  0 1 0 0  = 4   ✓
```

The two 1s and two 2s each land an even number of `1`s in every column → wiped. Only 4's bits, appearing once, survive. You never counted occurrences — XOR's parity *is* the count mod 2.

## Gotchas
- **`n & (n-1)` is the lowest set bit, not the lowest bit.** It clears the rightmost `1` wherever it sits. Don't confuse it with `n & 1` (parity / LSB test).
- **Negative exponent in Pow.** `n` can be `-2^31`; computing `-n` on the raw int is fine in Python (arbitrary precision) but in fixed-width languages it overflows. Flip to `x = 1/x, n = -n` *before* looping. Also handle `n == 0 → 1`.
- **Missing Number XOR needs both ranges.** XOR all indices `0..n` *and* all values; the unpaired survivor is the gap. Off-by-one if you forget to include `n` itself as an index.
- **Counting Bits direction.** `bits[i] = bits[i>>1] + (i&1)` reads a *smaller, already-computed* index (`i>>1 < i`), so a single forward pass works. Don't try to fill it top-down.

## Python idioms
- `x.bit_count()` (3.10+) or `bin(x).count("1")` for popcount — but interviews usually want the Kernighan loop shown.
- `int.bit_length()` gives position of the highest set bit; `1 << k` builds a single-bit mask at position `k`.
- Python ints are **arbitrary precision** — no overflow, but also no automatic 32-bit wrap. For "treat as 32-bit" problems, mask with `& 0xFFFFFFFF`.
- Operators: `&` AND, `|` OR, `^` XOR, `~` NOT, `<<` left-shift (×2), `>>` right-shift (÷2 floor). Mask a bit: `n & (1 << k)`; set it: `n | (1 << k)`; clear lowest: `n & (n-1)`.
- `sum(range(n+1))` or `n*(n+1)//2` for the Gauss identity — integer `//` avoids float drift.

```visual
type: bar-steps
title: Fast exponentiation halves the exponent
shows: that computing x^13 takes ~log2(13)≈4 squaring steps, folding in the base only on set bits of the exponent
elements: exponent 13 = binary 1101; four rows for bits read low→high: bit0=1 (multiply result*=x, x→x^2), bit1=0 (skip, x→x^4), bit2=1 (multiply result*=x^4, x→x^8), bit3=1 (multiply result*=x^8); show result accumulating x^1 · x^4 · x^8 = x^13; label each row "square base, shift exponent right"
```

## Problem map
| LC | Problem | Df | How it instantiates the pattern |
|---|---|---|---|
| 136 | Single Number | E | XOR fold; identity 0; pairs self-cancel, loner remains |
| 191 | Number of 1 Bits | E | Kernighan: `n &= n-1` until 0, count loops = popcount |
| 268 | Missing Number | E | XOR all indices `0..n` ⊕ all values; survivor = gap (or Gauss `n(n+1)/2 - sum`) |
| 338 | Counting Bits | E | bit DP: `bits[i] = bits[i>>1] + (i&1)`, single forward pass, O(n) |
| 50 | Pow(x, n) | M | square-and-multiply; fold base on set bits, halve exponent → O(log n); handle `n<0` |
