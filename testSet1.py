import unittest
import sys
from Set1 import Set1


class Test_Set1(unittest.TestCase):
    def test_task1(self):
        hex_input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

        result = Set1.hex2base64(bytes.fromhex(hex_input))

        self.assertEqual(expected, result.decode())

    def test_task2(self):
        input1 = "1c0111001f010100061a024b53535009181c"
        input2 = "686974207468652062756c6c277320657965"
        expected = "746865206b696420646f6e277420706c6179"

        result = Set1.fixed_xor(bytes.fromhex(input1), bytes.fromhex(input2))

        self.assertEqual(expected, result.hex())

    def test_task3(self):
        hex_input = (
            "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
        )

        self.assertEqual(
            ("X", b"Cooking MC's like a pound of bacon"),
            Set1.single_byte_decipher(bytes.fromhex(hex_input)),
        )

    def test_task4(self):
        best_score = sys.maxsize
        english_text = ""
        key = ""

        with open("set1task4.txt", "r") as f:
            for line in f:
                result = Set1.single_byte_decipher(bytes.fromhex(line.rstrip()))
                score = Set1.chi_squared_scoring(result[1])
                if best_score > score:
                    best_score = score
                    english_text = result[1]
                    key = result[0]

        self.assertEqual(("5", b"Now that the party is jumping\n"), (key, english_text))

    def test_task5(self):
        input = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
        key = "ICE"
        expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

        result = Set1.repeated_xor(input.encode(), key.encode())

        self.assertEqual(expected, result.hex())


if __name__ == "__main__":
    unittest.main()
