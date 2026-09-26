from policy import POLICY
from test_data import data


def _filter_value(value, role):
    """Filter nested fields according to the access policy."""
    if isinstance(value, dict):
        return {
            k: _filter_value(v, role)
            for k, v in value.items()
            if role in POLICY.get(k, [])
        }

    if isinstance(value, list):
        return [_filter_value(item, role) for item in value]

    return value


def json_search(key, input_object, role=None):
    """Find matching fields only when the role is authorized."""
    if not isinstance(key, str) or not isinstance(role, str):
        return []

    if role not in POLICY.get(key, []):
        return []

    results = []

    if isinstance(input_object, dict):
        for k, v in input_object.items():
            if k == key:
                results.append({k: _filter_value(v, role)})

            results.extend(json_search(key, v, role=role))

    elif isinstance(input_object, list):
        for item in input_object:
            results.extend(json_search(key, item, role=role))

    return results


if __name__ == "__main__":
    print(json_search("issueSummary", data, role="viewer"))
