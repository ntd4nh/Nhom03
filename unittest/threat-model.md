# Threat Model — Nhóm 03

## 1. Bối cảnh và vai trò

Hàm json_search tra cứu dữ liệu từ API giám sát hạ tầng mạng.

- **admin:** quản trị hệ thống; được đọc cả ba trường trong POLICY.
- **operator:** vận hành hệ thống; được đọc managementIpAddress và issueSummary.
- **viewer:** theo dõi tình trạng; chỉ được đọc issueSummary trong ba trường đã quy định.

## 2. Tài sản cần bảo vệ

- apiKey: trong dữ liệu mẫu, trường này chứa chuỗi xác thực SNMP.
- managementIpAddress: địa chỉ IP quản trị thiết bị.
- Các thông tin nhận diện thiết bị như hostname, MAC và serialNumber cần được xem xét khi mở rộng chính sách.

## 3. Ranh giới tin cậy

Dữ liệu API có thể chứa thông tin mà người gọi không được phép xem. Ranh giới cần kiểm soát nằm giữa dữ liệu đầu vào đầy đủ và kết quả trả về cho từng role.

Nếu hàm chỉ tìm thấy key rồi trả về mà không kiểm tra POLICY, dữ liệu nhạy cảm có thể vượt qua ranh giới này.

Role phải đến từ tầng xác thực đáng tin cậy. Trường role có giá trị ACCESS trong dữ liệu thiết bị không phải role của người dùng gọi hàm.

## 4. Các đe dọa

| Mã | Nhóm STRIDE | Tình huống | Biện pháp |
|---|---|---|---|
| T1 | Information Disclosure | viewer hoặc operator tìm apiKey và nhận được bí mật SNMP | Kiểm tra quyền trước khi trả kết quả; áp dụng SR1 và SR2 |
| T2 | Information Disclosure | viewer đọc managementIpAddress | Từ chối và trả về []; áp dụng SR1 và SR2 |
| T3 | Information Disclosure | Người gọi tìm đối tượng cha deviceDetails để nhận cả apiKey bên trong | Từ chối key chưa có trong POLICY; áp dụng SR4 |
| T4 | Spoofing / Elevation of Privilege | Người dùng tự khai role=admin để vượt quyền | Tầng xác thực phải xác định role; không tin role do người dùng tự gửi |

## 5. Giới hạn

Kiểm tra chuỗi role trong json_search không đủ để ngăn giả mạo role nếu tầng gọi hàm chưa xác thực người dùng.

Chính sách bảo vệ trường managementIpAddress, không bảo đảm che mọi địa chỉ IP xuất hiện trong nội dung văn bản của issueSummary.
