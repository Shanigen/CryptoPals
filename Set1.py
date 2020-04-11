import base64
import sys

class Set1(object):
    """Solutions for qualifying exercises from Set 1 in Cryptopals."""
    @staticmethod
    def hex2base64(hex_input:bytes):
        """ Converts bytes representing hex string to bytes representing base64 string """
        return base64.b64encode(hex_input)

    @staticmethod
    def xor(hex_input1:bytes, hex_input2:bytes):
        """ Takes two equal-length buffers and produces their XOR combination in bytes. """
        return bytes([r ^ l for r, l in zip(hex_input1, hex_input2)])

    @staticmethod
    def chi_squared_scoring(text:bytes):
        """ Returns the chi-squared statistic of the text. """
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        frequencies = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
        text = text.upper().replace(b" ", b"")
        expected_counts = dict(zip(letters, list(map(lambda x: x * len(text), frequencies))))
        actual_counts = {letter: text.count(letter.encode()) for letter in letters}

        normalized_square_error = lambda a, e: (a - e)**2/e
        return sum([normalized_square_error(actual_counts[letter], expected_counts[letter]) for letter in letters])

    @staticmethod
    def single_byte_decipher(hex_input:bytes):
        """ Takes bytes representing hex encoded string that was XOR'd against a single character. Returns tuple containg key and decrypted message. """
        scores = {}
        for i in range(256):
            scores[chr(i)] = Set1.chi_squared_scoring(Set1.xor(hex_input, [i] * len(hex_input)))

        # Get key with minimal chi-squared error.
        key = min(scores,key = scores.get)
        return (key, Set1.xor(hex_input, [ord(key)] * len(hex_input)))

def main():
    pass

if __name__ == "__main__":
    sys.exit(int(main() or 0))

