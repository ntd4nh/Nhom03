# Security Requirements — Nhóm 03

## Phạm vi

Hàm `json_search(key, input_object, role=None)` tìm kiếm trong dữ liệu JSON và kiểm soát quyền đọc kết quả theo `POLICY` trong `policy.py`.

## Quyền truy cập

| Trường dữ liệu | admin | operator | viewer |
|---|---|---|---|
| apiKey | Cho phép | Từ chối | Từ chối |
| managementIpAddress | Cho phép | Cho phép | Từ chối |
| issueSummary | Cho phép | Cho phép | Cho phép |

## Yêu cầu

- **SR1:** Chỉ trả về giá trị của một trường khi role nằm trong danh sách được phép của trường đó.
- **SR2:** Khi không đủ quyền, hàm trả về danh sách rỗng `[]`. Quy định này áp dụng ở mọi mức lồng nhau của dict và list.
- **SR3 — Quyết định bổ sung:** Nếu role bị thiếu, bằng `None` hoặc không hợp lệ, hàm trả về `[]`.
- **SR4 — Quyết định bổ sung:** Nếu key chưa được khai báo trong POLICY, hàm trả về `[]`. Không mặc định cho phép đọc một đối tượng cha chứa dữ liệu nhạy cảm.
- **SR5:** Khi đủ quyền, hàm trả về đầy đủ các kết quả phù hợp dưới dạng list và không làm thay đổi dữ liệu đầu vào.

## Giả định

Role của người dùng phải được tầng xác thực đáng tin cậy cung cấp. Hàm tìm kiếm không tự xác thực danh tính và không tự xác minh người gọi có thực sự là admin hay không.

## Kiểm thử dự kiến

- viewer đọc apiKey → `[]`.
- operator đọc apiKey → `[]`.
- viewer đọc managementIpAddress → `[]`.
- admin đọc apiKey → trả về giá trị đúng.
- operator đọc managementIpAddress → trả về giá trị đúng.
- viewer đọc issueSummary → trả về giá trị đúng.
- Role thiếu hoặc không hợp lệ → `[]`.
- Key chưa được khai báo trong POLICY → `[]`.
