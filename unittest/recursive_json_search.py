from test_data import *
import policy

def json_search(key, input_object, role=None):
    # Nếu không truyền role, hệ thống áp dụng vai trò mặc định tối thiểu là 'viewer'
    if role is None:
        role = "viewer"

    # Lấy bảng phân quyền từ policy.py
    rules = getattr(policy, 'POLICY', getattr(policy, 'policy', {}))

    # Nếu key thuộc danh mục kiểm soát quyền và role không hợp lệ -> từ chối
    if key in rules:
        if role not in rules[key]:
            return []

    ret_val = []
    if isinstance(input_object, dict):
        for k, v in input_object.items():
            if k == key:
                ret_val.append({k: v})
            if isinstance(v, dict):
                ret_val.extend(json_search(key, v, role=role))
            elif isinstance(v, list):
                for item in v:
                    if not isinstance(item, (str, int)):
                        ret_val.extend(json_search(key, item, role=role))
    elif isinstance(input_object, list):
        for val in input_object:
            if not isinstance(val, (str, int)):
                ret_val.extend(json_search(key, val, role=role))
    return ret_val

if __name__ == '__main__':
    print(json_search("issueSummary", data))
