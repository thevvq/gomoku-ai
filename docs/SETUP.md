## Setup — Gomoku AI (ngắn gọn)

Mục tiêu: mọi người dùng cùng phiên bản Python để tránh lỗi khi cài `pygame` trên Windows.

Yêu cầu trước: cài Python 3.11 (x86-64) và chọn "Add Python to PATH" khi cài.

Link tải: https://www.python.org/downloads/release/python-3110/

1) Kiểm tra Python 3.11 đã có:

```powershell
py -3.11 --version
```

2) Tự động tạo virtualenv và cài phụ thuộc (khuyến nghị):

```powershell
.\scripts\setup.ps1
# Nếu muốn tái tạo venv sạch:
.\scripts\setup.ps1 -Recreate
```

3) Hoặc làm thủ công (nếu không dùng script):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

4) Chạy ứng dụng:

```powershell
python src/main.py
```

Ghi chú nhanh / lỗi hay gặp:
- `scripts/setup.ps1` **không** cài Python; nếu `py -3.11` không tìm thấy, cài Python 3.11 từ link ở trên.
- Nếu PowerShell chặn chạy script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

- Nếu `requirements.txt` có vấn đề mã hóa (hiếm):

```powershell
Get-Content .\requirements.txt | Out-File .\requirements-utf8.txt -Encoding utf8
pip install -r requirements-utf8.txt
```

Thêm: `scripts/setup.ps1` tạo `./.venv` và cài các gói cục bộ; không thay đổi repo (không commit venv).

Muốn mình rút ngắn phần này để bỏ vào `README.txt` không? (Mình có thể copy phiên bản ngắn vào README.)
