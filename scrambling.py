from scrambling import b8zs, hdb3


def validate_bits(bits):
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Input must contain only 0s and 1s.")


def b8zs(bits):
    """B8ZS scrambling. Returns two voltage samples per bit."""
    validate_bits(bits)

    signal = []
    last_pulse = -1
    i = 0

    while i < len(bits):
        if bits[i:i + 8] == [0] * 8:
            p = last_pulse

            # 000VB0VB; V violates AMI, B follows AMI polarity.
            pattern = [0, 0, 0, p, -p, 0, -p, p]
            signal.extend(pattern)
            last_pulse = pattern[-1]
            i += 8

        else:
            if bits[i] == 1:
                last_pulse *= -1
                signal.append(last_pulse)
            else:
                signal.append(0)

            i += 1

    return [level for level in signal for _ in range(2)]


def hdb3(bits):
    """HDB3 scrambling. Returns two voltage samples per bit."""
    validate_bits(bits)

    signal = []
    last_pulse = -1
    marks_since_violation = 0
    i = 0

    while i < len(bits):
        if bits[i:i + 4] == [0] * 4:

            if marks_since_violation % 2 == 0:
                # B00V: B and V have the same polarity.
                b = -last_pulse
                signal.extend([b, 0, 0, b])
                last_pulse = b
            else:
                # 000V: V has the same polarity as the previous pulse.
                signal.extend([0, 0, 0, last_pulse])

            marks_since_violation = 0
            i += 4

        else:
            if bits[i] == 1:
                last_pulse *= -1
                signal.append(last_pulse)
                marks_since_violation += 1
            else:
                signal.append(0)

            i += 1

    return [level for level in signal for _ in range(2)]
