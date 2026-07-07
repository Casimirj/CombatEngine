"""Unit tests for CombatEngine exceptions."""

import unittest
from combat_engine.Domain.Exceptions.InvalidLoadoutException import InvalidLoadoutException


class TestInvalidLoadoutException(unittest.TestCase):
    def test_message_is_stored(self):
        e = InvalidLoadoutException("Bad config: missing weapon")
        self.assertEqual(str(e), "Bad config: missing weapon")

    def test_is_exception(self):
        e = InvalidLoadoutException("test")
        self.assertIsInstance(e, Exception)

    def test_can_be_raised_and_caught(self):
        with self.assertRaises(InvalidLoadoutException) as ctx:
            raise InvalidLoadoutException("Something went wrong")
        self.assertEqual(str(ctx.exception), "Something went wrong")


if __name__ == "__main__":
    unittest.main()
