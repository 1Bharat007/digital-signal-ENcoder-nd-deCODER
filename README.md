# Digital Signal Encoder and Decoder

Python implementation of digital data generation, line coding, AMI scrambling, line decoding, PCM and Delta Modulation.

## Requirements

- Python 3.10 or newer
- NumPy
- Matplotlib

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python main.py
```

## Implemented features

- Random binary data generation and forced runs of four/eight zeros
- Longest contiguous binary palindrome using Manacher's algorithm
- NRZ-L, NRZ-I, Manchester, Differential Manchester and AMI encoding
- B8ZS and HDB3 scrambling of AMI
- Waveform-based decoders for all implemented line codes
- Uniform PCM encoder/decoder
- One-bit Delta Modulation encoder/decoder
- Matplotlib waveform and analog staircase plots

## Signal conventions and assumptions

- Voltage levels are normalized to -1, 0 and +1.
- Every bit is represented by two samples (two half-bit intervals).
- NRZ-L: 0 = +1, 1 = -1.
- NRZ-I: a 1 causes a transition; a 0 causes no transition; initial level is +1.
- Manchester: 0 = high-to-low; 1 = low-to-high.
- Differential Manchester: a 0 causes a transition at the start; every bit has a middle transition; initial level is +1.
- AMI: zeros are 0 V; ones alternate polarity; initial previous-pulse state is -1.
- PCM uses uniform mid-rise quantization over the input sample range. The quantizer range is carried as decoder metadata in this simulation.
- Delta Modulation uses a fixed user-selected step size and initial reconstruction value 0.
- This is a software simulation, not a physical transmission channel; timing recovery, noise and channel distortion are not modeled.

## Files

- `data_generator.py`: bit generation and longest palindrome
- `line_coding.py`: basic line encoders
- `scrambling.py`: B8ZS and HDB3
- `line_decoder.py`: waveform-based decoders
- `analog_modulation.py`: PCM and Delta Modulation
- `main.py`: interactive application

## Acknowledgement

The submitted report should acknowledge any AI assistance, online references or discussions used, as required by the course assignment. Add the specific references consulted by your group.
