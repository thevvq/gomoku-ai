"""
minimax.py — Giai đoạn 6: Minimax + Alpha-Beta Pruning
========================================================
Xây dựng cây tìm kiếm Minimax để AI dự đoán các nước đi tương lai.
Tối ưu hóa quá trình tìm kiếm bằng kỹ thuật Alpha-Beta Pruning.

Mục tiêu:
  - Mô phỏng các nước đi tương lai (lên đến độ sâu `depth`)
  - Đánh giá trạng thái bàn cờ một cách đệ quy
  - Chọn nước đi tốt nhất dựa trên điểm số
"""

from config import BOARD_SIZE
from heuristic import evaluate_move, get_candidate_cells, score_for_player

# Giá trị infinity để dùng trong minimax
INF = float('inf')

# ---------------------------------------------------------------------------
# Hàm Đánh Giá Trạng Thái Bàn Cờ
# ---------------------------------------------------------------------------

def evaluate_board(grid, ai_player, human_player):
    """
    Đánh giá trạng thái bàn cờ từ góc nhìn của AI.
    
    Công thức tính điểm:
        score = (điểm AI) - (điểm Human)
    
    Trường hợp đặc biệt:
      - Nếu AI thắng: trả về +INF
      - Nếu Human thắng: trả về -INF
    
    Args:
        grid:         2D list bàn cờ với các ô [r][c] ∈ {None, 'X', 'O'}
        ai_player:    ký hiệu quân của AI (mặc định 'O')
        human_player: ký hiệu quân của người chơi (mặc định 'X')
    
    Returns:
        Điểm số (float): giá trị cao → tốt cho AI, giá trị thấp → tốt cho Human
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
    Kiểm tra xem trò chơi đã kết thúc hay chưa.
    
    Trò chơi kết thúc khi:
      - Một trong hai người chơi có 5 quân liên tiếp
      - Bàn cờ đầy (không còn ô trống nào)
    
    Returns:
        bool: True nếu trò chơi kết thúc, False nếu vẫn tiếp tục
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
    Lấy danh sách tất cả các ô trống trên bàn cờ.
    
    Ghi chú: Các ô này sẽ được sắp xếp theo độ gần với các quân hiện có
    để tối ưu hóa quá trình tìm kiếm.
    
    Returns:
        list: Danh sách các ô có thể đi [(row, col), ...]
    """
    empty_cells = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] is None:
                empty_cells.append((r, c))
    
    return empty_cells


def get_candidate_moves(grid, radius=1):
    """Lấy các ô trống nằm gần quân đã có trên bàn cờ."""
    return list(get_candidate_cells(grid, size=BOARD_SIZE, radius=radius))


def _limit_moves(moves, max_moves):
    if len(moves) <= max_moves:
        return moves
    return moves[:max_moves]


def sort_moves_by_proximity(grid, moves, ai_player='O', human_player='X'):
    """Sắp xếp nước đi theo heuristic trước, khoảng cách gần quân cũ là phụ."""
    def distance_to_closest_piece(r, c):
        """Tính khoảng cách Manhattan đến quân gần nhất trên bàn cờ."""
        min_dist = INF
        for rr in range(BOARD_SIZE):
            for cc in range(BOARD_SIZE):
                if grid[rr][cc] is not None:
                    dist = abs(r - rr) + abs(c - cc)
                    min_dist = min(min_dist, dist)
        return min_dist

    def move_sort_key(move):
        r, c = move
        heuristic_score = evaluate_move(grid, r, c, ai_player=ai_player, human_player=human_player)
        if heuristic_score is None:
            heuristic_score = -INF
        proximity = distance_to_closest_piece(r, c)
        return (-heuristic_score, proximity, r, c)

    return sorted(moves, key=move_sort_key)


# ---------------------------------------------------------------------------
# Minimax với Alpha-Beta Pruning
# ---------------------------------------------------------------------------

def minimax(grid, depth, is_maximizing, alpha, beta, ai_player, human_player):
    """
    Thuật toán Minimax kết hợp với Alpha-Beta Pruning.
    
    Nguyên lý hoạt động:
      - Maximizing: AI tìm nước đi để tối đa hóa điểm → điểm cao = tốt cho AI
      - Minimizing: Human tìm nước đi để tối thiểu hóa điểm → điểm thấp = tốt cho Human
      - Alpha-Beta Pruning: loại bỏ các nhánh không cần khảo sát để tối ưu tìm kiếm
    
    Args:
        grid:              2D list trạng thái bàn cờ [r][c] ∈ {None, 'X', 'O'}
        depth:             độ sâu tìm kiếm còn lại (0 = dừng tìm kiếm)
        is_maximizing:     True = lượt tối đa (AI), False = lượt tối thiểu (Human)
        alpha:             giá trị tốt nhất hiện tại cho người tối đa
        beta:              giá trị tốt nhất hiện tại cho người tối thiểu
        ai_player:         ký hiệu quân của AI (thường là 'O')
        human_player:      ký hiệu quân của người chơi (thường là 'X')
    
    Returns:
        float: Điểm đánh giá của trạng thái bàn cờ hiện tại
    """
    # Điều kiện dừng: không còn độ sâu hoặc trò chơi đã kết thúc
    if depth == 0 or is_terminal(grid, ai_player, human_player):
        return evaluate_board(grid, ai_player, human_player)
    
    moves = get_candidate_moves(grid)
    if not moves:
        moves = get_all_moves(grid)
    
    if not moves:  # Bàn cờ đầy, không còn nước đi
        return evaluate_board(grid, ai_player, human_player)
    
    # Sắp xếp nước đi để tìm kiếm tốt hơn (pruning hiệu quả hơn)
    moves = sort_moves_by_proximity(grid, moves, ai_player=ai_player, human_player=human_player)
    moves = _limit_moves(moves, 12 if depth <= 2 else 10)
    
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

def get_best_move_minimax(board, depth=4, ai_player='O', human_player='X', max_candidates=16):
    """
    Tìm nước đi tốt nhất cho AI sử dụng thuật toán Minimax + Alpha-Beta Pruning.
    
    Args:
        board:          đối tượng Board chứa trạng thái bàn cờ
        depth:          độ sâu tìm kiếm (mặc định 4 = xem trước 4 nước)
        ai_player:      ký hiệu quân của AI (mặc định 'O')
        human_player:   ký hiệu quân của người chơi (mặc định 'X')
        max_candidates: số nước ứng viên tối đa xét ở nốt gốc.
                        Cao hơn → AI mạnh hơn nhưng chậm hơn.
    
    Returns:
        Tuple (row, col) nước đi tốt nhất, hoặc None nếu bàn cờ không còn ô trống
    """
    moves = get_candidate_moves(board.grid)
    if not moves:
        moves = get_all_moves(board.grid)
    
    if not moves:
        return None
    
    # Nếu chỉ còn 1 ô trống, trực tiếp chọn ô đó
    if len(moves) == 1:
        return moves[0]
    
    best_move = None
    best_eval = -INF
    
    # Sắp xếp nước đi để tìm kiếm hiệu quả hơn (alpha-beta pruning tốt hơn)
    moves = sort_moves_by_proximity(board.grid, moves, ai_player=ai_player, human_player=human_player)
    moves = _limit_moves(moves, max_candidates)
    
    for r, c in moves:
        # Thử đặt quân AI tại vị trí (r, c)
        board.grid[r][c] = ai_player
        
        # Tính điểm đánh giá cho nước đi này (lượt tiếp theo là của Human)
        eval_score = minimax(board.grid, depth - 1, False, -INF, INF, ai_player, human_player)
        
        board.grid[r][c] = None  # Hoàn tác nước đi
        
        # Cập nhật nước đi tốt nhất nếu tìm được điểm cao hơn
        if eval_score > best_eval:
            best_eval = eval_score
            best_move = (r, c)
    
    return best_move
