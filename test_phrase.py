import pytest

class TestPhrase:
    def test_input_phrase(self):
        phrase = input("\nSet a phrase shorter than 15 symbols:")

        assert len(phrase) < 15, f"Phrase is longer than 15 symbols!!! ({len(phrase)}symbols)"