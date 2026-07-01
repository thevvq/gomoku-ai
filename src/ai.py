"""
ai.py — Module AI cho Gomoku
==============================
Ba mức độ khó với hành vi phân biệt rõ ràng:

  easy   — AI đơn giản: chọn heuristic nhưng thường xuyên sai lầm,
            KHÔNG kiểm tra thắng ngay hay chặn đối thủ (trừ 4-liên).
  medium — AI khá: thắng ngay nếu có thể, chặn đối thủ khi cần,
            dùng minimax nông (depth 2-3).
  hard   — AI mạnh: thắng ngay, chặn sớm, minimax sâu (depth 4-5),
            xét nhiều ứng viên hơn.
"""

import random
from heuristic import get_best_move, get_candidate_cells, get_easy_move, score_for_player
from minimax import get_best_move_minimax

# ---------------------------------------------------------------------------
# Helpers — phát hiện tình huống buộc phải xử lý
# ---------------------------------------------------------------------------

def _count_empty_cells(board):
    return sum(
        1 for r in range(board.size)
        for c in range(board.size)
        if not board.is_occupied(r, c)
    )


def _get_winning_move(board, ai_player='O', human_player='X'):
    """
    Tìm nước đi khiến AI thắng ngay (5 quân liên tiếp).
    Trả về (r, c) hoặc None.
    """
    for r in range(board.size):
        for c in range(board.size):
            if board.is_occupied(r, c):
                continue
            board.grid[r][c] = ai_player
            score = score_for_player(board.grid, ai_player)
            board.grid[r][c] = None
            if score >= 100_000:
                return (r, c)
    return None


def _get_forced_block(board, ai_player='O', human_player='X', threshold=10_000):
    """
    Tìm nước chặn đối thủ sắp thắng.

    threshold:
      10_000 → chỉ chặn khi đối thủ có 4-mở (sắp thắng ngay lập tức)
       1_000 → chặn cả khi đối thủ có 3-mở (nguy hiểm tiềm ẩn)
    """
    critical = []
    for r in range(board.size):
        for c in range(board.size):
            if board.is_occupied(r, c):
                continue
            board.grid[r][c] = human_player
            defend_score = score_for_player(board.grid, human_player)
            board.grid[r][c] = None
            if defend_score >= threshold:
                critical.append((defend_score, r, c))

    if not critical:
        return None
    critical.sort(reverse=True)
    return (critical[0][1], critical[0][2])


# ---------------------------------------------------------------------------
# Mức DỄ — AI "gà mờ": hay sai lầm, dễ bị thắng
# ---------------------------------------------------------------------------

def _get_easy_ai_move(board, ai_player='O', human_player='X'):
    """
    Mức Dễ (yếu hơn):
      - 30% xác suất đi hoàn toàn ngẫu nhiên vào ô lân cận.
      - Chỉ thắng ngay / chặn khi đối thủ thực sự thắng (100_000).
      - Không phòng thủ sớm, không đọc trước.
      - Chọn ngẫu nhiên trong top-8 nước heuristic (trọng số phòng thủ rất thấp).
    """
    # 30% xác suất đi ngẫu nhiên (đi bừa)
    if random.random() < 0.30:
        candidates = get_candidate_cells(board.grid, board.size, radius=2)
        empty = [pos for pos in candidates if board.grid[pos[0]][pos[1]] is None]
        if empty:
            return random.choice(empty)

    # Chỉ thắng ngay — không bao giờ bỏ nước thắng
    winning_move = _get_winning_move(board, ai_player, human_player)
    if winning_move is not None:
        return winning_move

    # Chỉ chặn khi đối thủ ĐÃ CÓ 4-mở (sắp thắng ngay lập tức)
    # KHÔNG chặn 3-mở hay đòn hiểm sớm
    forced = _get_forced_block(board, ai_player, human_player, threshold=10_000)
    if forced is not None and random.random() < 0.70:  # 30% bỏ lỡ cả chặn 4-mở
        return forced

    return get_easy_move(
        board,
        ai_player=ai_player,
        human_player=human_player,
        top_k=8,
        defend_weight=0.3,
    )


# ---------------------------------------------------------------------------
# Mức VỪA — AI trung bình: đủ chiến thuật, minimax nông
# ---------------------------------------------------------------------------

def _get_medium_ai_move(board, ai_player='O', human_player='X'):
    """
    Mức Vừa:
      1. Thắng ngay nếu có thể.
      2. Chặn khi đối thủ có 4-mở hoặc 3-mở nguy hiểm (threshold 1000).
      3. Minimax depth 2 khi còn nhiều ô trống, depth 3 khi ít hơn.
    """
    winning_move = _get_winning_move(board, ai_player, human_player)
    if winning_move is not None:
        return winning_move

    forced = _get_forced_block(board, ai_player, human_player, threshold=1_000)
    if forced is not None and random.random() < 0.80:  # 20% bỏ lỡ đòn nguy hiểm
        return forced

    empty = _count_empty_cells(board)
    depth = 2 if empty > 160 else 3

    move = get_best_move_minimax(
        board, depth=depth,
        ai_player=ai_player, human_player=human_player,
        max_candidates=12
    )
    if move is not None:
        return move

    return get_best_move(board, ai_player=ai_player, human_player=human_player)


# ---------------------------------------------------------------------------
# Mức KHÓ — AI mạnh: minimax sâu, chặn sớm, nhiều ứng viên
# ---------------------------------------------------------------------------

def _get_hard_ai_move(board, ai_player='O', human_player='X'):
    """
    Mức Khó:
      1. Thắng ngay nếu có thể.
      2. Chặn khi đối thủ nguy hiểm (threshold 1000, bao gồm 3-mở).
      3. Minimax depth 3 khi bàn còn đông quân, depth 4-5 khi ít.
         Xét nhiều ứng viên hơn (max_candidates=20) → tính toán toàn diện.
    """
    winning_move = _get_winning_move(board, ai_player, human_player)
    if winning_move is not None:
        return winning_move

    forced = _get_forced_block(board, ai_player, human_player, threshold=1_000)
    if forced is not None:
        return forced

    empty = _count_empty_cells(board)
    if empty > 170:
        depth = 3
    elif empty > 100:
        depth = 4
    else:
        depth = 5

    move = get_best_move_minimax(
        board, depth=depth,
        ai_player=ai_player, human_player=human_player,
        max_candidates=20
    )
    if move is not None:
        return move

    return get_best_move(board, ai_player=ai_player, human_player=human_player)


# ---------------------------------------------------------------------------
# Dispatcher chính — gọi từ server.py
# ---------------------------------------------------------------------------

def get_ai_move(board, ai_player='O', human_player='X', difficulty='medium'):
    """
    Trả về nước đi tốt nhất cho AI theo mức độ khó được chọn.

    Args:
        board:        đối tượng Board
        ai_player:    ký hiệu quân AI   (mặc định 'O')
        human_player: ký hiệu quân người (mặc định 'X')
        difficulty:   'easy' | 'medium' | 'hard'

    Returns:
        (row, col) hoặc None nếu bàn cờ đầy.
    """
    difficulty = (difficulty or 'medium').lower()

    if difficulty == 'easy':
        return _get_easy_ai_move(board, ai_player, human_player)
    elif difficulty == 'hard':
        return _get_hard_ai_move(board, ai_player, human_player)
    else:  # medium (default)
        return _get_medium_ai_move(board, ai_player, human_player)


# ---------------------------------------------------------------------------
# Legacy helpers (giữ lại để tương thích / kiểm thử)
# ---------------------------------------------------------------------------

def get_ai_move_minimax(board, ai_player='O', human_player='X'):
    """AI sử dụng Minimax + Alpha-Beta (depth=1, legacy)."""
    move = get_best_move_minimax(
        board, depth=1,
        ai_player=ai_player, human_player=human_player,
    )
    return move


def get_random_move(board):
    """Chọn ngẫu nhiên một ô trống (legacy / fallback)."""
    empty_cells = [
        (r, c)
        for r in range(board.size)
        for c in range(board.size)
        if not board.is_occupied(r, c)
    ]
    return random.choice(empty_cells) if empty_cells else None
