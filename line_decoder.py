def check_signal(signal):
    """Validate the encoded voltage samples."""
    signal = list(signal)

    if len(signal) == 0 or len(signal) % 2 != 0:
        raise ValueError("Signal must contain two samples per bit.")

    if any(level not in (-1, 0, 1) for level in signal):
        raise ValueError("Signal levels must be -1, 0, or +1.")

    return signal


def get_bit_levels(signal):
    """Extract the repeated voltage level for each bit."""
    signal = check_signal(signal)

    for i in range(0, len(signal), 2):
        if signal[i] != signal[i + 1]:
            raise ValueError("Expected a constant voltage within each bit.")

    return signal[::2]


def decode_nrz_l(signal):
    levels = get_bit_levels(signal)
    return [0 if level == 1 else 1 for level in levels]


def decode_nrz_i(signal):
    levels = get_bit_levels(signal)
    previous = 1
    bits = []

    for level in levels:
        bits.append(1 if level != previous else 0)
        previous = level

    return bits


def decode_manchester(signal):
    signal = check_signal(signal)
    bits = []

    for i in range(0, len(signal), 2):
        pair = signal[i:i + 2]

        if pair == [-1, 1]:
            bits.append(1)
        elif pair == [1, -1]:
            bits.append(0)
        else:
            raise ValueError("Invalid Manchester waveform.")

    return bits


def decode_differential_manchester(signal):
    signal = check_signal(signal)
    previous = 1
    bits = []

    for i in range(0, len(signal), 2):
        first, second = signal[i:i + 2]

        if first == second:
            raise ValueError("Missing middle transition.")

        # A transition at the beginning means bit 0.
        bits.append(0 if first != previous else 1)
        previous = second

    return bits


def decode_ami(signal):
    levels = get_bit_levels(signal)

    # AMI represents 0 with zero voltage and 1 with a nonzero pulse.
    return [0 if level == 0 else 1 for level in levels]


def decode_b8zs(signal):
    levels = get_bit_levels(signal)
    bits = []
    last_pulse = -1
    i = 0

    while i < len(levels):
        p = last_pulse
        pattern = [0, 0, 0, p, -p, 0, -p, p]

        if levels[i:i + 8] == pattern:
            bits.extend([0] * 8)
            i += 8
            # The last pulse of this pattern has polarity p.
            last_pulse = p
        else:
            level = levels[i]
            bits.append(0 if level == 0 else 1)

            if level != 0:
                last_pulse = level

            i += 1

    return bits


def decode_hdb3(signal):
    levels = get_bit_levels(signal)
    bits = []
    last_pulse = -1
    i = 0

    while i < len(levels):
        # 000V: V has the same polarity as the previous pulse.
        if levels[i:i + 4] == [0, 0, 0, last_pulse]:
            bits.extend([0] * 4)
            i += 4

        # B00V: B is a normal AMI pulse; V repeats its polarity.
        elif (
            i + 3 < len(levels)
            and levels[i] != 0
            and levels[i + 1:i + 3] == [0, 0]
            and levels[i + 3] == levels[i]
            and levels[i] == -last_pulse
        ):
            last_pulse = levels[i]
            bits.extend([0] * 4)
            i += 4

        else:
            level = levels[i]
            bits.append(0 if level == 0 else 1)

            if level != 0:
                last_pulse = level

            i += 1

    return bits