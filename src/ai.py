"""
ai.py — Module AI cho Gomoku
==============================
Giai Đoạn 4: get_random_move  — AI đi ngẫu nhiên (giữ lại để tham khảo)
Giai Đoạn 5: get_best_move    — AI đánh giá heuristic (nước đi chiến thuật)
"""

import random
from heuristic import get_best_move
from minimax import get_best_move_minimax

def get_ai_move_minimax(board, ai_player='O', human_player='X'):
    """
    AI sử dụng Minimax + Alpha-Beta
    """
    move = get_best_move_minimax(
        board,
        depth=1,
        ai_player=ai_player,
        human_player=human_player
    )

    return move
# ---------------------------------------------------------------------------
# Giai Đoạn 4 — AI ngẫu nhiên (legacy, vẫn giữ để fallback / kiểm thử)
# ---------------------------------------------------------------------------

def get_random_move(board):
    """
    Find all empty cells on the board and return one chosen randomly.
    Returns:
        (row, col) tuple of the selected move, or None if the board is full.
    """
    empty_cells = []
    for r in range(board.size):
        for c in range(board.size):
            if not board.is_occupied(r, c):
                empty_cells.append((r, c))

    if not empty_cells:
        return None

    return random.choice(empty_cells)


# ---------------------------------------------------------------------------
# Giai Đoạn 5 — AI heuristic (nước đi chiến thuật)
# ---------------------------------------------------------------------------

def get_ai_move(board, ai_player='O', human_player='X'):
    """
    Trả về nước đi tốt nhất cho AI bằng đánh giá heuristic.

    Ưu tiên:
      1. Thắng ngay nếu có thể.
      2. Chặn đối thủ nếu đối thủ sắp thắng.
      3. Chọn ô có điểm kết hợp (tấn công + phòng thủ) cao nhất.

    Args:
        board:        đối tượng Board
        ai_player:    ký hiệu quân AI   (mặc định 'O')
        human_player: ký hiệu quân người (mặc định 'X')

    Returns:
        (row, col) hoặc None nếu bàn cờ đầy.
    """
    move = get_best_move(board, ai_player=ai_player, human_player=human_player)
    if move is not None:
        return move
    # Fallback: nếu heuristic không trả về gì (vô lý), dùng ngẫu nhiên
    return get_random_move(board)
