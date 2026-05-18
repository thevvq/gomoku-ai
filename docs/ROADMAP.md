# Lộ Trình Phát Triển Gomoku AI

## Tổng Quan Dự Án

Dự án này nhằm xây dựng một trò chơi Gomoku có tích hợp AI bằng Python và Pygame.
AI sẽ được phát triển dần từ một hệ thống đi ngẫu nhiên đơn giản thành đối thủ thông minh sử dụng đánh giá heuristic và thuật toán Minimax kết hợp Alpha-Beta Pruning.

---

# Lộ Trình Phát Triển

## Giai Đoạn 1 — Vẽ Bàn Cờ

### Mục Tiêu

Tạo giao diện bàn cờ Gomoku bằng đồ họa.

### Công Việc

- Khởi tạo cửa sổ Pygame
- Vẽ bàn cờ 10x10 hoặc 15x15
- Hiển thị các đường lưới
- Hiển thị tiêu đề trò chơi

### Kết Quả Mong Đợi

Có giao diện bàn cờ hiển thị và sẵn sàng để chơi.

### File Chính

- `main.py`
- `board.py`

---

## Giai Đoạn 2 — Xử Lý Tương Tác Người Chơi

### Mục Tiêu

Cho phép người chơi đặt quân cờ bằng chuột.

### Công Việc

- Nhận vị trí click chuột
- Chuyển tọa độ chuột thành ô trên bàn cờ
- Đặt quân X/O lên bàn cờ
- Ngăn không cho đặt vào ô đã có quân

### Kết Quả Mong Đợi

Người chơi có thể tương tác với bàn cờ bình thường.

### File Chính

- `game.py`
- `board.py`

---

## Giai Đoạn 3 — Hệ Thống Kiểm Tra Thắng

### Mục Tiêu

Phát hiện điều kiện chiến thắng trong trò chơi.

### Công Việc

- Kiểm tra hàng ngang
- Kiểm tra hàng dọc
- Kiểm tra đường chéo
- Phát hiện 5 quân liên tiếp

### Kết Quả Mong Đợi

Trò chơi thông báo người chiến thắng chính xác.

### File Chính

- `game.py`

---

## Giai Đoạn 4 — AI Chơi Ngẫu Nhiên

### Mục Tiêu

Xây dựng AI cơ bản.

### Công Việc

- Sinh các nước đi hợp lệ
- Chọn ngẫu nhiên một ô trống
- Luân phiên lượt chơi giữa người chơi và AI

### Kết Quả Mong Đợi

Người chơi có thể đấu với AI cơ bản.

### File Chính

- `ai.py`

---

## Giai Đoạn 5 — Đánh Giá Heuristic

### Mục Tiêu

Cải thiện AI bằng hệ thống chấm điểm heuristic.

### Công Việc

- Đánh giá trạng thái bàn cờ
- Gán điểm cho các mẫu chiến thuật:
  - Bốn mở
  - Ba mở
  - Chuỗi bị chặn

- Ưu tiên cả tấn công và phòng thủ

### Ví Dụ Bảng Heuristic

| Mẫu              | Điểm   |
| ---------------- | ------ |
| 5 quân liên tiếp | 100000 |
| Bốn mở           | 10000  |
| Ba mở            | 1000   |
| Chặn bốn đối thủ | 9000   |

### Kết Quả Mong Đợi

AI biết đưa ra quyết định chiến thuật thay vì đi ngẫu nhiên.

### File Chính

- `heuristic.py`
- `ai.py`

---

## Giai Đoạn 6 — Minimax + Alpha-Beta Pruning

### Mục Tiêu

Xây dựng AI có khả năng ra quyết định thông minh.

### Công Việc

- Xây dựng cây tìm kiếm Minimax
- Mô phỏng các nước đi tương lai
- Đánh giá bàn cờ bằng đệ quy
- Tối ưu tìm kiếm bằng Alpha-Beta Pruning

### Kết Quả Mong Đợi

AI có thể dự đoán nước đi tương lai và chơi chiến thuật hơn.

### File Chính

- `minimax.py`
- `ai.py`

---

# Hướng Phát Triển Trong Tương Lai

## Các Tính Năng Có Thể Bổ Sung

- Nhiều mức độ khó
- Thiết kế giao diện đẹp hơn
- Hiển thị quá trình AI suy nghĩ
- Lịch sử nước đi
- Chức năng hoàn tác (Undo)
- Hiệu ứng âm thanh
- Chế độ nhiều người chơi

---

# Công Nghệ Sử Dụng

- Python
- Pygame
- Thuật toán Minimax
- Alpha-Beta Pruning
- Đánh giá Heuristic

---

# Mục Tiêu Học Tập

Dự án giúp rèn luyện:

- Kiến thức về Trí tuệ nhân tạo
- Thuật toán tìm kiếm
- Đánh giá heuristic
- Quản lý trạng thái trò chơi
- Lập trình đệ quy
- Tối ưu thuật toán

---

# Mục Tiêu Cuối Cùng

Xây dựng một hệ thống Gomoku AI hoàn chỉnh có thể cạnh tranh với người chơi bằng các thuật toán ra quyết định thông minh.
