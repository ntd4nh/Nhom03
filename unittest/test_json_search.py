# Fill the Python code in this file
import unittest

from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    """Test the recursive JSON search function."""

    def test_search_found(self):
        """An existing key should return a non-empty list."""
        self.assertNotEqual([], json_search(key1, data, role="viewer"))

    def test_search_not_found(self):
        """A missing key should return an empty list."""
        self.assertEqual([], json_search(key2, data, role="viewer"))

    def test_is_a_list(self):
        """The result should be a list."""
        self.assertIsInstance(json_search(key1, data, role="viewer"), list)
    def test_wrong_role_cannot_read_secret(self):
        '''Role viewer không có quyền đọc apiKey'''
        result = json_search("apiKey", data, role="viewer")
        self.assertEqual([], result)

    def test_admin_can_read_secret(self):
        '''Role admin có toàn quyền đọc apiKey'''
        result = json_search("apiKey", data, role="admin")
        self.assertTrue(len(result) > 0)

    def test_operator_cannot_read_secret_but_can_read_ip(self):
        '''Role operator không đọc được apiKey nhưng đọc được managementIpAddress'''
        secret_res = json_search("apiKey", data, role="operator")
        ip_res = json_search("managementIpAddress", data, role="operator")
        self.assertEqual([], secret_res)
        self.assertTrue(len(ip_res) > 0)  

if __name__ == "__main__":
    unittest.main()
