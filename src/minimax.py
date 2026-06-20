"""
minimax.py — Giai Đoạn 6: Minimax + Alpha-Beta Pruning
======================================================
Xây dựng cây tìm kiếm Minimax để AI dự đoán nước đi tương lai.
Tối ưu tìm kiếm bằng Alpha-Beta Pruning.

Mục Tiêu:
  - Mô phỏng các nước đi tương lai (lên đến độ sâu `depth`)
  - Đánh giá bàn cờ bằng đệ quy
  - Chọn nước đi tốt nhất dựa trên điểm số
"""

from config import BOARD_SIZE
from heuristic import score_for_player

# Giá trị infinity để dùng trong minimax
INF = float('inf')

# ---------------------------------------------------------------------------
# Hàm Đánh Giá Trạng Thái Bàn Cờ
# ---------------------------------------------------------------------------

def evaluate_board(grid, ai_player, human_player):
    """
    Đánh giá trạng thái bàn cờ từ góc nhìn AI.
    
    Công thức:
        score = (AI score) - (Human score)
    
    Nếu AI thắng: +INF
    Nếu Human thắng: -INF
    
    Args:
        grid:         2D list bàn cờ [r][c] ∈ {None, 'X', 'O'}
        ai_player:    ký hiệu quân AI   (mặc định 'O')
        human_player: ký hiệu quân người (mặc định 'X')
    
    Returns:
        Điểm số (float): nếu AI cao → AI tốt, nếu thấp → Human tốt
    """
    ai_score = score_for_player(grid, ai_player)
    human_score = score_for_player(grid, human_player)
    
    # Nếu AI hoặc Human có 5 quân → game kết thúc
    if ai_score >= 100_000:
        return INF  # AI thắng
    if human_score >= 100_000:
        return -INF  # Human thắng
    
    # Trả về hiệu số điểm
    return ai_score - human_score


def is_terminal(grid, ai_player, human_player):
    """
    Kiểm tra trò chơi có kết thúc không.
    
    Game kết thúc khi:
      - Một trong hai người có 5 quân liên tiếp
      - Bàn cờ đầy (không còn ô trống)
    
    Returns:
        bool: True nếu game kết thúc
    """
    ai_score = score_for_player(grid, ai_player)
    human_score = score_for_player(grid, human_player)
    
    if ai_score >= 100_000 or human_score >= 100_000:
        return True
    
    # Kiểm tra bàn cờ đầy
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] is None:
                return False
    
    return True


def get_all_moves(grid):
    """
    Trả về tất cả các ô trống trên bàn cờ.
    
    Ưu tiên: nước đi gần các quân hiện có hơn (để tìm kiếm hiệu quả).
    
    Returns:
        list: [(row, col), ...] các ô có thể đi
    """
    empty_cells = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] is None:
                empty_cells.append((r, c))
    
    return empty_cells


def sort_moves_by_proximity(grid, moves):
    """
    Sắp xếp nước đi theo gần với các quân hiện có (tính heuristic).
    Nước đi gần quân hiện có có khả năng tốt hơn.
    
    Args:
        grid:  2D list bàn cờ
        moves: list [(row, col), ...]
    
    Returns:
        list: moves được sắp xếp
    """
    def distance_to_closest_piece(r, c):
        """Tính khoảng cách đến quân gần nhất."""
        min_dist = INF
        for rr in range(BOARD_SIZE):
            for cc in range(BOARD_SIZE):
                if grid[rr][cc] is not None:
                    dist = abs(r - rr) + abs(c - cc)
                    min_dist = min(min_dist, dist)
        return min_dist
    
    # Sắp xếp theo khoảng cách (gần nhất trước)
    return sorted(moves, key=lambda move: distance_to_closest_piece(move[0], move[1]))


# ---------------------------------------------------------------------------
# Minimax với Alpha-Beta Pruning
# ---------------------------------------------------------------------------

def minimax(grid, depth, is_maximizing, alpha, beta, ai_player, human_player):
    """
    Thuật toán Minimax với Alpha-Beta Pruning.
    
    Ý tưởng:
      - Maximizing: AI chọn nước để max hóa điểm → điểm càng cao càng tốt
      - Minimizing: Human chọn nước để min hóa điểm (từ góc AI) → điểm càng thấp càng tốt
      - Alpha-Beta Pruning: cắt nhánh không cần thiết để tối ưu tìm kiếm
    
    Args:
        grid:              2D list bàn cờ hiện tại [r][c] ∈ {None, 'X', 'O'}
        depth:             độ sâu tìm kiếm còn lại (0 = dừng)
        is_maximizing:     True = lượt AI, False = lượt Human
        alpha:             tốt nhất cho Maximizer (dùng pruning)
        beta:              tốt nhất cho Minimizer (dùng pruning)
        ai_player:         ký hiệu quân AI ('O')
        human_player:      ký hiệu quân người ('X')
    
    Returns:
        float: Điểm số của trạng thái này
    """
    # Điều kiện dừng: depth = 0 hoặc game kết thúc
    if depth == 0 or is_terminal(grid, ai_player, human_player):
        return evaluate_board(grid, ai_player, human_player)
    
    moves = get_all_moves(grid)
    
    if not moves:  # Bàn cờ đầy
        return evaluate_board(grid, ai_player, human_player)
    
    # Sắp xếp nước đi để tìm kiếm tốt hơn (pruning hiệu quả hơn)
    moves = sort_moves_by_proximity(grid, moves)
    
    if is_maximizing:
        # Lượt AI: chọn nước có điểm cao nhất
        max_eval = -INF
        for r, c in moves:
            # Thử đi ở (r, c)
            grid[r][c] = ai_player
            eval_score = minimax(grid, depth - 1, False, alpha, beta, ai_player, human_player)
            grid[r][c] = None  # Undo
            
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            
            # Alpha-Beta Pruning: nếu alpha >= beta, cắt nhánh
            if alpha >= beta:
                break
        
        return max_eval
    
    else:
        # Lượt Human: chọn nước có điểm thấp nhất (từ góc AI)
        min_eval = INF
        for r, c in moves:
            # Thử đi ở (r, c)
            grid[r][c] = human_player
            eval_score = minimax(grid, depth - 1, True, alpha, beta, ai_player, human_player)
            grid[r][c] = None  # Undo
            
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            
            # Alpha-Beta Pruning: nếu alpha >= beta, cắt nhánh
            if alpha >= beta:
                break
        
        return min_eval


# ---------------------------------------------------------------------------
# Hàm Tìm Nước Đi Tốt Nhất Bằng Minimax
# ---------------------------------------------------------------------------

def get_best_move_minimax(board, depth=4, ai_player='O', human_player='X'):
    """
    Tìm nước đi tốt nhất cho AI bằng Minimax + Alpha-Beta Pruning.
    
    Args:
        board:         đối tượng Board
        depth:         độ sâu tìm kiếm (mặc định 4 = tìm 4 nước trước)
        ai_player:     ký hiệu quân AI ('O')
        human_player:  ký hiệu quân người ('X')
    
    Returns:
        (row, col) nước đi tốt nhất, hoặc None nếu bàn cờ đầy
    """
    moves = get_all_moves(board.grid)
    
    if not moves:
        return None
    
    # Nếu chỉ 1 ô trống, đi luôn
    if len(moves) == 1:
        return moves[0]
    
    best_move = None
    best_eval = -INF
    
    # Sắp xếp nước đi theo gần các quân hiện có
    moves = sort_moves_by_proximity(board.grid, moves)
    
    for r, c in moves:
        # Thử đi ở (r, c)
        board.grid[r][c] = ai_player
        
        # Tính điểm cho nước đi này (lượt tiếp theo là Human)
        eval_score = minimax(board.grid, depth - 1, False, -INF, INF, ai_player, human_player)
        
        board.grid[r][c] = None  # Undo
        
        # Chọn nước có điểm cao nhất
        if eval_score > best_eval:
            best_eval = eval_score
            best_move = (r, c)
    
    return best_move
