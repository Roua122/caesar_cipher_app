"""
Validation and sanitization helper methods for inputs.
"""

class CipherValidator:
    """Helper class to validate key inputs and text payloads."""

    @staticmethod
    def validate_key(key_input: any) -> int:
        """Sanitizes key input to a valid integer."""
        try:
            val = int(key_input)
            return val % 26
        except (ValueError, TypeError):
            return 3  # Default fallback Caesar key

    @staticmethod
    def get_alphabet_stats(text: str) -> dict:
        """Returns statistics on letter counts, uppercase, lowercase, numbers, and symbols."""
        total = len(text)
        alpha = sum(1 for c in text if c.isalpha())
        digits = sum(1 for c in text if c.isdigit())
        spaces = sum(1 for c in text if c.isspace())
        symbols = total - alpha - digits - spaces
        return {
            'total': total,
            'alpha': alpha,
            'digits': digits,
            'spaces': spaces,
            'symbols': symbols
        }
