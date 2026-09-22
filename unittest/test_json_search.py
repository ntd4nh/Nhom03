# Fill the Python code in this file
import unittest

from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    """Test the recursive JSON search function."""

    def test_search_found(self):
        """An existing key should return a non-empty list."""
        self.assertNotEqual([], json_search(key1, data))

    def test_search_not_found(self):
        """A missing key should return an empty list."""
        self.assertEqual([], json_search(key2, data))

    def test_is_a_list(self):
        """The result should be a list."""
        self.assertIsInstance(json_search(key1, data), list)


if __name__ == "__main__":
    unittest.main()
