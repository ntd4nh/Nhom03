# recursive_json_search.py
"""
Recursive JSON Search Module with Role-Based Access Control (RBAC).

This module implements json_search(key, input_object, role=None) to recursively
search for keys within nested JSON data structures (dictionaries and lists) and
enforces access control policies defined in policy.py.
"""

import os
import sys

# Ensure local directory is in sys.path for importing policy
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from policy import POLICY
except ImportError:
    POLICY = {
        "apiKey": ["admin"],
        "managementIpAddress": ["admin", "operator"],
        "issueSummary": ["admin", "operator", "viewer"],
    }


def json_search(key, input_object, role=None):
    """
    Recursively search for a key in a JSON-like object (dicts and lists),
    enforcing role-based access control based on policy.py.

    Security Requirements:
    - SR1: Return values of a field only when role is in the allowed list for that key.
    - SR2: When permission is denied, return an empty list [].
    - SR3: If role is missing, None, or invalid, return [].
    - SR4: If key is not declared in POLICY, return [].
    - SR5: When authorized, return all matching items in a list without mutating input_object.

    :param key: The key to search for.
    :param input_object: The JSON data structure (dict, list, or primitive).
    :param role: The user role (e.g. 'admin', 'operator', 'viewer'). Defaults to None.
    :return: A list of matched values, or [] if unauthorized or not found.
    """
    # SR4: Key must be explicitly declared in POLICY
    if key not in POLICY:
        return []

    # SR3: Role must not be missing, None, or non-string
    if role is None or not isinstance(role, str):
        return []

    # SR1 & SR2: Role must be in the allowed roles list for this key
    if role not in POLICY[key]:
        return []

    # SR5: Recursive search traversing all nested dicts and lists without dropping data
    results = []

    def _recursive_search(current):
        if isinstance(current, dict):
            for k, v in current.items():
                if k == key:
                    results.append(v)
                if isinstance(v, (dict, list)):
                    _recursive_search(v)
        elif isinstance(current, list):
            for item in current:
                if isinstance(item, (dict, list)):
                    _recursive_search(item)

    _recursive_search(input_object)
    return results
