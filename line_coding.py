import numpy as np
import matplotlib.pyplot as plt

# 0 = +1 V, 1 = -1 V
def nrz_l(bits):
    levels = [1 if bit == 0 else -1 for bit in bits]
    return np.repeat(levels, 2)


# 1 changes the level; 0 keeps it unchanged
def nrz_i(bits):
    level = 1
    levels = []

    for bit in bits:
        if bit == 1:
            level *= -1
        levels.append(level)

    return np.repeat(levels, 2)


# Every bit has a middle transition
# 0 = high-to-low; 1 = low-to-high
def manchester(bits):
    signal = []

    for bit in bits:
        signal.extend([-1, 1] if bit == 1 else [1, -1])

    return signal


# Always transition in the middle.
# Also transition at the start for bit 0.
def differential_manchester(bits):
    level = 1
    signal = []

    for bit in bits:
        if bit == 0:
            level *= -1

        signal.append(level)

        level *= -1
        signal.append(level)

    return signal


# 0 = zero voltage; 1 = alternating positive/negative
def ami(bits):
    pulse = -1
    levels = []

    for bit in bits:
        if bit == 1:
            pulse *= -1
            levels.append(pulse)
        else:
            levels.append(0)

    return np.repeat(levels, 2)


# Our test input
bits = [1, 0, 1, 1, 0, 0, 0, 0]

# A dictionary lets us add schemes without a huge if/else chain.
schemes = {
    "NRZ-L": nrz_l,
    "NRZ-I": nrz_i,
    "Manchester": manchester,
    "Differential Manchester": differential_manchester,
    "AMI": ami,
}

fig, axes = plt.subplots(5, 1, figsize=(12, 9), sharex=True)

for ax, (name, encoder) in zip(axes, schemes.items()):
    signal = encoder(bits)

    # Two samples per bit: one per half-bit interval.
    time = np.arange(len(signal) + 1) / 2
    values = np.append(signal, signal[-1])

    ax.step(time, values, where="post")
    ax.set_ylabel(name)
    ax.set_yticks([-1, 0, 1])
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(0, len(bits))
    ax.grid(axis="x", alpha=0.3)

axes[-1].set_xticks(range(len(bits) + 1))
axes[-1].set_xlabel("Time (bit intervals)")
fig.suptitle("Line Encoding: 10110000")
plt.tight_layout()
plt.show()