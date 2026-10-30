"""Digital bit-stream generation and longest palindromic substring."""
import random


def generate_random_bits(length: int) -> list[int]:
    if length < 1:
        raise ValueError("length must be at least 1")
    return [random.randint(0, 1) for _ in range(length)]


def generate_bits_with_zero_run(length: int, run_length: int = 8) -> list[int]:
    if run_length not in (4, 8):
        raise ValueError("run_length must be 4 or 8")
    if length < run_length:
        raise ValueError("length must be at least run_length")
    bits = generate_random_bits(length)
    start = random.randrange(length - run_length + 1)
    bits[start:start + run_length] = [0] * run_length
    return bits


def longest_palindrome(bits: list[int]) -> list[int]:
    """Manacher's algorithm: O(n) time and O(n) extra space."""
    if not bits:
        return []
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("bits must contain only 0 and 1")

    original = "".join(map(str, bits))
    transformed = "^#" + "#".join(original) + "#$"
    radius = [0] * len(transformed)
    center = right = 0

    for i in range(1, len(transformed) - 1):
        mirror = 2 * center - i
        if i < right:
            radius[i] = min(right - i, radius[mirror])
        while transformed[i + 1 + radius[i]] == transformed[i - 1 - radius[i]]:
            radius[i] += 1
        if i + radius[i] > right:
            center, right = i, i + radius[i]

    longest_length = max(radius)
    center_index = radius.index(longest_length)
    start = (center_index - longest_length) // 2
    return [int(ch) for ch in original[start:start + longest_length]]
