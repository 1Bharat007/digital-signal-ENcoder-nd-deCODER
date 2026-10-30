"""Simple PCM and Delta Modulation encoders and decoders."""
import math


def _validate_samples(samples):
    values = [float(value) for value in samples]
    if not values:
        raise ValueError("enter at least one analog sample")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("analog samples must be finite numbers")
    return values


def pcm_encode(samples, bits_per_sample=3):
    """Uniform PCM quantizer. Returns (serialized_bits, metadata)."""
    values = _validate_samples(samples)
    if not 1 <= bits_per_sample <= 16:
        raise ValueError("bits_per_sample must be between 1 and 16")

    vmin, vmax = min(values), max(values)
    if vmin == vmax:
        padding = max(abs(vmin) * 0.05, 0.5)
        vmin -= padding
        vmax += padding

    levels = 2 ** bits_per_sample
    step = (vmax - vmin) / levels
    encoded_bits = []
    for value in values:
        index = int((value - vmin) / step)
        index = max(0, min(levels - 1, index))
        encoded_bits.extend(int(bit) for bit in format(index, f"0{bits_per_sample}b"))

    metadata = {
        "bits_per_sample": bits_per_sample,
        "vmin": vmin,
        "vmax": vmax,
        "step": step,
    }
    return encoded_bits, metadata


def pcm_decode(bits, bits_per_sample, vmin, vmax):
    """Decode PCM bits to midpoint reconstruction levels."""
    if not bits or any(bit not in (0, 1) for bit in bits):
        raise ValueError("PCM input must be a non-empty bit sequence")
    if len(bits) % bits_per_sample:
        raise ValueError("PCM bitstream length must be divisible by bits_per_sample")
    levels = 2 ** bits_per_sample
    step = (vmax - vmin) / levels
    reconstructed = []
    for start in range(0, len(bits), bits_per_sample):
        index = int("".join(map(str, bits[start:start + bits_per_sample])), 2)
        reconstructed.append(vmin + (index + 0.5) * step)
    return reconstructed


def delta_encode(samples, step_size=0.25, initial_value=0.0):
    """One-bit delta encoder: 1 steps up, 0 steps down."""
    values = _validate_samples(samples)
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    estimate = float(initial_value)
    bits = []
    for value in values:
        if value >= estimate:
            bits.append(1)
            estimate += step_size
        else:
            bits.append(0)
            estimate -= step_size
    return bits


def delta_decode(bits, step_size=0.25, initial_value=0.0):
    """Reconstruct the staircase by accumulating +/- step_size."""
    if not bits or any(bit not in (0, 1) for bit in bits):
        raise ValueError("Delta input must be a non-empty bit sequence")
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    estimate = float(initial_value)
    reconstructed = []
    for bit in bits:
        estimate += step_size if bit == 1 else -step_size
        reconstructed.append(estimate)
    return reconstructed
