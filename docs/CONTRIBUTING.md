# Hướng Dẫn Đóng Góp

File này quy định workflow làm việc nhóm và các quy tắc Git cho project Gomoku AI.

Vui lòng đọc kỹ trước khi tham gia phát triển dự án.

---

# Quy Tắc Chung

- KHÔNG code trực tiếp trên nhánh `main`.
- Mỗi tính năng hoặc lỗi phải được phát triển trên một nhánh riêng.
- Luôn pull code mới nhất trước khi bắt đầu làm việc.
- Commit phải rõ ràng, ngắn gọn và có ý nghĩa.
- Tránh chỉnh sửa các file không liên quan.
- Test code trước khi push lên GitHub.

---

# Quy Tắc Về Nhánh

Mỗi tính năng hoặc lỗi cần được xử lý trên một nhánh riêng.

## Quy Ước Đặt Tên Nhánh

### Nhánh tính năng

```text
feature/board-ui
feature/click-input
feature/random-ai
feature/heuristic
feature/minimax
feature/alpha-beta
```

### Nhánh sửa lỗi

```text
fix/win-check
fix/board-rendering
```

### Nhánh tài liệu

```text
docs/readme-update
docs/project-structure
```

> Tên nhánh phải mô tả đúng công việc đang thực hiện.
> KHÔNG đặt theo tên thành viên.

GitHub đã tự lưu thông tin người tạo và người push branch.

---

# Quy Trình Làm Việc Với Git

## 1. Clone Repository (Lần đầu)

```bash
git clone https://github.com/thevvq/gomoku-ai.git
cd gomoku-ai
```

---

## 2. Tạo Nhánh Mới

```bash
git checkout -b feature/your-feature-name
```

Ví dụ:

```bash
git checkout -b feature/minimax
```

---

## 3. Trước Mỗi Lần Code

Luôn cập nhật code mới nhất:

```bash
git checkout main
git pull origin main
```

Quay lại nhánh của mình:

```bash
git checkout <your-branch>
```

Merge code mới từ `main`:

```bash
git merge main
```

Việc này giúp giảm conflict khi merge sau này.

---

# Quy Tắc Làm Việc

Chỉ chỉnh sửa các file liên quan đến phần việc được giao.

| Chức năng  | File                                  |
| ---------- | ------------------------------------- |
| Board UI   | `board.py`, `config.py`               |
| Game Logic | `game.py`                             |
| AI         | `ai.py`, `heuristic.py`, `minimax.py` |

Tránh chỉnh sửa các module không liên quan nếu không cần thiết.

---

# Commit Và Push Code

Sau khi code xong:

```bash
git add .
```

Tạo commit:

```bash
git commit -m "Tên: mô tả ngắn"
```

Ví dụ:

```bash
git commit -m "Quyen: implement minimax recursion"
git commit -m "Ngan: add board rendering"
```

Push code lên GitHub:

```bash
git push -u origin <your-branch-name>
```

Ví dụ:

```bash
git push -u origin feature/minimax
```

---

# Quy Tắc Commit

## Format chuẩn

```text
Tên: mô tả ngắn
```

## Ví dụ tốt

```text
Quyen: add heuristic evaluation
Ngan: implement board grid
```

## Tránh commit kiểu

```text
update
fix
final
abcxyz
code
```

Commit message cần mô tả rõ phần công việc đã làm.

---

# Pull Request Và Merge

Sau khi hoàn thành tính năng:

1. Push branch lên GitHub
2. Chờ review trước khi merge

---

# Tránh Merge Conflict

- Luôn pull `main` mới nhất
- Merge `main` vào branch thường xuyên
- Chỉ sửa module được giao
- Không format lại toàn bộ file nếu không cần

---

# Khi Bị Conflict

Nếu xảy ra conflict:

- KHÔNG tự ý xóa code của người khác
- So sánh thay đổi cẩn thận
- Hỏi teammate nếu không chắc
- Resolve conflict cùng nhau nếu cần

---

# Mục Tiêu Chung

Xây dựng một project Gomoku AI:

- sạch
- ổn định
- dễ mở rộng
- có workflow chuyên nghiệp
- thể hiện đúng định hướng môn AI
