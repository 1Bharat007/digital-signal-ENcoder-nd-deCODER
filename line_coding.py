"""Basic digital line-coding encoders. All return two samples per bit."""


def _validate_bits(bits):
    if not bits or any(bit not in (0, 1) for bit in bits):
        raise ValueError("bits must be a non-empty sequence of 0s and 1s")


def nrz_l(bits):
    _validate_bits(bits)
    levels = [1 if bit == 0 else -1 for bit in bits]
    return [level for level in levels for _ in range(2)]


def nrz_i(bits):
    _validate_bits(bits)
    level = 1
    levels = []
    for bit in bits:
        if bit == 1:
            level *= -1
        levels.append(level)
    return [level for level in levels for _ in range(2)]


def manchester(bits):
    _validate_bits(bits)
    signal = []
    for bit in bits:
        signal.extend([-1, 1] if bit == 1 else [1, -1])
    return signal


def differential_manchester(bits):
    _validate_bits(bits)
    level = 1
    signal = []
    for bit in bits:
        if bit == 0:
            level *= -1  # transition at beginning means 0
        signal.append(level)
        level *= -1    # mandatory middle transition
        signal.append(level)
    return signal


def ami(bits):
    _validate_bits(bits)
    pulse = -1
    levels = []
    for bit in bits:
        if bit == 1:
            pulse *= -1
            levels.append(pulse)
        else:
            levels.append(0)
    return [level for level in levels for _ in range(2)]
