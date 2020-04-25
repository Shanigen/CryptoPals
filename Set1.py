import base64
import sys
from itertools import cycle
from bitstring import Bits


class Set1(object):
    """Solutions for qualifying exercises from Set 1 in Cryptopals."""

    @staticmethod
    def hex2base64(text: bytes) -> bytes:
        """ Converts bytes representing hex string to bytes representing base64 string """
        return base64.b64encode(text)

    @staticmethod
    def base64decode(text: bytes) -> bytes:
        """ Decode base64 encoded bytes-like object. """
        return base64.b64decode(text)

    @staticmethod
    def fixed_xor(text: bytes, key: bytes) -> bytes:
        """ Takes two equal-length buffers and produces their XOR combination in bytes. """
        return bytes([l ^ r for l, r in zip(text, key)])

    @staticmethod
    def chi_squared_scoring(text: bytes) -> float:
        """ Returns the chi-squared statistic of the text. """
        letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        frequencies = [
            8.167,
            1.492,
            2.782,
            4.253,
            12.702,
            2.228,
            2.015,
            6.094,
            6.966,
            0.153,
            0.772,
            4.025,
            2.406,
            6.749,
            7.507,
            1.929,
            0.095,
            5.987,
            6.327,
            9.056,
            2.758,
            0.978,
            2.360,
            0.150,
            1.974,
            0.074,
        ]
        text = text.upper().replace(b" ", b"")
        expected_counts = dict(
            zip(letters, list(map(lambda x: x * len(text), frequencies)))
        )
        actual_counts = {letter: text.count(letter.encode()) for letter in letters}

        normalized_square_error = lambda a, e: (a - e) ** 2 / e
        return sum(
            [
                normalized_square_error(actual_counts[letter], expected_counts[letter])
                for letter in letters
            ]
        )

    @staticmethod
    def single_byte_xor_decipher(text: bytes) -> (bytes, bytes):
        """ Takes bytes representing hex encoded string that was XOR'd against a single character. Returns tuple containg key and decrypted message. """
        scores = {}
        for i in range(256):
            scores[chr(i)] = Set1.chi_squared_scoring(
                Set1.fixed_xor(text, [i] * len(text))
            )
        # Get key with minimal chi-squared error.
        key = min(scores, key=scores.get)

        return (key.encode(), Set1.fixed_xor(text, [ord(key)] * len(text)))

    @staticmethod
    def detect_single_char_xor(input_file):
        best_score = sys.maxsize
        english_text = ""
        key = ""

        with open(input_file, "r") as f:
            for line in f:
                result = Set1.single_byte_xor_decipher(bytes.fromhex(line.rstrip()))
                score = Set1.chi_squared_scoring(result[1])
                if best_score > score:
                    best_score = score
                    english_text = result[1]
                    key = result[0]

        return (key, english_text)

    @staticmethod
    def repeated_xor(text: bytes, key: bytes) -> bytes:
        """ Takes two non equal-length buffers and produces their XOR combination in bytes."""
        longer, shorter = b"", b""
        if len(text) >= len(key):
            longer = text
            shorter = key
        else:
            longer = key
            shorter = text

        return bytes([l ^ s for l, s in zip(longer, cycle(shorter))])

    @staticmethod
    def hamming_distance(text1: bytes, text2: bytes) -> int:
        """ Return Hamming distance between binary representations of the two input texts."""
        distance = 0

        for l, r in zip(Bits(text1).bin, Bits(text2).bin):
            distance += 1 if l != r else 0
        return distance

    @staticmethod
    def break_repeating_key_xor(text: bytes) -> (bytes, bytes):
        keysizes_scores = {}
        # Get normalized edit distances and find the 3 keysizes with best score
        for keysize in range(2, 41):
            blocks = [text[i * keysize : (i * keysize) + keysize] for i in range(4)]
            distances = [
                Set1.hamming_distance(blocks[i], blocks[i + 1])
                for i in range(len(blocks) - 1)
            ]
            keysizes_scores[keysize] = (sum(distances) / len(distances)) / keysize

        keysizes_scores = {k: v for k, v in sorted(keysizes_scores.items(), key=lambda item: item[1])}
        best_keysizes = list(keysizes_scores.keys())[0:3]

        keys = {}
        for keysize in best_keysizes:
            keysized_blocks = [
                text[i * keysize : (i * keysize) + keysize]
                for i in range(len(text) // keysize)
            ]

            transposed_blocks = [b"" for _ in range(keysize)]
            for i in range(keysize):
                for block in keysized_blocks:
                    transposed_blocks[i] += bytes([block[i]])

            key = b""
            for block in transposed_blocks:
                key += Set1.single_byte_xor_decipher(block)[0]
            keys[keysize] = key

        text_scores = {} 
        for keysize, key in keys.items():
            text_scores[key] = Set1.chi_squared_scoring(Set1.repeated_xor(text, key))
        key = min(text_scores, key=text_scores.get)
        
        return (key, Set1.repeated_xor(text, key))
        


def main():
    pass


if __name__ == "__main__":
    sys.exit(int(main() or 0))
