import random


def generate_random_bits(length: int) -> list[int]:
    """Generate a random sequence of 0s and 1s."""
    return [random.randint(0, 1) for _ in range(length)]


def generate_bits_with_zero_run(
    length: int, run_length: int = 8
) -> list[int]:
    """Generate bits with 4 or 8 consecutive zeros."""

    if length < run_length:
        raise ValueError("Length must be at least run_length.")

    if run_length not in (4, 8):
        raise ValueError("run_length must be 4 or 8.")

    bits = generate_random_bits(length)

    # Choose a random starting position for the zero sequence.
    start = random.randrange(length - run_length + 1)

    bits[start:start + run_length] = [0] * run_length

    return bits


def longest_palindrome(bits: list[int]) -> list[int]:
    """Find the longest contiguous palindromic substring in O(n)."""

    original = "".join(map(str, bits))

    # Add separators to handle even and odd length palindromes uniformly.
    transformed = "^#" + "#".join(original) + "#$"

    radius = [0] * len(transformed)
    center = right = 0

    for i in range(1, len(transformed) - 1):
        mirror = 2 * center - i

        if i < right:
            radius[i] = min(right - i, radius[mirror])

        while (
            transformed[i + 1 + radius[i]]
            == transformed[i - 1 - radius[i]]
        ):
            radius[i] += 1

        if i + radius[i] > right:
            center = i
            right = i + radius[i]

    max_length = max(radius)
    center_index = radius.index(max_length)

    start = (center_index - max_length) // 2
    result = original[start:start + max_length]

    return [int(bit) for bit in result]


if __name__ == "__main__":
    bits = generate_bits_with_zero_run(24, 8)

    print("Generated bits:       ", bits)
    print("Longest palindrome:   ", longest_palindrome(bits))