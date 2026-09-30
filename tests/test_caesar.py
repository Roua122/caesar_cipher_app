"""
Unit tests for CaesarCipher core engine.
"""

import unittest
from core.caesar_cipher import CaesarCipher


class TestCaesarCipher(unittest.TestCase):

    def test_encryption_basic(self):
        self.assertEqual(CaesarCipher.encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(CaesarCipher.encrypt("hello", 3), "khoor")
        self.assertEqual(CaesarCipher.encrypt("Hello World!", 3), "Khoor Zruog!")

    def test_decryption_basic(self):
        self.assertEqual(CaesarCipher.decrypt("KHOOR", 3), "HELLO")
        self.assertEqual(CaesarCipher.decrypt("khoor", 3), "hello")
        self.assertEqual(CaesarCipher.decrypt("Khoor Zruog!", 3), "Hello World!")

    def test_wrap_around(self):
        self.assertEqual(CaesarCipher.encrypt("XYZ", 3), "ABC")
        self.assertEqual(CaesarCipher.decrypt("ABC", 3), "XYZ")

    def test_large_and_negative_keys(self):
        self.assertEqual(CaesarCipher.encrypt("ABC", 29), "DEF")  # 29 mod 26 = 3
        self.assertEqual(CaesarCipher.decrypt("DEF", -3), "GHI")  # -3 mod 26 = 23 -> encrypt shift

    def test_brute_force(self):
        encrypted = CaesarCipher.encrypt("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", 7)
        candidates = CaesarCipher.brute_force(encrypted)
        best_match = next(c for c in candidates if c['is_best_match'])
        self.assertEqual(best_match['key'], 7)
        self.assertEqual(best_match['decrypted'], "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG")


if __name__ == '__main__':
    unittest.main()
