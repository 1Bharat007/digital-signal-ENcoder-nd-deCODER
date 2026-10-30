# Project Specification: Digital Signal Encoder and Decoder

**Course:** ITT 036 — Programming Assignment 1  
**Language:** Python 3  
**Libraries:** NumPy and Matplotlib

## Description
The program generates digital bit streams or accepts sampled analog values. For digital input, it can generate random bits or insert a run of four/eight consecutive zeros. It also reports the longest contiguous palindromic substring using Manacher's algorithm. The bit stream can be encoded using NRZ-L, NRZ-I, Manchester, Differential Manchester or AMI. AMI can optionally use B8ZS or HDB3 scrambling. The program plots the encoded voltage waveform and can decode the waveform to recover the digital bits.

For analog input, the user enters a comma-separated sequence of sample amplitudes and selects either Pulse Code Modulation (PCM) or Delta Modulation (DM). The program converts the samples into bits, decodes those bits into reconstructed amplitude samples, and plots the staircase reconstruction. The resulting bits can also pass through a selected line-coding scheme.

## Assumptions
Voltage levels are normalized to -1, 0 and +1. Two samples represent each bit interval. NRZ-L maps 0 to +1 and 1 to -1. NRZ-I starts at +1; a 1 causes a transition. Manchester maps 0 to high-to-low and 1 to low-to-high. Differential Manchester starts at +1, uses a start transition for 0, and always has a middle transition. AMI maps 0 to zero voltage and alternates the polarity of successive 1s. PCM uses uniform mid-rise quantization over the entered sample range. Delta Modulation uses a fixed user-selected step size and an initial reconstructed value of zero. Noise and physical-channel effects are not modeled.

## How to run
Install dependencies using `python -m pip install -r requirements.txt`, then run `python main.py`. Follow the terminal prompts to choose digital or analog input, encoding method and optional decoding.

## References and acknowledgement
Add the exact textbook, lecture notes, websites or other sources consulted. Acknowledge AI assistance and discussions in accordance with the assignment instructions.
