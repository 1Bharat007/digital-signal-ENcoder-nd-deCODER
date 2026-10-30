"""Quick round-trip checks for project encoders and decoders."""
import unittest
from data_generator import longest_palindrome
from line_coding import nrz_l, nrz_i, manchester, differential_manchester, ami
from scrambling import b8zs, hdb3
from line_decoder import (
    decode_nrz_l, decode_nrz_i, decode_manchester,
    decode_differential_manchester, decode_ami, decode_b8zs, decode_hdb3,
)
from analog_modulation import pcm_encode, pcm_decode, delta_encode, delta_decode


class ProjectTests(unittest.TestCase):
    def test_basic_line_codes(self):
        bits = [1, 0, 1, 1, 0, 0, 1, 0]
        cases = [
            (nrz_l, decode_nrz_l),
            (nrz_i, decode_nrz_i),
            (manchester, decode_manchester),
            (differential_manchester, decode_differential_manchester),
            (ami, decode_ami),
        ]
        for encoder, decoder in cases:
            self.assertEqual(decoder(encoder(bits)), bits)

    def test_b8zs(self):
        for bits in ([1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]):
            self.assertEqual(decode_b8zs(b8zs(list(bits))), list(bits))

    def test_hdb3(self):
        for bits in ([0, 0, 0, 0], [1, 0, 0, 0, 0, 1],
                     [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]):
            self.assertEqual(decode_hdb3(hdb3(list(bits))), list(bits))

    def test_analog(self):
        samples = [-1, -0.5, 0, 0.5, 1]
        pcm_bits, meta = pcm_encode(samples, 4)
        pcm_result = pcm_decode(pcm_bits, meta["bits_per_sample"], meta["vmin"], meta["vmax"])
        self.assertEqual(len(pcm_result), len(samples))
        dm_bits = delta_encode(samples, 0.25)
        dm_result = delta_decode(dm_bits, 0.25)
        self.assertEqual(len(dm_result), len(samples))

    def test_palindrome(self):
        self.assertEqual(longest_palindrome([1, 1, 0, 1, 0, 0, 1]), [1, 0, 0, 1])


if __name__ == "__main__":
    unittest.main()
