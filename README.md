# 🎮 Gomoku AI

Ứng dụng trò chơi Gomoku (Caro) được xây dựng bằng **Python** với AI sử dụng thuật toán **Minimax**, **Alpha-Beta Pruning** và **Heuristic Evaluation** để lựa chọn nước đi.

Dự án được thực hiện nhằm áp dụng các thuật toán tìm kiếm trong Trí tuệ nhân tạo (Artificial Intelligence) vào bài toán trò chơi đối kháng.

---

# ✨ Tính năng

- Chơi Gomoku giữa người và AI.
- Ba mức độ khó:
  - Easy
  - Medium
  - Hard

- AI sử dụng:
  - Minimax
  - Alpha-Beta Pruning
  - Heuristic Evaluation

- Phát hiện thắng, thua và hòa.
- Hỗ trợ hai giao diện:
  - Web (FastAPI + HTML/CSS/JavaScript)

---

# 🧠 Thuật toán sử dụng

## Minimax

Minimax được sử dụng để mô phỏng các nước đi có thể xảy ra trong tương lai và lựa chọn nước đi mang lại kết quả tốt nhất cho AI.

## Alpha-Beta Pruning

Alpha-Beta Pruning giúp loại bỏ các nhánh không cần thiết trong cây tìm kiếm, từ đó giảm thời gian tính toán mà vẫn đảm bảo kết quả giống Minimax.

## Heuristic Evaluation

Ở những trạng thái chưa kết thúc, AI sử dụng hàm đánh giá để chấm điểm bàn cờ dựa trên các mẫu chiến thuật như:

- Five in a Row
- Open Four
- Closed Four
- Open Three
- Closed Three
- Open Two

Giá trị đánh giá được dùng để xác định nước đi tối ưu.

---

# 🚀 Cài đặt

## Yêu cầu

- Python 3.11 trở lên

## Cài đặt thư viện

```bash
pip install -r requirements.txt
```

---

# ▶️ Chạy chương trình

```bash
python src/main.py
```

Sau khi khởi động server, mở trình duyệt tại:


[http://localhost:7891](http://localhost:7891)

---

# 🎮 Luật chơi

- Người chơi và AI lần lượt đặt quân lên bàn cờ.
- Người đầu tiên tạo được **5 quân liên tiếp** theo hàng ngang, dọc hoặc chéo sẽ chiến thắng.
- Không thể đánh vào ô đã có quân.

---

# 📂 Cấu trúc dự án

```text
gomoku-ai/
├── src/
│   ├── ai.py
│   ├── minimax.py
│   ├── heuristic.py
│   ├── board.py
│   ├── game.py
│   ├── main.py
│   ├── server.py
│   ├── config.py
│   └── database.py
│
├── docs/
├── tests/
├── scripts/
├── requirements.txt
└── README.md
```

---

# ⚙️ Công nghệ sử dụng

| Thành phần  | Công nghệ                                         |
| ----------- | ------------------------------------------------- |
| Ngôn ngữ    | Python 3.11                                       |
| Desktop GUI | Pygame                                            |
| Backend     | FastAPI                                           |
| Frontend    | HTML5, CSS3, JavaScript                           |
| AI          | Minimax, Alpha-Beta Pruning, Heuristic Evaluation |

---

# 📚 Kiến thức áp dụng

Dự án áp dụng các kiến thức:

- Game Tree Search
- Minimax Algorithm
- Alpha-Beta Pruning
- Heuristic Design
- Artificial Intelligence
- Python Desktop Application
- Web Application Development

---

# 📌 Hướng phát triển

Các tính năng có thể bổ sung trong tương lai:

- Lưu lịch sử ván đấu.
- AI đấu với AI.
- Chế độ nhiều người chơi.
- Cải thiện hàm Heuristic.
- Tối ưu tốc độ tìm kiếm.
- Phân tích và gợi ý nước đi.

---

# 📄 Giấy phép

Dự án được phát triển phục vụ mục đích học tập, nghiên cứu và tìm hiểu các thuật toán Trí tuệ nhân tạo.

---

# 👨‍💻 Tác giả

**Nhóm 8 **

Sinh viên ngành Công nghệ Thông tin.

Đồ án được thực hiện nhằm nghiên cứu và ứng dụng các thuật toán AI vào trò chơi Gomoku.
