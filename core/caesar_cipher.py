"""
Caesar Cipher (Additive Cipher) Core Engine.

Provides clean, modular functions for encrypting, decrypting, and brute-force
cracking text using the Caesar cipher algorithm.
"""

from typing import List, Dict, Any, Tuple
import math

# Standard English letter frequencies for likelihood scoring in brute-force
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.01, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}


class CaesarCipher:
    """Core cryptographic engine for General Caesar / Additive Cipher operations."""

    @staticmethod
    def shift_char(char: str, key: int) -> str:
        """
        Shifts a single character by `key` positions.
        Preserves uppercase/lowercase casing and leaves non-alphabetic chars intact.
        """
        if 'A' <= char <= 'Z':
            return chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            return chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        else:
            return char

    @classmethod
    def encrypt(cls, text: str, key: int) -> str:
        """
        Encrypts plaintext using shift key K:
        C = (P + K) mod 26
        """
        if not text:
            return ""
        normalized_key = key % 26
        return "".join(cls.shift_char(ch, normalized_key) for ch in text)

    @classmethod
    def decrypt(cls, text: str, key: int) -> str:
        """
        Decrypts ciphertext using shift key K:
        P = (C - K) mod 26
        """
        if not text:
            return ""
        normalized_key = (-key) % 26
        return "".join(cls.shift_char(ch, normalized_key) for ch in text)

    @classmethod
    def score_text_frequency(cls, text: str) -> float:
        """
        Calculates a chi-squared frequency score comparing letter distribution
        in `text` against standard English letter frequencies.
        Lower score indicates higher likelihood of natural English text.
        """
        letters_only = [c.upper() for c in text if c.isalpha() and 'A' <= c.upper() <= 'Z']
        total_letters = len(letters_only)

        if total_letters == 0:
            return 999.0

        counts = {chr(i + ord('A')): 0 for i in range(26)}
        for ch in letters_only:
            counts[ch] += 1

        chi_squared = 0.0
        for char, freq in ENGLISH_FREQUENCIES.items():
            expected = (freq / 100.0) * total_letters
            observed = counts.get(char, 0)
            chi_squared += ((observed - expected) ** 2) / (expected + 1e-5)

        return chi_squared

    @classmethod
    def brute_force(cls, ciphertext: str) -> List[Dict[str, Any]]:
        """
        Attempts all 26 possible shift keys (k = 0 to 25) on ciphertext.
        Returns a sorted list of candidate decryptions with likelihood confidence percentages.
        """
        results = []
        if not ciphertext.strip():
            return results

        scores = []
        for k in range(26):
            decrypted = cls.decrypt(ciphertext, k)
            score = cls.score_text_frequency(decrypted)
            scores.append((k, decrypted, score))

        # Sort by chi-squared score ascending (lowest score = highest match)
        scores.sort(key=lambda item: item[2])

        min_score = scores[0][2]
        max_score = max(item[2] for item in scores)
        score_range = (max_score - min_score) if (max_score - min_score) > 1e-5 else 1.0

        for key, decrypted_text, score in scores:
            # Map score to confidence percentage (0% to 100%)
            confidence = max(0.0, min(100.0, 100.0 * (1.0 - (score - min_score) / score_range)))
            results.append({
                'key': key,
                'decrypted': decrypted_text,
                'score': round(score, 2),
                'confidence': round(confidence, 1)
            })

        # Sort final results by key (0..25) but highlight best match candidate
        best_key = results[0]['key']
        results.sort(key=lambda x: x['key'])
        for res in results:
            res['is_best_match'] = (res['key'] == best_key)

        return results
