# test_json_search.py
"""
Unit test suite for recursive_json_search with Role-Based Access Control (RBAC).
"""

import copy
import os
import sys
import unittest

# Ensure local directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from recursive_json_search import json_search
from test_data import data, key1, key2
from policy import POLICY


class json_search_test(unittest.TestCase):
    """Test class verifying recursive JSON search functionality and RBAC security policy."""

    # ---------------------------------------------------------
    # Baseline Functional Tests
    # ---------------------------------------------------------

    def test_search_found(self):
        """Verify that an existing key is found and returns a non-empty list for an authorized role."""
        result = json_search(key1, data, role="admin")
        self.assertTrue([] != result)
        self.assertIn("Network Device 10.10.20.82 Is Unreachable From Controller", result)

    def test_search_not_found(self):
        """Verify that searching for a non-existent key returns an empty list."""
        result = json_search(key2, data, role="admin")
        self.assertTrue([] == result)

    def test_is_a_list(self):
        """Verify that json_search always returns a list object."""
        self.assertIsInstance(json_search(key1, data, role="admin"), list)
        self.assertIsInstance(json_search(key2, data, role="admin"), list)
        self.assertIsInstance(json_search(key1, data), list)

    def test_nested_aggregation(self):
        """Verify that json_search aggregates results across deeply nested dicts and lists without dropping data."""
        nested_data = {
            "issueSummary": "Summary 1",
            "nested": {
                "issueSummary": "Summary 2",
                "list_items": [
                    {"issueSummary": "Summary 3"},
                    [{"issueSummary": "Summary 4"}]
                ]
            }
        }
        result = json_search("issueSummary", nested_data, role="viewer")
        self.assertEqual(len(result), 4)
        self.assertEqual(result, ["Summary 1", "Summary 2", "Summary 3", "Summary 4"])

    # ---------------------------------------------------------
    # Security Tests Validating Role Permissions (policy.py)
    # ---------------------------------------------------------

    def test_security_viewer_denied_apikey(self):
        """Verify that viewer role is denied access to apiKey and returns an empty list (SR1, SR2)."""
        result = json_search("apiKey", data, role="viewer")
        self.assertEqual(result, [])

    def test_security_operator_denied_apikey(self):
        """Verify that operator role is denied access to apiKey and returns an empty list (SR1, SR2)."""
        result = json_search("apiKey", data, role="operator")
        self.assertEqual(result, [])

    def test_security_viewer_denied_management_ip(self):
        """Verify that viewer role is denied access to managementIpAddress and returns an empty list (SR1, SR2)."""
        result = json_search("managementIpAddress", data, role="viewer")
        self.assertEqual(result, [])

    def test_security_admin_allowed_apikey(self):
        """Verify that admin role is allowed access to apiKey and returns the correct SNMP community string (SR1, SR5)."""
        result = json_search("apiKey", data, role="admin")
        self.assertEqual(result, ["SNMP-COMMUNITY-STRING-7f3a9c"])

    def test_security_operator_allowed_management_ip(self):
        """Verify that operator role is allowed access to managementIpAddress and returns the IP (SR1, SR5)."""
        result = json_search("managementIpAddress", data, role="operator")
        self.assertEqual(result, ["10.10.20.21"])

    def test_security_viewer_allowed_issue_summary(self):
        """Verify that viewer role is allowed access to issueSummary and returns the correct message (SR1, SR5)."""
        result = json_search("issueSummary", data, role="viewer")
        self.assertEqual(result, ["Network Device 10.10.20.82 Is Unreachable From Controller"])

    def test_security_missing_or_invalid_role(self):
        """Verify that omitting role, passing None, or passing an invalid role returns an empty list (SR3)."""
        self.assertEqual(json_search("issueSummary", data), [])
        self.assertEqual(json_search("issueSummary", data, role=None), [])
        self.assertEqual(json_search("issueSummary", data, role="guest"), [])
        self.assertEqual(json_search("issueSummary", data, role="hacker"), [])
        self.assertEqual(json_search("issueSummary", data, role=""), [])
        self.assertEqual(json_search("issueSummary", data, role=12345), [])

    def test_security_unregistered_key(self):
        """Verify that searching for a key not declared in POLICY returns an empty list (SR4)."""
        self.assertEqual(json_search("deviceDetails", data, role="admin"), [])
        self.assertEqual(json_search("macAddress", data, role="admin"), [])
        self.assertEqual(json_search("id", data, role="admin"), [])

    def test_security_input_data_immutability(self):
        """Verify that json_search does not mutate the input data structure (SR5)."""
        cloned_data = copy.deepcopy(data)
        json_search("issueSummary", cloned_data, role="admin")
        json_search("apiKey", cloned_data, role="admin")
        self.assertEqual(cloned_data, data)


if __name__ == '__main__':
    unittest.main()
