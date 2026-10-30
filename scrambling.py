"""AMI-based B8ZS and HDB3 scramblers. Outputs two samples per bit."""


def _validate_bits(bits):
    if not bits or any(bit not in (0, 1) for bit in bits):
        raise ValueError("bits must be a non-empty sequence of 0s and 1s")


def _expand(levels):
    return [level for level in levels for _ in range(2)]


def b8zs(bits):
    """Replace each run of eight zeros with 000VB0VB."""
    _validate_bits(bits)
    levels = []
    last_pulse = -1  # same initialization as the project's AMI encoder
    i = 0
    while i < len(bits):
        if bits[i:i + 8] == [0] * 8:
            p = last_pulse
            replacement = [0, 0, 0, p, -p, 0, -p, p]
            levels.extend(replacement)
            last_pulse = replacement[-1]
            i += 8
        else:
            if bits[i] == 1:
                last_pulse *= -1
                levels.append(last_pulse)
            else:
                levels.append(0)
            i += 1
    return _expand(levels)


def hdb3(bits):
    """Replace each run of four zeros with 000V or B00V."""
    _validate_bits(bits)
    levels = []
    last_pulse = -1
    marks_since_violation = 0
    i = 0
    while i < len(bits):
        if bits[i:i + 4] == [0] * 4:
            if marks_since_violation % 2 == 0:
                # B00V: B is the next normal AMI polarity; V repeats B.
                b = -last_pulse
                levels.extend([b, 0, 0, b])
                last_pulse = b
            else:
                # 000V: V has the same polarity as the preceding pulse.
                levels.extend([0, 0, 0, last_pulse])
            marks_since_violation = 0
            i += 4
        else:
            if bits[i] == 1:
                last_pulse *= -1
                levels.append(last_pulse)
                marks_since_violation += 1
            else:
                levels.append(0)
            i += 1
    return _expand(levels)
