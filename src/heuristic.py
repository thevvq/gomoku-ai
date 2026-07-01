"""
heuristic.py — Giai Đoạn 5: Đánh Giá Heuristic
================================================
Chấm điểm trạng thái bàn cờ dựa trên các mẫu chiến thuật:

  Điểm Tấn Công (AI = 'O'):
    5 quân liên tiếp   → 100 000
    Bốn mở (open-4)    →  10 000
    Bốn bị chặn 1 đầu  →   5 000
    Ba mở (open-3)     →   1 000
    Ba bị chặn 1 đầu   →     200
    Hai mở (open-2)    →      50
    Một quân           →      10

  Điểm Phòng Thủ (đối thủ 'X'):
    5 quân liên tiếp   → -100 000  (phải chặn ngay)
    Bốn mở đối thủ     →  -9 000
    Bốn bị chặn đối thủ →  -4 500
    Ba mở đối thủ      →    -800
    Ba bị chặn đối thủ →    -150
    Hai mở đối thủ     →     -30
"""

import random

from config import BOARD_SIZE

# ---------------------------------------------------------------------------
# Bảng điểm theo (count, open_ends)
#   open_ends = 2 → cả hai đầu trống (open)
#   open_ends = 1 → một đầu bị chặn
#   open_ends = 0 → cả hai đầu bị chặn (vô nghĩa, bỏ qua)
# ---------------------------------------------------------------------------

SCORE_TABLE = {
    # (count, open_ends): score
    (5, 2): 100_000,
    (5, 1): 100_000,
    (5, 0): 100_000,
    (4, 2):  10_000,
    (4, 1):   5_000,
    (3, 2):   1_000,
    (3, 1):     200,
    (2, 2):      50,
    (2, 1):      10,
    (1, 2):      10,
    (1, 1):       5,
}

# Directions: (delta_row, delta_col)
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]


def _in_bounds(r, c):
    """Kiểm tra tọa độ nằm trong bàn cờ."""
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def _count_line(grid, r, c, dr, dc, player):
    """
    Đếm số quân liên tiếp của `player` theo hướng (dr, dc) bắt đầu từ (r, c),
    đồng thời kiểm tra hai đầu có trống hay không.

    Returns:
        (count, open_ends)
    """
    count = 1  # bao gồm ô (r, c) hiện tại

    # Đếm theo chiều thuận
    i, j = r + dr, c + dc
    while _in_bounds(i, j) and grid[i][j] == player:
        count += 1
        i += dr
        j += dc
    # Sau vòng lặp, (i, j) là ô đầu tiên không phải quân của player theo chiều thuận
    open_forward = _in_bounds(i, j) and grid[i][j] is None

    # Đếm theo chiều ngược
    i, j = r - dr, c - dc
    while _in_bounds(i, j) and grid[i][j] == player:
        count += 1
        i -= dr
        j -= dc
    open_backward = _in_bounds(i, j) and grid[i][j] is None

    open_ends = int(open_forward) + int(open_backward)
    return count, open_ends


def score_for_player(grid, player):
    """
    Tính tổng điểm heuristic cho `player` trên toàn bàn cờ.

    Mỗi ô được kiểm tra theo 4 hướng; tránh đếm trùng cùng một chuỗi
    bằng cách chỉ xét ô là điểm bắt đầu (ô đầu tiên của chuỗi) theo mỗi hướng.
    """
    total = 0
    visited = set()

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] != player:
                continue

            for dr, dc in DIRECTIONS:
                # Chỉ xử lý nếu đây là đầu chuỗi (ô trước không phải quân cùng loại)
                pr, pc = r - dr, c - dc
                if _in_bounds(pr, pc) and grid[pr][pc] == player:
                    continue  # không phải đầu chuỗi → bỏ qua

                state_key = (r, c, dr, dc)
                if state_key in visited:
                    continue
                visited.add(state_key)

                count, open_ends = _count_line(grid, r, c, dr, dc, player)
                if open_ends == 0 and count < 5:
                    continue  # chuỗi bị chặn cả hai đầu, không có giá trị

                score = SCORE_TABLE.get((count, open_ends), 0)
                # Chuỗi dài hơn 5 vẫn tính là thắng
                if count >= 5:
                    score = 100_000
                total += score

    return total


def evaluate_board(grid, ai_player='O', human_player='X'):
    """
    Đánh giá tổng thể bàn cờ từ góc nhìn của AI.

    Returns:
        int — điểm dương = lợi thế AI, âm = lợi thế đối thủ.
    """
    ai_score = score_for_player(grid, ai_player)
    human_score = score_for_player(grid, human_player)
    return ai_score - human_score


def evaluate_move(grid, r, c, ai_player='O', human_player='X', defend_weight=0.9):
    """Đánh giá giá trị của một nước đi mà không làm thay đổi bàn cờ."""
    if grid[r][c] is not None:
        return None

    grid[r][c] = ai_player
    attack_score = score_for_player(grid, ai_player)
    grid[r][c] = None

    grid[r][c] = human_player
    defend_score = score_for_player(grid, human_player)
    grid[r][c] = None

    if defend_score >= 10_000:
        effective_defend_weight = 1.5
    elif defend_score >= 5_000:
        effective_defend_weight = 1.2
    else:
        effective_defend_weight = defend_weight

    return attack_score + defend_score * effective_defend_weight


def get_candidate_cells(grid, size=None, radius=2):
    """Trả về tập hợp các ô trống nằm trong bán kính `radius` quanh quân đã đặt."""
    if size is None:
        size = BOARD_SIZE

    candidates = set()
    for r in range(size):
        for c in range(size):
            if grid[r][c] is not None:
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        nr, nc = r + dr, c + dc
                        if _in_bounds(nr, nc) and grid[nr][nc] is None:
                            candidates.add((nr, nc))
    return candidates


def get_best_move(board, ai_player='O', human_player='X'):
    """Chọn nước đi tốt nhất cho AI dựa trên heuristic."""
    grid = board.grid
    size = board.size
    best_score = -float('inf')
    best_move = None

    candidates = get_candidate_cells(grid, size)
    if not candidates:
        mid = size // 2
        return (mid, mid)

    for r, c in candidates:
        if grid[r][c] is not None:
            continue

        combined = evaluate_move(grid, r, c, ai_player=ai_player, human_player=human_player)
        if combined is None:
            continue

        if combined > best_score:
            best_score = combined
            best_move = (r, c)

    return best_move


def get_easy_move(board, ai_player='O', human_player='X', top_k=3, defend_weight=0.9):
    """Chọn một nước đi heuristic tốt ngẫu nhiên từ top-k ứng viên."""
    grid = board.grid
    size = board.size
    moves_with_score = []

    candidates = get_candidate_cells(grid, size)
    if not candidates:
        mid = size // 2
        return (mid, mid)

    for r, c in candidates:
        if grid[r][c] is not None:
            continue

        combined = evaluate_move(
            grid,
            r,
            c,
            ai_player=ai_player,
            human_player=human_player,
            defend_weight=defend_weight,
        )
        if combined is None:
            continue
        moves_with_score.append((combined, (r, c)))

    if not moves_with_score:
        return None

    moves_with_score.sort(reverse=True, key=lambda x: x[0])
    top_moves = moves_with_score[:min(top_k, len(moves_with_score))]
    return random.choice(top_moves)[1]
