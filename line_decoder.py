"""Decoders that recover bits from encoded voltage samples (not source bits)."""


def _check_signal(signal):
    signal = [int(value) for value in signal]
    if not signal or len(signal) % 2:
        raise ValueError("signal must contain two samples per bit")
    if any(value not in (-1, 0, 1) for value in signal):
        raise ValueError("voltage samples must be -1, 0, or +1")
    return signal


def _get_levels(signal):
    signal = _check_signal(signal)
    levels = []
    for i in range(0, len(signal), 2):
        if signal[i] != signal[i + 1]:
            raise ValueError("expected constant voltage during each bit interval")
        levels.append(signal[i])
    return levels


def decode_nrz_l(signal):
    return [0 if level == 1 else 1 for level in _get_levels(signal)]


def decode_nrz_i(signal):
    levels = _get_levels(signal)
    previous = 1
    bits = []
    for level in levels:
        bits.append(1 if level != previous else 0)
        previous = level
    return bits


def decode_manchester(signal):
    signal = _check_signal(signal)
    bits = []
    for i in range(0, len(signal), 2):
        pair = signal[i:i + 2]
        if pair == [-1, 1]:
            bits.append(1)
        elif pair == [1, -1]:
            bits.append(0)
        else:
            raise ValueError("invalid Manchester pair")
    return bits


def decode_differential_manchester(signal):
    signal = _check_signal(signal)
    previous = 1
    bits = []
    for i in range(0, len(signal), 2):
        first, second = signal[i:i + 2]
        if first == second:
            raise ValueError("missing mandatory middle transition")
        bits.append(0 if first != previous else 1)
        previous = second
    return bits


def decode_ami(signal):
    return [0 if level == 0 else 1 for level in _get_levels(signal)]


def decode_b8zs(signal):
    levels = _get_levels(signal)
    bits = []
    last_pulse = -1
    i = 0
    while i < len(levels):
        p = last_pulse
        replacement = [0, 0, 0, p, -p, 0, -p, p]
        if levels[i:i + 8] == replacement:
            bits.extend([0] * 8)
            last_pulse = replacement[-1]
            i += 8
        else:
            level = levels[i]
            bits.append(0 if level == 0 else 1)
            if level != 0:
                last_pulse = level
            i += 1
    return bits


def decode_hdb3(signal):
    levels = _get_levels(signal)
    bits = []
    last_pulse = -1
    i = 0
    while i < len(levels):
        current = levels[i:i + 4]
        # 000V: V repeats the previous non-zero pulse polarity.
        if len(current) == 4 and current == [0, 0, 0, last_pulse]:
            bits.extend([0] * 4)
            i += 4
        # B00V: B is opposite the previous pulse and V repeats B.
        elif (len(current) == 4 and current[0] == -last_pulse
              and current[1:] == [0, 0, current[0]]):
            last_pulse = current[0]
            bits.extend([0] * 4)
            i += 4
        else:
            level = levels[i]
            bits.append(0 if level == 0 else 1)
            if level != 0:
                last_pulse = level
            i += 1
    return bits
