import unittest
from copy import deepcopy

from recursive_json_search import json_search
from test_data import data


class SecurityRegressionTest(unittest.TestCase):
    def test_missing_or_invalid_role_is_denied(self):
        """SR3: missing, None and unknown roles are denied."""
        self.assertEqual([], json_search("issueSummary", data))

        for role in (None, "guest", ""):
            with self.subTest(role=role):
                self.assertEqual(
                    [],
                    json_search("issueSummary", data, role=role),
                )

    def test_unlisted_parent_is_denied(self):
        """SR4: querying a parent must not expose nested secrets."""
        for role in ("admin", "operator", "viewer"):
            with self.subTest(role=role):
                self.assertEqual(
                    [],
                    json_search("deviceDetails", data, role=role),
                )

    def test_viewer_cannot_read_management_ip(self):
        """Viewer cannot read the management IP address."""
        self.assertEqual(
            [],
            json_search("managementIpAddress", data, role="viewer"),
        )

    def test_nested_secret_is_filtered_without_mutation(self):
        """An allowed field cannot expose a nested secret."""
        sample = {"issueSummary": {"apiKey": "sample-secret"}}
        original = deepcopy(sample)

        self.assertEqual(
            [{"issueSummary": {}}],
            json_search("issueSummary", sample, role="viewer"),
        )
        self.assertEqual(original, sample)


if __name__ == "__main__":
    unittest.main()
