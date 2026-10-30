"""Interactive digital line coding + analog PCM/DM demonstration."""
import numpy as np
import matplotlib.pyplot as plt

from data_generator import generate_random_bits, generate_bits_with_zero_run, longest_palindrome
from line_coding import nrz_l, nrz_i, manchester, differential_manchester, ami
from scrambling import b8zs, hdb3
from line_decoder import (
    decode_nrz_l, decode_nrz_i, decode_manchester,
    decode_differential_manchester, decode_ami, decode_b8zs, decode_hdb3,
)
from analog_modulation import pcm_encode, pcm_decode, delta_encode, delta_decode


ENCODERS = {
    "1": ("NRZ-L", nrz_l, decode_nrz_l),
    "2": ("NRZ-I", nrz_i, decode_nrz_i),
    "3": ("Manchester", manchester, decode_manchester),
    "4": ("Differential Manchester", differential_manchester, decode_differential_manchester),
    "5": ("AMI", ami, decode_ami),
}


def show_analog_reconstruction(original, reconstructed, title):
    x = np.arange(len(original))
    plt.figure(figsize=(10, 4))
    plt.plot(x, original, marker="o", label="Input analog samples")
    plt.step(x, reconstructed, where="mid", label="Decoded staircase")
    plt.title(title)
    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def show_line_signal(signal, bit_count, title):
    signal = np.asarray(signal, dtype=int)
    time = np.arange(len(signal) + 1) / 2
    values = np.append(signal, signal[-1])
    plt.figure(figsize=(12, 4))
    plt.step(time, values, where="post")
    plt.title(title)
    plt.xlabel("Time (bit intervals)")
    plt.ylabel("Voltage")
    plt.yticks([-1, 0, 1], ["-1 V", "0 V", "+1 V"])
    plt.xticks(range(bit_count + 1))
    plt.xlim(0, bit_count)
    plt.ylim(-1.5, 1.5)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    print("=== DIGITAL SIGNAL ENCODER AND DECODER ===")
    print("1. Digital input (generate bits)")
    print("2. Analog input (PCM or Delta Modulation)")
    input_type = input("Choose input type: ").strip()

    analog_mode = False
    analog_method = None
    analog_metadata = None
    analog_step = None
    analog_initial = 0.0
    original_analog = None

    if input_type == "1":
        length = int(input("Enter number of bits: "))
        print("1. Completely random bits")
        print("2. Include a run of consecutive zeros")
        generation_choice = input("Choose generation type: ").strip()
        if generation_choice == "1":
            bits = generate_random_bits(length)
        elif generation_choice == "2":
            run_length = int(input("Choose zero-run length (4 or 8): "))
            bits = generate_bits_with_zero_run(length, run_length)
        else:
            raise ValueError("Invalid generation choice")

    elif input_type == "2":
        analog_mode = True
        raw = input("Enter analog sample values separated by commas (e.g. 0,0.5,1,0.5,0,-0.5): ")
        original_analog = [float(value.strip()) for value in raw.split(",") if value.strip()]
        print("1. PCM")
        print("2. Delta Modulation")
        analog_choice = input("Choose analog conversion: ").strip()

        if analog_choice == "1":
            analog_method = "PCM"
            bit_depth = int(input("Enter bits per sample (e.g. 3 or 4): "))
            bits, analog_metadata = pcm_encode(original_analog, bit_depth)
            analog_step = analog_metadata["step"]
            reconstructed = pcm_decode(
                bits, analog_metadata["bits_per_sample"],
                analog_metadata["vmin"], analog_metadata["vmax"]
            )
        elif analog_choice == "2":
            analog_method = "Delta Modulation"
            analog_step = float(input("Enter delta step size (e.g. 0.25): "))
            bits = delta_encode(original_analog, analog_step, analog_initial)
            reconstructed = delta_decode(bits, analog_step, analog_initial)
        else:
            raise ValueError("Invalid analog conversion choice")

        print(f"{analog_method} generated digital bits:", "".join(map(str, bits)))
        show_analog_reconstruction(original_analog, reconstructed, f"{analog_method} decoded staircase")

    else:
        raise ValueError("Choose 1 or 2")

    print("\nDigital bitstream:", "".join(map(str, bits)))
    print("Longest palindrome:", "".join(map(str, longest_palindrome(bits))))

    print("\nChoose line-coding scheme:")
    for key, (name, _, _) in ENCODERS.items():
        print(f"{key}. {name}")
    choice = input("Enter scheme choice: ").strip()
    if choice not in ENCODERS:
        raise ValueError("Invalid line-coding choice")

    scheme_name, encoder, decoder = ENCODERS[choice]
    if choice == "5":
        scramble = input("Apply B8ZS/HDB3 scrambling? (y/n): ").strip().lower()
        if scramble == "y":
            print("1. B8ZS\n2. HDB3")
            scramble_choice = input("Choose scrambling: ").strip()
            if scramble_choice == "1":
                scheme_name, encoder, decoder = "AMI + B8ZS", b8zs, decode_b8zs
            elif scramble_choice == "2":
                scheme_name, encoder, decoder = "AMI + HDB3", hdb3, decode_hdb3
            else:
                raise ValueError("Invalid scrambling choice")

    signal = encoder(bits)
    print("\nSelected scheme:", scheme_name)
    print("Encoded voltage samples:", signal)
    show_line_signal(signal, len(bits), f"{scheme_name} encoded waveform")

    answer = input("Decode the received waveform? (y/n): ").strip().lower()
    if answer == "y":
        recovered_bits = decoder(signal)
        print("Decoded bitstream:", "".join(map(str, recovered_bits)))
        print("Original matches decoded:", recovered_bits == bits)

        if analog_mode and recovered_bits == bits:
            if analog_method == "PCM":
                final_reconstruction = pcm_decode(
                    recovered_bits,
                    analog_metadata["bits_per_sample"],
                    analog_metadata["vmin"],
                    analog_metadata["vmax"],
                )
            else:
                final_reconstruction = delta_decode(recovered_bits, analog_step, analog_initial)
            show_analog_reconstruction(
                original_analog, final_reconstruction,
                f"{analog_method} staircase after line decoding"
            )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError) as error:
        print("\nInput error:", error)
