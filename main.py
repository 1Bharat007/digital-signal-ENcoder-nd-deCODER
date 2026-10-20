import numpy as np
import matplotlib.pyplot as plt

from line_coding import nrz_l

from data_generator import (
    generate_random_bits,
    generate_bits_with_zero_run,
    longest_palindrome,
)

from line_coding import (
    nrz_l,
    nrz_i,
    manchester,
    differential_manchester,
    ami,
)


# Map menu choices to encoder functions.
schemes = {
    "1": ("NRZ-L", nrz_l),
    "2": ("NRZ-I", nrz_i),
    "3": ("Manchester", manchester),
    "4": ("Differential Manchester", differential_manchester),
    "5": ("AMI", ami),
}


# 1. Generate digital input
length = int(input("Enter the number of bits to generate: "))

if length < 1:
    raise SystemExit("Bit length must be positive.")

print("\n1. Completely random bits")
print("2. Bits containing consecutive zeros")

generation_choice = input("Choose input type: ")

if generation_choice == "1":
    bits = generate_random_bits(length)

elif generation_choice == "2":
    run_length = int(input("Enter zero-run length (4 or 8): "))
    bits = generate_bits_with_zero_run(length, run_length)

else:
    raise SystemExit("Invalid input choice.")


# 2. Display generated bits and longest palindrome
print("\nDigital input:     ", "".join(map(str, bits)))
print("Longest palindrome:", "".join(map(str, longest_palindrome(bits))))


# 3. Select line-coding scheme
print("\nChoose line-coding scheme:")

for key, (name, _) in schemes.items():
    print(f"{key}. {name}")

choice = input("Enter your choice: ")

if choice not in schemes:
    raise SystemExit("Invalid scheme choice.")

scheme_name, encoder = schemes[choice]


# 4. Encode the bits
signal = np.asarray(encoder(bits), dtype=int)

print("\nSelected scheme:", scheme_name)
print("Encoded voltage levels:", signal.tolist())


# 5. Plot the encoded waveform
time = np.arange(len(signal) + 1) / 2
values = np.append(signal, signal[-1])

plt.figure(figsize=(12, 4))
plt.step(time, values, where="post")
plt.title(f"{scheme_name} Encoding")
plt.xlabel("Time (bit intervals)")
plt.ylabel("Voltage level")
plt.yticks([-1, 0, 1], ["-1 V", "0 V", "+1 V"])
plt.xticks(range(len(bits) + 1))
plt.xlim(0, len(bits))
plt.ylim(-1.5, 1.5)
plt.grid(axis="both", alpha=0.3)
plt.tight_layout()
plt.show()
